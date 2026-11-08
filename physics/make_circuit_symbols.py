"""Writes a flashdeck bundle of the standard circuit symbols of GCSE Physics:
cards.yaml beside this script, and the symbols, drawn here, as SVG images in
images/. Being drawn for this deck, the images need no credit or licence.

    uv run python decks/physics/make_circuit_symbols.py
    uv run python manage.py flashdeck_import decks/physics
"""

import math
from pathlib import Path

from flashdeck.manifest import dump_manifest

HERE = Path(__file__).parent
W, H, Y = 240, 120, 60  # the image's size, and the height of the wire
INK = "#111111"


def svg(*parts):
    """A symbol on a white background (so that it shows on a dark page too)."""
    body = "\n".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#ffffff"/>
<g fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
{body}
</g>
</svg>
"""


def line(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def leads(left, right):
    """The wire on each side of a component that spans left to right."""
    return line(20, Y, left, Y) + "\n" + line(right, Y, W - 20, Y)


def rect(x, y, w, h, fill="none", stroke=True):
    stroke_attr = "" if stroke else ' stroke="none"'
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{stroke_attr}/>'
    )


def circle(cx, cy, r, fill="none"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def arrow(x1, y1, x2, y2, head=11):
    """A line with a filled arrowhead at (x2, y2)."""
    length = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    bx, by = x2 - head * ux, y2 - head * uy
    nx, ny = -uy * head * 0.45, ux * head * 0.45
    points = f"{x2},{y2} {bx + nx:.1f},{by + ny:.1f} {bx - nx:.1f},{by - ny:.1f}"
    shaft = line(x1, y1, f"{bx:.1f}", f"{by:.1f}")
    return f'{shaft}\n<polygon points="{points}" fill="{INK}" stroke-width="2"/>'


def letter(text):
    return (
        f'<text x="120" y="61" fill="{INK}" stroke="none" font-family="Helvetica, '
        f'Arial, sans-serif" font-size="30" font-weight="600" text-anchor="middle" '
        f'dominant-baseline="central">{text}</text>'
    )


def cell_plates(x):
    """A cell's plates: the long, thin positive one at x, the short, thick
    negative one to its right. Returns them and the x where the cell ends."""
    return (
        rect(x - 2, Y - 32, 4, 64, fill=INK, stroke=False)
        + "\n"
        + rect(x + 16, Y - 16, 9, 32, fill=INK, stroke=False)
    ), x + 25


def meter(text):
    return svg(leads(96, 144), circle(120, Y, 24), letter(text))


def resistor_box():
    return rect(85, Y - 14, 70, 28)


def diode(left=95, right=140, half=22):
    return "\n".join(
        [
            f'<polygon points="{left},{Y - half} {left},{Y + half} {right},{Y}"/>',
            line(right, Y - half, right, Y + half),
        ]
    )


def symbols():
    cell, end = cell_plates(108)
    first, first_end = cell_plates(68)
    second, second_end = cell_plates(145)
    led_circle = circle(118, Y, 34)
    return {
        "cell": svg(line(20, Y, 106, Y), line(end, Y, 220, Y), cell),
        "battery": svg(
            line(20, Y, 66, Y),
            first,
            line(first_end, Y, 143, Y),
            second,
            line(second_end, Y, 220, Y),
        ),
        "open-switch": svg(
            leads(85, 155),
            line(94, 57, 146, 30),
            circle(90, Y, 5, "#ffffff"),
            circle(150, Y, 5, "#ffffff"),
        ),
        "closed-switch": svg(
            leads(85, 155),
            line(94, Y, 146, Y),
            circle(90, Y, 5, "#ffffff"),
            circle(150, Y, 5, "#ffffff"),
        ),
        "diode": svg(line(20, Y, 220, Y), diode()),
        "led": svg(
            leads(84, 152),
            line(84, Y, 152, Y),
            led_circle,
            diode(102, 136, 18),
            arrow(128, 24, 146, 6),
            arrow(142, 31, 160, 13),
        ),
        "resistor": svg(leads(85, 155), resistor_box()),
        "variable-resistor": svg(
            leads(85, 155), resistor_box(), arrow(90, 92, 152, 26)
        ),
        "thermistor": svg(
            leads(85, 155), resistor_box(), line(66, 94, 82, 94), line(82, 94, 158, 26)
        ),
        "ldr": svg(
            leads(76, 164),
            circle(120, Y, 44),
            rect(94, Y - 12, 52, 24),
            arrow(58, 10, 90, 40),
            arrow(80, 4, 110, 34),
        ),
        "lamp": svg(
            leads(96, 144),
            circle(120, Y, 24),
            line(103, 43, 137, 77),
            line(103, 77, 137, 43),
        ),
        "fuse": svg(line(20, Y, 220, Y), rect(80, Y - 12, 80, 24)),
        "voltmeter": meter("V"),
        "ammeter": meter("A"),
    }


# Key: (answer, other accepted answers, notes).
CARDS = {
    "cell": ("cell", [], "The longer line is the positive terminal."),
    "battery": ("battery", [], "Two or more cells joined together."),
    "open-switch": (
        "open switch",
        ["switch (open)", "switch open"],
        "The circuit is broken, so no current flows.",
    ),
    "closed-switch": (
        "closed switch",
        ["switch (closed)", "switch closed"],
        "The circuit is complete, so current can flow.",
    ),
    "diode": (
        "diode",
        [],
        "Lets current flow one way only, in the direction the triangle points.",
    ),
    "led": (
        "light-emitting diode",
        ["LED", "light emitting diode"],
        "A diode that gives out light when a current flows through it. It is "
        "sometimes drawn without the circle.",
    ),
    "resistor": ("resistor", ["fixed resistor"], "Limits the current in a circuit."),
    "variable-resistor": (
        "variable resistor",
        ["rheostat"],
        "A resistor whose resistance can be changed, such as to dim a lamp.",
    ),
    "thermistor": (
        "thermistor",
        [],
        "A resistor whose resistance changes with temperature: for the usual kind, "
        "it falls as the thermistor gets hotter.",
    ),
    "ldr": (
        "light-dependent resistor",
        ["LDR", "light dependent resistor"],
        "A resistor whose resistance falls as the light on it gets brighter. It is "
        "sometimes drawn without the circle.",
    ),
    "lamp": (
        "lamp",
        ["bulb", "light bulb", "filament lamp"],
        "Gives out light when a current flows through it.",
    ),
    "fuse": (
        "fuse",
        [],
        "Melts, breaking the circuit, if the current becomes too large.",
    ),
    "voltmeter": (
        "voltmeter",
        [],
        "Measures the potential difference (voltage) across a component, so it is "
        "connected in parallel with it.",
    ),
    "ammeter": (
        "ammeter",
        [],
        "Measures the current, so it is connected in series.",
    ),
}


def with_articles(forms):
    """Each answer also with "a" or "an" before it (both, since "an LED" and "a
    lamp" follow the sound, not the letter)."""
    out = []
    for form in forms:
        out += [form, f"a {form}", f"an {form}"]
    return out


def bundle():
    cards = []
    for key, (text, alternatives, notes) in CARDS.items():
        cards.append(
            {
                "key": key,
                "prompt": "Name this circuit symbol.",
                "image": f"images/{key}.svg",
                "image_alt": "A circuit symbol",
                "answers": [
                    {
                        "text": text,
                        "alternatives": with_articles([text, *alternatives])[1:],
                    }
                ],
                "notes": notes,
            }
        )
    return {
        "format": "flashdeck/1",
        "subject": {"slug": "physics", "title": "Physics", "language": "en"},
        "decks": [
            {
                "slug": "circuit-symbols",
                "title": "Circuit symbols",
                "description": "The standard circuit symbols of GCSE Physics.",
                "public": True,
                "reference": (
                    "In a circuit diagram, wires are drawn as straight lines. A dot "
                    "marks where wires are joined; wires that cross without a dot "
                    "are not joined."
                ),
                "cards": cards,
            }
        ],
    }


if __name__ == "__main__":
    images = HERE / "images"
    images.mkdir(exist_ok=True)
    for key, image in symbols().items():
        (images / f"{key}.svg").write_text(image, encoding="utf-8")
    (HERE / "cards.yaml").write_text(
        "# Generated by make_circuit_symbols.py: change that script, not this file.\n"
        + dump_manifest(bundle()),
        encoding="utf-8",
    )
    print(f"Wrote {HERE / 'cards.yaml'} and {len(CARDS)} images")
