import asyncio
import json
import logging
from asyncio import Semaphore
from typing import Literal

import nodriver
import validators
from curl_cffi.requests import AsyncSession
from nodriver.core.tab import Tab


class BingImages:
    selectors_mapping = {
        'strict': '#ss-strict',
        'moderate': '.ftrSe',
        'off': '#ss-off'
    }

    def __init__(self, base_url: str = 'https://www.bing.com', safe_search: bool = True):
        self.base_url = base_url
        self.safe_search = safe_search

        self._session = AsyncSession(impersonate='chrome', max_clients=100)

    @staticmethod
    async def _scrap_urls(tab: Tab, max_number: int):
        old_image_elements_count = 0

        while True:
            image_elements = await tab.select_all('.iusc')
            if len(image_elements) > max_number:
                break
            elif len(image_elements) > old_image_elements_count:
                old_image_elements_count = len(image_elements)
                await tab.scroll_down(100)
            else:
                button = await tab.query_selector('.btn_seemore')
                if button:
                    await button.click()
                else:
                    break
            await tab.sleep(2)

        image_urls = []
        for image_element in image_elements:
            if 'm' in image_element.attrs:
                image_url = json.loads(image_element.attrs['m'])['murl']
                if validators.url(image_url):
                    image_urls.append(image_url)
        return image_urls[:max_number]

    async def _set_safe_search(self, tab: Tab, new_value: Literal['strict', 'moderate', 'off']):
        drop_down = await tab.select('#ftr_ss_hl')
        await drop_down.click()
        toggle_button = await tab.select(self.selectors_mapping[new_value])
        await toggle_button.click()

    async def _search_urls(self, query: str, max_number: int = 100):
        browser = await nodriver.start(headless=True)
        try:
            tab = await browser.get(f'{self.base_url}/images/search?q={query}')
            if not self.safe_search:
                await self._set_safe_search(tab, 'off')
            image_urls = await self._scrap_urls(tab, max_number)
        finally:
            browser.stop()
        return image_urls

    async def _download_page(self, url: str, semaphore: Semaphore):
        async with semaphore:
            response = await self.session.get(url)
            return response.content

    async def get_images(self, query: str, max_number: int, sim_num: int = 10):
        image_urls = await self._search_urls(query, max_number)
        semaphore = asyncio.Semaphore(sim_num)
        tasks = [asyncio.create_task(self._download_page(url, semaphore)) for url in image_urls]

        async def _generator():
            for task in asyncio.as_completed(tasks):
                try:
                    yield await task
                except Exception as e:
                    logging.warning(str(e), exc_info=e)

        return _generator()

    @property
    def session(self):
        return self._session

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
