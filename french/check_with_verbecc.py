"""Compares the French verbs bundle (cards.yaml) with the conjugations of verbecc,
a second source (whose tables come from Verbiste), in both directions: every model
answer should be one of verbecc's forms, and every verbecc form an accepted
answer. verbecc has no forms for falloir (only "-"), so its cards are reported.

    uv run --with verbecc python french/check_with_verbecc.py french/cards.yaml
"""

import logging
import re
import sys

import yaml
from verbecc import CompleteConjugator
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang

logging.disable(logging.WARNING)

TENSES = {
    "present": ("indicatif", "présent"),
    "passe-compose": ("indicatif", "passé-composé"),
    "imparfait": ("indicatif", "imparfait"),
    "futur": ("indicatif", "futur-simple"),
    "conditionnel": ("conditionnel", "présent"),
    "subjonctif": ("subjonctif", "présent"),
    "imperatif": ("imperatif", "imperatif-présent"),
}
SLOTS = {
    ("1", "s"): 0,
    ("2", "s"): 1,
    ("3", "s"): 2,
    ("1", "p"): 3,
    ("2", "p"): 4,
    ("3", "p"): 5,
}
IMPERATIVE_SLOTS = {("2", "s"): 0, ("1", "p"): 1, ("2", "p"): 2}
PRONOUN = re.compile(
    r"^(?:que |qu')?(?:je |j'|tu |il |elle |on |nous |vous |ils |elles )"
)


def plain(text):
    return " ".join(text.replace("’", "'").split())


def main(path):
    data = yaml.safe_load(open(path, encoding="utf-8"))
    conjugator = CompleteConjugator(Lang("fr"))
    cache = {}
    problems = checked = 0
    for deck in data["decks"]:
        mood, tense = TENSES[deck["slug"]]
        slots = IMPERATIVE_SLOTS if deck["slug"] == "imperatif" else SLOTS
        for card in deck["cards"]:
            infinitive = card["prompt"].split(" (")[0]
            if infinitive not in cache:
                result = conjugator.conjugate(infinitive).get_data()
                if result["verb"]["predicted"]:
                    print(f"NOTE {infinitive}: not in verbecc's tables (predicted)")
                cache[infinitive] = {
                    str(m): {str(t): v for t, v in ts.items()}
                    for m, ts in result["moods"].items()
                }
            theirs = [set() for _ in range(6)]
            for entry in cache[infinitive][mood][tense]:
                slot = slots.get((str(entry["p"].value), str(entry["n"].value)))
                if slot is None:
                    continue
                for form in entry["c"]:
                    theirs[slot].add(PRONOUN.sub("", plain(form)))
            for i, answer in enumerate(card["answers"]):
                if len(card["answers"]) == 1:
                    i = 2  # an impersonal verb's only form: il
                checked += 1
                ours = {plain(answer["text"])} | {
                    plain(a) for a in answer.get("alternatives", [])
                }
                where = f"{deck['slug']:14} {infinitive:10} {answer['label']:14}"
                if plain(answer["text"]) not in theirs[i]:
                    problems += 1
                    print(
                        f"DIFFERENT {where} ours {answer['text']!r}, verbecc {sorted(theirs[i])}"
                    )
                missing = theirs[i] - ours
                if missing:
                    problems += 1
                    print(f"MISSING   {where} verbecc also has {sorted(missing)}")
    print(f"{checked} answers checked, {problems} differences")


if __name__ == "__main__":
    main(sys.argv[1])
