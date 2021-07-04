from __future__ import annotations
from itertools import chain
from PIL import Image as PILImage, ImageDraw
from random import seed, randint


class Image:
    def __init__(self, width: int, height: int, fill: tuple[int, int, int] = (0, 0, 0)):
        self.width = width
        self.height = height
        self._image = [[fill] * width for _ in range(height)]

    def blend(self, x: int, y: int, color: tuple[int, int, int], alpha: float = 0.5):
        self[x, y] = tuple(
            (channel * (1 - alpha) + new_channel * alpha) // 2
            for channel, new_channel in zip(self[x, y], color)
        )

    def generate(self):
        flattened = self._flatten_to_bytes()
        return PILImage.frombytes("RGB", (self.width, self.height), flattened)

    def __getitem__(self, coords: tuple[int, int]) -> tuple[int, int, int]:
        x, y = coords
        return self._image[y][x]

    def __setitem__(self, coords: tuple[int, int], color: tuple[int, int, int]):
        x, y = coords
        self._image[y][x] = color

    def _flatten_to_bytes(self) -> bytes:
        return bytes(chain(*chain(*self._image)))


def generate_stars(
    iteration: int, background: tuple[int, int, int], width: int, height: int
) -> PILImage:
    img = PILImage.new("RGB", (width, height), background)

    seed(0)
    draw = ImageDraw.Draw(img)
    for i in range(200):
        x, y = randint(0, 600), randint(0, 240)
        size = randint(1, 3)
        weight = (randint(0, 96) + iteration) % 97
        if weight > 48:
            weight = 96 - weight
        draw.ellipse(
            (x - size // 2, y - size // 2, x + size, y + size),
            fill=tuple(
                ((c * weight + bc * (48 - weight)) // 48)
                for c, bc in zip((255, 255, 255), background)
            ),
        )

    return img


def generate_image(width: int, height: int):
    frames: PILImage = []
    distance = 380
    bg = (0, 0, 30)
    fps = 24
    total_frames = 4 * fps
    for i in range(total_frames):
        img = generate_stars(i, bg, width, height)
        asteroid_lg = PILImage.open("asteroid-lg.png")

        f = i + 48
        d = 120
        img.paste(
            asteroid_lg.rotate(f % total_frames * d // total_frames),
            (
                240 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_lg.rotate(f % total_frames * d // total_frames),
        )

        f = i
        d = 120
        img.paste(
            asteroid_lg.rotate(f % total_frames * d // total_frames),
            (
                600 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_lg.rotate(f % total_frames * d // total_frames),
        )

        # Small Asteroid
        asteroid_sm = PILImage.open("asteroid-sm.png")

        f = i + 60
        d = 120
        img.paste(
            asteroid_sm.rotate(f % total_frames * d // total_frames),
            (
                30 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_sm.rotate(f % total_frames * d // total_frames),
        )

        f = i + 32
        d = -180
        img.paste(
            asteroid_sm.rotate(f % total_frames * d // total_frames),
            (
                300 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_sm.rotate(f % total_frames * d // total_frames),
        )

        f = i + 32
        d = -100
        img.paste(
            asteroid_sm.rotate(f % total_frames * d // total_frames),
            (
                120 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_sm.rotate(f % total_frames * d // total_frames),
        )

        f = i + 72
        d = 120
        img.paste(
            asteroid_sm.rotate(f % total_frames * d // total_frames),
            (
                500 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_sm.rotate(f % total_frames * d // total_frames),
        )

        f = i + 40
        d = -90
        img.paste(
            asteroid_sm.rotate(f % total_frames * d // total_frames),
            (
                580 - f % total_frames * distance // total_frames,
                240 - f % total_frames * distance // total_frames,
            ),
            asteroid_sm.rotate(f % total_frames * d // total_frames),
        )
        frames.append(img.convert("P", dither=PILImage.NONE))

    frames[0].save(
        "zechcodes-cover-july-2021.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1,
        loop=0,
        dither=PILImage.NONE,
    )


if __name__ == "__main__":
    generate_image(600, 240)
