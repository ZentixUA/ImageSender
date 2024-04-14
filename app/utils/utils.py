import asyncio
from io import BytesIO
from os import PathLike

import win32clipboard
from PIL import Image


async def prepare_image(image: PathLike | BytesIO):
    def _prepare_image():
        pil_image = Image.open(image)
        new_image = BytesIO()
        pil_image.convert('RGB').save(new_image, 'BMP')
        return new_image.getvalue()[14:]

    return await asyncio.to_thread(_prepare_image)


async def send_to_clipboard(clip_type: int, data):
    def _send_to_clipboard():
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    await asyncio.to_thread(_send_to_clipboard)
