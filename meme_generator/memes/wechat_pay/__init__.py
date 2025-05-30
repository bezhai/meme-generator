from datetime import datetime
from pathlib import Path

import qrcode
from pil_utils import BuildImage
from pydantic import Field
from qrcode.image.pil import PilImage

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"

help_text = "二维码内容"


class Model(MemeArgsModel):
    message: str = Field("", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-m", "--message"],
            args=[ParserArg(name="message", value="str")],
            help_text=help_text,
        ),
    ],
)

default_message = "https://github.com/bezhai/meme-generator"


def wechat_pay(images: list[BuildImage], texts: list[str], args: Model):
    message = args.message or default_message
    if not texts and not args.user_infos:
        raise TextOrNameNotEnough()
    name = texts[0] if texts else args.user_infos[0].name
    avatar = images[0]

    frame = BuildImage.open(img_dir / "0.png")

    qr = qrcode.QRCode(version=5, border=0, error_correction=qrcode.ERROR_CORRECT_Q)
    qr.add_data(message)
    qr.make(fit=True)
    qr_img = BuildImage(qr.make_image(image_factory=PilImage))  # type: ignore
    qr_img = qr_img.resize((530, 530))
    frame.paste(qr_img, (356, 439))

    block = BuildImage.new("RGBA", (186, 186), "white")
    frame.paste(block, (528, 611))

    avatar = avatar.convert("RGBA").resize((166, 166), keep_ratio=True).circle_corner(8)
    frame.paste(avatar, (538, 621), alpha=True)

    logo = BuildImage.open(img_dir / "logo.png")
    frame.paste(logo, (649, 734), alpha=True)

    try:
        frame.draw_text(
            (370, 1000, 872, 1100),
            name,
            allow_wrap=False,
            max_fontsize=80,
            min_fontsize=50,
            fill="black",
        )
    except ValueError:
        raise TextOverLength(name)

    return frame.save_jpg()


add_meme(
    "wechat_pay",
    wechat_pay,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    args_type=args_type,
    keywords=["微信支付"],
    date_created=datetime(2024, 10, 30),
    date_modified=datetime(2024, 10, 30),
)
