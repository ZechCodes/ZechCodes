from __future__ import annotations
from PIL import Image as PILImage, ImageDraw
from random import seed, randint


def generate_stars(
    iteration: int,
    background: tuple[int, int, int],
    width: int,
    height: int,
    num: int = 200,
    min_diameter: int = 1,
    max_diameter: int = 3,
) -> PILImage:
    img = PILImage.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(img)
    for i in range(num):
        x, y = randint(0, width), randint(0, height)
        size = randint(min_diameter, max_diameter)
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
    seed(0)
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
        # frames.append(img.convert("P", dither=PILImage.NONE))
        frames.append(img)

    frames[0].save(
        "zechcodes-cover-july-2021.png",
        # save_all=True,
        # append_images=frames[1:],
        # duration=1,
        # loop=0,
        # dither=PILImage.NONE,
    )


def generate_image_twitter(width: int, height: int):
    bg = (0x0, 0x10, 0x43)
    img = generate_stars(0, bg, width, height, 400, 2, 5)

    asteroid_lg = PILImage.open("asteroid-lg.png")
    for i in range(7):
        rotation = randint(-180, 180)
        x = randint(0, width + asteroid_lg.width)
        y = randint(0, height + asteroid_lg.height)
        img.paste(
            asteroid_lg.rotate(rotation),
            (
                x - asteroid_lg.width // 2,
                y - asteroid_lg.height // 2,
            ),
            asteroid_lg.rotate(rotation),
        )

    asteroid_sm = PILImage.open("asteroid-sm.png")
    for i in range(15):
        rotation = randint(-180, 180)
        x = randint(0, width + asteroid_sm.width)
        y = randint(0, height + asteroid_sm.height)
        img.paste(
            asteroid_sm.rotate(rotation),
            (
                x - asteroid_sm.width // 2,
                y - asteroid_sm.height // 2,
            ),
            asteroid_sm.rotate(rotation),
        )

    img.save("zechcodes-cover-july-2021.png")


if __name__ == "__main__":
    # generate_image(600, 240)  # Discord cover
    generate_image_twitter(1500, 500)  # Twitter cover
