from PIL import Image, ImageDraw, ImageFont
import traceback, discord

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


create_wanted_png()
