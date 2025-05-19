from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def turn_right(images, texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    
    positions = [
        (160, 180, 390, 362),
        (480, 180, 740, 362),
        (300, 700, 650, 800),
    ]
    
    for i, text in enumerate(texts):
        try:
            frame.draw_text(
                positions[i],
                text,
                allow_wrap=True,
                lines_align="center",
                min_fontsize=10,
                max_fontsize=80,
                fill=(255, 255, 255),
                stroke_fill=(0, 0, 0),
                stroke_ratio=0.04,
            )
        except ValueError:
            raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "turn_right",
    turn_right,
    min_texts=3,
    max_texts=3,
    keywords=["右转"],
    default_texts=["早起锻炼", "当死肥宅", "周末的我"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)
