import pytest
import validators

from app.core.bing_images import BingImages


@pytest.mark.asyncio
async def test_search_images():
    query = 'cats'
    max_number = 5

    async with BingImages() as client:
        image_urls = await client._search_urls(query, max_number)

        assert len(image_urls) == max_number, 'The number of URLs does not match the expected number'
        assert all(validators.url(url) for url in image_urls), 'All returned URLs must be valid'


@pytest.mark.asyncio
async def test_get_images():
    query = 'cats'
    max_number = 5
    async with BingImages() as client:
        image_generator = await client.get_images(query, max_number)
        images_list = [image async for image in image_generator]

        assert len(images_list) == max_number
