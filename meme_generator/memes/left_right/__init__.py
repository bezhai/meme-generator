from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def left_right(images, texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    
    positions = [
        (265, 50, 415, 110),
        (640, 90, 790, 150),
    ]
    
    for i, text in enumerate(texts):
        try:
            frame.draw_text(
                positions[i],
                text,
                allow_wrap=True,
                lines_align="center",
                min_fontsize=10,
                max_fontsize=50,
                fill=(255, 255, 255),
                stroke_fill=(0, 0, 0),
                stroke_ratio=0.1,
            )
        except ValueError:
            raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "left_right",
    left_right,
    min_texts=2,
    max_texts=2,
    keywords=["左右"],
    default_texts=["左边", "右边"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)
