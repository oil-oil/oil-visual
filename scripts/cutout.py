#!/usr/bin/env python3
"""Remove a uniform chroma-key background and write a transparent PNG.

The script samples the key color from the image border, builds a soft alpha
matte from color distance, and removes key-color spill from antialiased edges.

Usage:
    python3 cutout.py source.png transparent.png
    python3 cutout.py source.png transparent.png \
        --transparent-threshold 12 --opaque-threshold 220
"""

from __future__ import annotations

import argparse
from pathlib import Path
from statistics import median

from PIL import Image


Color = tuple[int, int, int]
ALPHA_NOISE_FLOOR = 8
KEY_DOMINANCE_THRESHOLD = 16


def _clamp(value: float) -> int:
    return max(0, min(255, int(round(value))))


def _distance(color: Color, key: Color) -> int:
    return max(abs(color[index] - key[index]) for index in range(3))


def _smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def _distance_alpha(distance: int, transparent: float, opaque: float) -> int:
    if distance <= transparent:
        return 0
    if distance >= opaque:
        return 255
    ratio = (distance - transparent) / (opaque - transparent)
    return _clamp(255 * _smoothstep(ratio))


def _key_channels(key: Color) -> list[int]:
    strongest = max(key)
    if strongest < 128:
        return []
    return [
        index
        for index, value in enumerate(key)
        if value >= strongest - 16 and value >= 128
    ]


def _dominance_alpha(color: Color, key: Color) -> int:
    key_channels = _key_channels(key)
    if not key_channels:
        return 255

    other_channels = [index for index in range(3) if index not in key_channels]
    key_strength = min(color[index] for index in key_channels)
    other_strength = max((color[index] for index in other_channels), default=0)
    dominance = key_strength - other_strength
    if dominance <= 0:
        return 255

    denominator = max(1, max(key) - other_strength)
    return _clamp(255 * (1 - min(1.0, dominance / denominator)))


def _key_dominance(color: Color, key: Color) -> int:
    key_channels = _key_channels(key)
    if not key_channels:
        return 0
    other_channels = [index for index in range(3) if index not in key_channels]
    key_strength = min(color[index] for index in key_channels)
    other_strength = max((color[index] for index in other_channels), default=0)
    return key_strength - other_strength


def _looks_key_colored(color: Color, key: Color, distance: int) -> bool:
    if distance <= 32:
        return True
    if not _key_channels(key):
        return True
    return _key_dominance(color, key) >= KEY_DOMINANCE_THRESHOLD


def _despill(color: Color, key: Color, alpha: int) -> Color:
    if alpha >= 252:
        return color

    key_channels = _key_channels(key)
    if not key_channels:
        return color
    other_channels = [index for index in range(3) if index not in key_channels]
    if not other_channels:
        return color

    channels = list(color)
    neutral_edge = max(channels[index] for index in other_channels)
    for index in key_channels:
        channels[index] = min(channels[index], neutral_edge)
    return channels[0], channels[1], channels[2]


def _sample_border_key(image: Image.Image) -> Color:
    pixels = image.load()
    width, height = image.size
    band = max(1, min(width, height, 6))
    step = max(1, min(width, height) // 256)
    samples: list[Color] = []

    for x in range(0, width, step):
        for offset in range(band):
            samples.append(pixels[x, offset][:3])
            samples.append(pixels[x, height - 1 - offset][:3])
    for y in range(0, height, step):
        for offset in range(band):
            samples.append(pixels[offset, y][:3])
            samples.append(pixels[width - 1 - offset, y][:3])

    return tuple(
        int(round(median(sample[channel] for sample in samples)))
        for channel in range(3)
    )


def remove_background(
    input_path: Path,
    output_path: Path,
    transparent_threshold: float = 12,
    opaque_threshold: float = 220,
    despill: bool = True,
) -> tuple[Color, int, int]:
    image = Image.open(input_path).convert("RGBA")
    key = _sample_border_key(image)
    pixels = image.load()
    width, height = image.size
    transparent_count = 0
    partial_count = 0

    for y in range(height):
        for x in range(width):
            red, green, blue, source_alpha = pixels[x, y]
            color = (red, green, blue)
            distance = _distance(color, key)
            key_like = _looks_key_colored(color, key, distance)
            alpha = _distance_alpha(
                distance,
                transparent_threshold,
                opaque_threshold,
            )
            if key_like:
                alpha = min(alpha, _dominance_alpha(color, key))
            alpha = _clamp(alpha * (source_alpha / 255))
            if alpha <= ALPHA_NOISE_FLOOR:
                pixels[x, y] = (0, 0, 0, 0)
                transparent_count += 1
                continue

            if despill and key_like:
                red, green, blue = _despill(color, key, alpha)
            pixels[x, y] = (red, green, blue, alpha)
            if alpha < 255:
                partial_count += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return key, transparent_count, partial_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Opaque source image")
    parser.add_argument("output", type=Path, help="Transparent PNG output path")
    parser.add_argument(
        "--transparent-threshold",
        type=float,
        default=12,
        help="Color distance that becomes fully transparent (default: 12)",
    )
    parser.add_argument(
        "--opaque-threshold",
        type=float,
        default=220,
        help="Color distance that becomes fully opaque (default: 220)",
    )
    parser.add_argument(
        "--no-despill",
        action="store_true",
        help="Keep key-color spill on antialiased edge pixels",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Input image not found: {args.input}")
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Input and output paths must be different")
    if args.output.suffix.lower() != ".png":
        raise SystemExit("Output path must end in .png")
    if not 0 <= args.transparent_threshold < args.opaque_threshold <= 255:
        raise SystemExit(
            "Thresholds must satisfy 0 <= transparent < opaque <= 255"
        )

    key, transparent, partial = remove_background(
        args.input,
        args.output,
        transparent_threshold=args.transparent_threshold,
        opaque_threshold=args.opaque_threshold,
        despill=not args.no_despill,
    )
    print(f"cutout: {args.input} -> {args.output}")
    print(f"key: #{key[0]:02x}{key[1]:02x}{key[2]:02x}")
    print(f"transparent pixels: {transparent}")
    print(f"partially transparent pixels: {partial}")


if __name__ == "__main__":
    main()
