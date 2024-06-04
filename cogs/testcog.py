from PIL import Image, ImageDraw, ImageFont
import traceback, discord, asyncio
from concurrent.futures import ThreadPoolExecutor

POOL = ThreadPoolExecutor()

def create_wanted_png():
    base_width = 800
    wanted_poster = Image.open("profileAssets/wanted.png")  # (1545, 2000)
    avatar = Image.open("profileAssets/test_user.png")  # (128, 128)

    wpercent = (base_width / float(avatar.size[0]))
    hsize = int((float(avatar.size[1]) * float(wpercent)))
    avatar = avatar.resize((base_width, hsize), Image.Resampling.LANCZOS)

    wanted_poster.paste(avatar, (385, 540))
    poster = ImageDraw.Draw(wanted_poster)
    poster.text((385, 1540), "unseeyou", fill=(0, 0, 0), align="center", font=ImageFont.load_default(150))
    wanted_poster.show()


async def task_ImageGeneration(loop):
    result = await loop.run_in_executor(executor=POOL, func=create_wanted_png())
    return result


async def main():
    loop = asyncio.get_event_loop()
    await loop.create_task(task_ImageGeneration(loop))


asyncio.run(main())
