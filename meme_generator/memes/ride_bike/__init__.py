from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def ride_bike(images, texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    
    positions = [
        (100, 300, 600, 392),
        (100, 600, 600, 692),
        (100, 880, 600, 972),
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
                stroke_ratio=0.04,
            )
        except ValueError:
            raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "ride_bike",
    ride_bike,
    min_texts=3,
    max_texts=3,
    keywords=["骑车"],
    date_created=datetime(2025, 5, 19),
    date_modified=datetime(2025, 5, 19),
)
