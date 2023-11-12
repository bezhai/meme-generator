from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def this_chichen(images: List[BuildImage], texts, args):
    text = texts[0] if texts else "这是十二生肖中的鸡"
    img = images[0].convert("RGBA").resize((640, 640), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (439, 956, 1001, 1038),
            text,
            max_fontsize=60,
            min_fontsize=30,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(
        img.perspective(((507, 0), (940, 351), (383, 625), (0, 256))),
        (201, 201),
        below=True,
    )
    return frame.save_jpg()


add_meme(
    "this_chichen",
    this_chichen,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts="这是十二生肖中的鸡",
    keywords=["这是鸡", "🐔"],
)
