"""Writes cards.yaml, beside this script: a flashdeck bundle of 32 common irregular
French verbs in seven tenses, with one deck per tense.

The forms are built from each verb's présent, past participle, auxiliary and future
stem by the usual rules, with the exceptions listed below.

    uv run python decks/french/make_verbs.py
    uv run python manage.py flashdeck_import decks/french
"""

import re
import unicodedata
from pathlib import Path

from flashdeck.manifest import dump_manifest

# Infinitive: English, présent (je to ils), past participle, auxiliary, future stem.
VERBS = {
    "être": ("to be", "suis es est sommes êtes sont", "été", "avoir", "ser"),
    "avoir": ("to have", "ai as a avons avez ont", "eu", "avoir", "aur"),
    "aller": ("to go", "vais vas va allons allez vont", "allé", "être", "ir"),
    "faire": (
        "to do, to make",
        "fais fais fait faisons faites font",
        "fait",
        "avoir",
        "fer",
    ),
    "dire": ("to say", "dis dis dit disons dites disent", "dit", "avoir", "dir"),
    "pouvoir": (
        "to be able to",
        "peux peux peut pouvons pouvez peuvent",
        "pu",
        "avoir",
        "pourr",
    ),
    "vouloir": (
        "to want",
        "veux veux veut voulons voulez veulent",
        "voulu",
        "avoir",
        "voudr",
    ),
    "savoir": (
        "to know (a fact)",
        "sais sais sait savons savez savent",
        "su",
        "avoir",
        "saur",
    ),
    "devoir": (
        "to have to, to owe",
        "dois dois doit devons devez doivent",
        "dû",
        "avoir",
        "devr",
    ),
    "venir": (
        "to come",
        "viens viens vient venons venez viennent",
        "venu",
        "être",
        "viendr",
    ),
    "tenir": (
        "to hold",
        "tiens tiens tient tenons tenez tiennent",
        "tenu",
        "avoir",
        "tiendr",
    ),
    "prendre": (
        "to take",
        "prends prends prend prenons prenez prennent",
        "pris",
        "avoir",
        "prendr",
    ),
    "mettre": (
        "to put",
        "mets mets met mettons mettez mettent",
        "mis",
        "avoir",
        "mettr",
    ),
    "voir": ("to see", "vois vois voit voyons voyez voient", "vu", "avoir", "verr"),
    "croire": (
        "to believe",
        "crois crois croit croyons croyez croient",
        "cru",
        "avoir",
        "croir",
    ),
    "boire": ("to drink", "bois bois boit buvons buvez boivent", "bu", "avoir", "boir"),
    "connaître": (
        "to know (be acquainted with)",
        "connais connais connaît connaissons connaissez connaissent",
        "connu",
        "avoir",
        "connaîtr",
    ),
    "vivre": ("to live", "vis vis vit vivons vivez vivent", "vécu", "avoir", "vivr"),
    "suivre": (
        "to follow",
        "suis suis suit suivons suivez suivent",
        "suivi",
        "avoir",
        "suivr",
    ),
    "écrire": (
        "to write",
        "écris écris écrit écrivons écrivez écrivent",
        "écrit",
        "avoir",
        "écrir",
    ),
    "lire": ("to read", "lis lis lit lisons lisez lisent", "lu", "avoir", "lir"),
    "ouvrir": (
        "to open",
        "ouvre ouvres ouvre ouvrons ouvrez ouvrent",
        "ouvert",
        "avoir",
        "ouvrir",
    ),
    "partir": (
        "to leave",
        "pars pars part partons partez partent",
        "parti",
        "être",
        "partir",
    ),
    "sortir": (
        "to go out",
        "sors sors sort sortons sortez sortent",
        "sorti",
        "être",
        "sortir",
    ),
    "dormir": (
        "to sleep",
        "dors dors dort dormons dormez dorment",
        "dormi",
        "avoir",
        "dormir",
    ),
    "courir": (
        "to run",
        "cours cours court courons courez courent",
        "couru",
        "avoir",
        "courr",
    ),
    "mourir": (
        "to die",
        "meurs meurs meurt mourons mourez meurent",
        "mort",
        "être",
        "mourr",
    ),
    "recevoir": (
        "to receive",
        "reçois reçois reçoit recevons recevez reçoivent",
        "reçu",
        "avoir",
        "recevr",
    ),
    "envoyer": (
        "to send",
        "envoie envoies envoie envoyons envoyez envoient",
        "envoyé",
        "avoir",
        "enverr",
    ),
    "conduire": (
        "to drive",
        "conduis conduis conduit conduisons conduisez conduisent",
        "conduit",
        "avoir",
        "conduir",
    ),
    "naître": (
        "to be born",
        "nais nais naît naissons naissez naissent",
        "né",
        "être",
        "naîtr",
    ),
    "rire": ("to laugh", "ris ris rit rions riez rient", "ri", "avoir", "rir"),
}

# Exceptions to the rules.
SUBJONCTIF = {
    "être": "sois sois soit soyons soyez soient",
    "avoir": "aie aies ait ayons ayez aient",
    "aller": "aille ailles aille allions alliez aillent",
    "faire": "fasse fasses fasse fassions fassiez fassent",
    "pouvoir": "puisse puisses puisse puissions puissiez puissent",
    "vouloir": "veuille veuilles veuille voulions vouliez veuillent",
    "savoir": "sache saches sache sachions sachiez sachent",
}
IMPERATIF = {
    "être": "sois soyons soyez",
    "avoir": "aie ayons ayez",
    "savoir": "sache sachons sachez",
    "vouloir": "veuille veuillons veuillez",
}
NO_IMPERATIF = {"pouvoir", "devoir", "naître"}  # none, or not in use
IMPARFAIT_STEM = {"être": "ét"}
# Other forms of the présent that are also right: je puis is the formal form of je
# peux, which survives in puis-je.
PRESENT_ALTERNATIVES = {"pouvoir": [["puis"], [], [], [], [], []]}

PERSONS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
ENDINGS = {
    "imparfait": "ais ais ait ions iez aient".split(),
    "futur": "ai as a ons ez ont".split(),
    "subjonctif": "e es e ions iez ent".split(),
}
AUXILIARY = {"avoir": VERBS["avoir"][1].split(), "être": VERBS["être"][1].split()}
ELIDES = re.compile(r"[aeiouyhâàéèêîôû]")

DECKS = [
    ("present", "présent"),
    ("passe-compose", "passé composé"),
    ("imparfait", "imparfait"),
    ("futur", "futur simple"),
    ("conditionnel", "conditionnel présent"),
    ("subjonctif", "subjonctif présent"),
    ("imperatif", "impératif"),
]


def labels(forms, subjunctive=False):
    out = []
    for i, form in enumerate(forms):
        person = "j’" if i == 0 and ELIDES.match(form) else PERSONS[i]
        if subjunctive:
            person = f"qu’{person}" if person.startswith("il") else f"que {person}"
        out.append(person)
    return out


def answers(forms, subjunctive=False, alternatives=None):
    out = []
    for i, (label, form) in enumerate(
        zip(labels(forms, subjunctive), forms, strict=True)
    ):
        entry = {"label": label, "text": form}
        alts = list(alternatives[i]) if alternatives else []
        # The 1990 spelling reform drops the circumflex of connaître and naître.
        if "aît" in form:
            alts.append(form.replace("aît", "ait"))
        if alts:
            entry["alternatives"] = alts
        out.append(entry)
    return out


def stem_note(verb, stem):
    if stem == verb:
        return f"Stem: the infinitive, {stem}-."
    if stem == verb[:-1]:
        return f"Stem: the infinitive without its final e, {stem}-."
    return f"Stem: {stem}- (irregular)."


def tenses(verb):
    english, present, participle, auxiliary, future = VERBS[verb]
    present = present.split()
    nous_stem = present[3].removesuffix("ons")
    imparfait_stem = IMPARFAIT_STEM.get(verb, nous_stem)
    imparfait = [imparfait_stem + e for e in ENDINGS["imparfait"]]

    yield "present", answers(present, alternatives=PRESENT_ALTERNATIVES.get(verb)), ""

    aux = AUXILIARY[auxiliary]
    if auxiliary == "avoir":
        compound = [f"{a} {participle}" for a in aux]
        yield (
            "passe-compose",
            answers(compound),
            f"Auxiliary: avoir; past participle: {participle}.",
        )
    else:
        p = participle
        singular = [p, [f"{p}e", f"{p}(e)"]]
        plural = [f"{p}s", [f"{p}es", f"{p}(e)s"]]
        polite = [f"{p}s", [f"{p}es", f"{p}(e)s", p, f"{p}e", f"{p}(e)"]]
        shapes = [singular, singular, singular, plural, polite, plural]
        compound = [f"{a} {shape[0]}" for a, shape in zip(aux, shapes, strict=True)]
        alternatives = [
            [f"{a} {x}" for x in shape[1]] for a, shape in zip(aux, shapes, strict=True)
        ]
        note = (
            f"Auxiliary: être; past participle: {participle}, which agrees with the "
            "subject (vous may be one person)."
        )
        yield "passe-compose", answers(compound, alternatives=alternatives), note

    if verb in IMPARFAIT_STEM:
        note = f"Stem: {imparfait_stem}- (the one exception to the rule)."
    else:
        note = f"Stem: {imparfait_stem}-, from nous {present[3]} in the présent."
    yield "imparfait", answers(imparfait), note

    note = stem_note(verb, future)
    yield "futur", answers([future + e for e in ENDINGS["futur"]]), note
    conditionnel = [future + e for e in ENDINGS["imparfait"]]
    yield (
        "conditionnel",
        answers(conditionnel),
        f"{note} The endings are those of the imparfait.",
    )

    if verb in SUBJONCTIF:
        subjonctif, note = SUBJONCTIF[verb].split(), "Irregular."
    else:
        stem = present[5].removesuffix("ent")
        subjonctif = [stem + e for e in ENDINGS["subjonctif"]]
        subjonctif[3:5] = imparfait[3:5]
        note = (
            f"Stem: {stem}-, from ils {present[5]}; nous and vous as in the imparfait."
        )
    yield "subjonctif", answers(subjonctif, subjunctive=True), note

    if verb in NO_IMPERATIF:
        return
    if verb in IMPERATIF:
        imperatif, note = IMPERATIF[verb].split(), "Irregular."
    else:
        tu = present[1]
        note = ""
        if tu.endswith("es") or tu == "vas":
            tu, note = tu[:-1], "No -s in the tu form, as for -er verbs."
        imperatif = [tu, present[3], present[4]]
    entries = answers(imperatif)
    for entry, person in zip(entries, ["(tu)", "(nous)", "(vous)"], strict=True):
        entry["label"] = person
    yield "imperatif", entries, note


def key(verb):
    decomposed = unicodedata.normalize("NFD", verb)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def italic_list(words):
    words = [f"*{w}*" for w in words]
    return ", ".join(words[:-1]) + " and " + words[-1]


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


SUBJECT_REFERENCE = """\
*Je* becomes *j’* before a vowel or a mute h (*j’ai*, *j’habite*), and *que*
becomes *qu’* before *il*, *elle* and *on* (*qu’il soit*).

Search the index for any form, such as *serais* or *aille*, to find its verb."""


def references():
    """Each tense's rule, with the exceptions taken from the tables above."""
    etre_verbs = [verb for verb, data in VERBS.items() if data[3] == "être"]
    future = [
        (f"*{verb}*", f"*{data[4]}-*")
        for verb, data in VERBS.items()
        if data[4] not in (verb, verb[:-1])
    ]
    subjonctif = [
        (f"*{verb}*", f"*{forms.split()[0]}*", f"*{forms.split()[3]}*")
        for verb, forms in SUBJONCTIF.items()
    ]
    return {
        "present": """\
The endings are usually -s, -s, -t, -ons, -ez, -ent (*je dors, il dort*).
*Pouvoir* and *vouloir* take -x, -x, -t (*je peux*); *ouvrir* takes -e, -es, -e,
as -er verbs such as *envoyer* do (*j’ouvre, j’envoie*); and *prendre* keeps its d
(*il prend*). Many of these verbs have one stem for nous and vous and another for
the other persons (*venir*: *je viens, ils viennent*, but *nous venons*). *Être*,
*avoir*, *aller* and *faire* are the most irregular, and *vous dites* and *vous
faites* end in -tes.""",
        "passe-compose": f"""\
The présent of *avoir* or *être*, followed by the past participle (*j’ai pris*,
*je suis venu*). Of these verbs, {italic_list(etre_verbs)} take *être*, and
their past participle agrees with the subject like an adjective (*elle est
partie*, *nous sommes allés*). With *avoir*, the past participle does not agree
with the subject.""",
        "imparfait": """\
The stem is the nous form of the présent without -ons (*nous buvons* → *buv-*),
and the endings are -ais, -ais, -ait, -ions, -iez, -aient. The one exception is
*être*, whose stem is *ét-* (*j’étais*). A stem ending in i or y keeps it before
-ions and -iez (*nous riions*, *nous voyions*).""",
        "futur": """\
The stem is the infinitive, without the final e of a verb in -re (*dormir-*,
*prendr-*), and the endings are -ai, -as, -a, -ons, -ez, -ont. Every stem ends in
r, including the irregular ones:

"""
        + table(["verb", "stem"], future),
        "conditionnel": """\
The stem of the futur simple with the endings of the imparfait: -ais, -ais, -ait,
-ions, -iez, -aient (*je serais*, *nous irions*).""",
        "subjonctif": """\
For je, tu, il and ils, the stem is the ils form of the présent without -ent (*ils
prennent* → *prenn-*), with the endings -e, -es, -e, -ent; nous and vous are as in
the imparfait (*nous prenions*). The irregular ones:

"""
        + table(["verb", "que je", "que nous"], subjonctif),
        "imperatif": """\
The tu, nous and vous forms of the présent, without their pronouns (*prends,
prenons, prenez*). A tu form in -es loses its s, as does *tu vas* (*ouvre*,
*envoie*, *va*). *Être*, *avoir*, *savoir* and *vouloir* take forms like those of
the subjonctif (*sois*, *aie*, *sache*, *veuille*). *Pouvoir* has no impératif,
and those of *devoir* and *naître* are not in use.""",
    }


def bundle():
    decks = {slug: [] for slug, _ in DECKS}
    tense_references = references()
    names = dict(DECKS)
    for verb in VERBS:
        english = VERBS[verb][0]
        for slug, entries, note in tenses(verb):
            card = {
                "key": key(verb),
                "prompt": f"{verb} ({english})\n{names[slug]}",
                "answers": entries,
            }
            if note:
                card["notes"] = note
            decks[slug].append(card)
    return {
        "format": "flashdeck/1",
        "subject": {
            "slug": "french",
            "title": "French",
            "language": "fr",
            "characters": "à â ç é è ê ë î ï ô ù û œ",
            "reference": SUBJECT_REFERENCE,
        },
        "decks": [
            {
                "slug": slug,
                "title": f"Irregular verbs: {name}",
                "public": False,
                "reference": tense_references[slug],
                "cards": decks[slug],
            }
            for slug, name in DECKS
        ],
    }


if __name__ == "__main__":
    path = Path(__file__).with_name("cards.yaml")
    text = dump_manifest(bundle())
    path.write_text(
        "# Generated by make_verbs.py: change that script, not this file.\n" + text,
        encoding="utf-8",
    )
    print(f"Wrote {path}")
