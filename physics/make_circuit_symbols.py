"""Writes a flashdeck bundle of the circuit symbols of GCSE Physics: cards.yaml
beside this script, and the symbols, drawn here, as SVG images in images/. Being
drawn for this deck, the images need no credit or licence.

The symbols are those of Appendix 8 of Pearson's specification for International
GCSE Physics, drawn in the same way (as WJEC's are, too), with AQA's closed
switch: AQA's list is a subset of these.

    uv run python decks/physics/make_circuit_symbols.py
    uv run python manage.py flashdeck_import decks/physics --update
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


def line(x1, y1, x2, y2, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{extra}/>'


def leads(left, right, y=Y):
    """The wire on each side of a component that spans left to right."""
    return line(20, y, left, y) + "\n" + line(right, y, W - 20, y)


def rect(x, y, w, h, fill="none", stroke=True):
    stroke_attr = "" if stroke else ' stroke="none"'
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{stroke_attr}/>'
    )


def circle(cx, cy, r, fill="none"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def path(d, fill="none"):
    return f'<path d="{d}" fill="{fill}"/>'


def arrow(x1, y1, x2, y2, head=11):
    """A line with a filled arrowhead at (x2, y2)."""
    length = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    bx, by = x2 - head * ux, y2 - head * uy
    nx, ny = -uy * head * 0.45, ux * head * 0.45
    points = f"{x2},{y2} {bx + nx:.1f},{by + ny:.1f} {bx - nx:.1f},{by - ny:.1f}"
    shaft = line(x1, y1, f"{bx:.1f}", f"{by:.1f}")
    return f'{shaft}\n<polygon points="{points}" fill="{INK}" stroke-width="2"/>'


def letter(text, x=120, y=61, size=30):
    return (
        f'<text x="{x}" y="{y}" fill="{INK}" stroke="none" font-family="Helvetica, '
        f'Arial, sans-serif" font-size="{size}" font-weight="600" text-anchor="middle" '
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
    """A circle with a letter in it: an ammeter, voltmeter, motor or generator."""
    return svg(leads(96, 144), circle(120, Y, 24), letter(text))


def resistor_box():
    return rect(85, Y - 14, 70, 28)


def diode():
    """A triangle pointing the way the current may flow, and a bar."""
    return "\n".join(
        [
            leads(97, 141),
            f'<polygon points="97,{Y - 22} 97,{Y + 22} 139,{Y}"/>',
            line(141, Y - 22, 141, Y + 22),
        ]
    )


def coil(x, bulge):
    """Three loops of a transformer's coil, down from (x, 30), bulging to the
    right (bulge=1) or the left (bulge=0)."""
    loop = f"a 10 10 0 0 {bulge} 0 20"
    return path(f"M {x} 30 {loop} {loop} {loop}")


def terminals(left, right):
    """A power supply's two terminals: small open circles, with leads."""
    return "\n".join(
        [
            leads(left - 6, right + 6),
            circle(left, Y, 6, "#ffffff"),
            circle(right, Y, 6, "#ffffff"),
        ]
    )


BASE = 84  # the wire's height for components drawn above it


def symbols():
    cell, end = cell_plates(108)
    first, first_end = cell_plates(68)
    second, second_end = cell_plates(143)
    return {
        "cell": svg(line(20, Y, 106, Y), line(end, Y, 220, Y), cell),
        "battery": svg(
            line(20, Y, 66, Y),
            first,
            line(first_end + 4, Y, 137, Y, ' stroke-dasharray="5 7"'),
            second,
            line(second_end, Y, 220, Y),
        ),
        # A switch's lever is hinged at the end of the left-hand wire; the dot is
        # the contact at the start of the right-hand one, which the lever of a
        # closed switch rests on (as WJEC's symbols draw it).
        "open-switch": svg(
            line(20, Y, 95, Y),
            line(95, Y, 140, 35),
            line(145, Y, 220, Y),
            circle(145, Y, 3, INK),
        ),
        "closed-switch": svg(
            line(20, Y, 95, Y),
            line(95, Y, 155, 54.5),
            line(145, Y, 220, Y),
            circle(145, Y, 3, INK),
        ),
        "diode": svg(diode()),
        # The arrows (the light) start clear of the diode's bar, which ends at
        # (141, 38).
        "led": svg(diode(), arrow(112, 30, 130, 12), arrow(126, 34, 144, 16)),
        "resistor": svg(leads(85, 155), resistor_box()),
        "variable-resistor": svg(
            leads(85, 155), resistor_box(), arrow(90, 92, 152, 26)
        ),
        "thermistor": svg(
            leads(85, 155), resistor_box(), line(66, 94, 82, 94), line(82, 94, 158, 26)
        ),
        "ldr": svg(
            leads(85, 155),
            resistor_box(),
            arrow(80, 10, 101, 38),
            arrow(98, 6, 119, 34),
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
        "junction": svg(
            line(20, Y, 220, Y), line(120, Y, 120, 106), circle(120, Y, 6, INK)
        ),
        "crossing-wires": svg(line(20, Y, 220, Y), line(120, 14, 120, 106)),
        "dc-supply": svg(
            terminals(104, 136),
            line(97, 38, 111, 38),
            line(104, 31, 104, 45),  # +
            line(129, 38, 143, 38),  # −
        ),
        "ac-supply": svg(terminals(96, 144), path(f"M 106 {Y} q 7 -12 14 0 t 14 0")),
        "heater": svg(
            leads(80, 160),
            rect(80, Y - 14, 80, 28),
            line(100, Y - 14, 100, Y + 14),
            line(120, Y - 14, 120, Y + 14),
            line(140, Y - 14, 140, Y + 14),
        ),
        "motor": meter("M"),
        "generator": meter("G"),
        "loudspeaker": svg(
            leads(108, 132, BASE),
            line(108, BASE, 108, 70),
            line(132, BASE, 132, 70),
            rect(108, 56, 24, 14),
            path("M 108 56 L 94 32 L 146 32 L 132 56"),
        ),
        "microphone": svg(
            leads(106, 134, BASE),
            line(106, BASE, 110, 70),
            line(134, BASE, 130, 70),
            circle(120, 58, 14),
            line(103, 41, 137, 41, ' stroke-width="6"'),
        ),
        "bell": svg(
            leads(108, 132, BASE),
            line(108, BASE, 108, 66),
            line(132, BASE, 132, 66),
            line(98, 66, 142, 66),
            path("M 103 66 A 17 17 0 0 1 137 66"),
        ),
        "earth": svg(
            line(20, 40, 220, 40),
            line(120, 40, 120, 66),
            line(98, 66, 142, 66),
            line(106, 78, 134, 78),
            line(114, 90, 126, 90),
        ),
        "transformer": svg(
            coil(92, 1),
            coil(142, 0),
            line(113, 24, 113, 96),
            line(121, 24, 121, 96),
            line(40, 30, 92, 30),
            line(40, 90, 92, 90),
            line(142, 30, 200, 30),
            line(142, 90, 200, 90),
        ),
    }


# Key: (answer, other accepted answers, notes), in the order in which the cards
# are introduced: the first fourteen are AQA's list.
CARDS = {
    "cell": ("cell", [], "The longer line is the positive terminal."),
    "battery": (
        "battery",
        ["battery of cells"],
        "Two or more cells joined together. The dashed line means that there can "
        "be more cells in between; it is sometimes drawn as a solid line.",
    ),
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
        "sometimes drawn inside a circle.",
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
        "sometimes drawn inside a circle.",
    ),
    "lamp": (
        "lamp",
        ["bulb", "light bulb", "filament lamp"],
        "Gives out light when a current flows through it.",
    ),
    "fuse": (
        "fuse",
        ["circuit breaker"],
        "Melts, breaking the circuit, if the current becomes too large. A circuit "
        "breaker, which does the same job but can be reset, has the same symbol.",
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
    "junction": (
        "junction",
        [
            "junction of conductors",
            "junction of wires",
            "joined wires",
            "wires joined",
            "connected wires",
            "T-junction",
        ],
        "The dot shows that the wires are joined.",
    ),
    "crossing-wires": (
        "wires crossing with no connection",
        [
            "crossing wires",
            "wires crossing",
            "conductors crossing",
            "conductors crossing with no connection",
            "wires crossing, not joined",
            "wires not joined",
            "not joined",
            "no connection",
        ],
        "Wires that cross without a dot are not joined.",
    ),
    "dc-supply": (
        "d.c. power supply",
        [
            "dc power supply",
            "d.c. supply",
            "dc supply",
            "direct current power supply",
            "direct current supply",
            "power supply (d.c.)",
            "positive and negative terminals",
        ],
        "A supply of direct current, which flows one way only, out of the positive "
        "(+) terminal and round the circuit to the negative (−) one.",
    ),
    "ac-supply": (
        "a.c. power supply",
        [
            "ac power supply",
            "a.c. supply",
            "ac supply",
            "alternating current power supply",
            "alternating current supply",
            "power supply (a.c.)",
        ],
        "A supply of alternating current, which changes direction many times a "
        "second (50 times a second for the mains in the UK).",
    ),
    "heater": (
        "heater",
        ["heating element", "electric heater"],
        "Transfers energy to its surroundings by heating them.",
    ),
    "motor": (
        "motor",
        ["electric motor"],
        "Turns when a current flows through it.",
    ),
    "generator": (
        "generator",
        ["dynamo"],
        "Produces a potential difference (voltage) when it is turned.",
    ),
    "loudspeaker": (
        "loudspeaker",
        ["speaker"],
        "Turns electrical signals into sound.",
    ),
    "microphone": (
        "microphone",
        ["mic"],
        "Turns sound into electrical signals.",
    ),
    "bell": (
        "electric bell",
        ["bell"],
        "Rings when a current flows through it.",
    ),
    "earth": (
        "earth",
        ["ground", "earth or ground", "earth connection"],
        "A connection to the ground, which keeps a metal case safe to touch if a "
        "fault makes it live.",
    ),
    "transformer": (
        "transformer",
        ["step-up transformer", "step-down transformer"],
        "Two coils wound on an iron core. It changes the size of an alternating "
        "potential difference (voltage): up, in a step-up transformer, or down, in "
        "a step-down one.",
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
                "description": "The circuit symbols of GCSE Physics.",
                "public": True,
                "reference": (
                    "In a circuit diagram, wires are drawn as straight lines. A dot "
                    "marks where wires are joined; wires that cross without a dot "
                    "are not joined. These are the symbols of Pearson's (Edexcel) "
                    "specification and WJEC's; AQA's are among them."
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
