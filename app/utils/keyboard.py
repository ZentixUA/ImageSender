import asyncio

import keyboard as keyboard_sync


async def press_and_release(*args, **kwargs):
    def _press_and_release():
        return keyboard_sync.press_and_release(*args, **kwargs)

    return await asyncio.to_thread(_press_and_release)
