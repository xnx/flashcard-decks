"""The deck of exercises on the pronouns y and en and the neuter le, for the French
bundle that make_french.py writes.

Each card is a sentence to rewrite with pronouns in place of the words in brackets,
so the choice between y, en and le is part of the exercise. The cards are written
here in three groups, one for each pronoun, and shuffled into a fixed random order
in the deck, since the app shows new cards in the order of the bundle.
"""

import random

INSTRUCTION = "Rewrite the sentence with pronouns for the words in brackets."
SEED = 20261121  # fixes the order of the cards; change it only to reshuffle them

# Key (which must not change, as progress is kept by it), sentence, answer, note.
# The note, plain text, is shown after the card is answered. Written with straight
# apostrophes and a space before ! and ?, which typeset() makes French.
Y = [
    (
        "gare",
        "Je vais [à la gare] tous les matins.",
        "J'y vais tous les matins.",
        "Y replaces a place introduced by à.",
    ),
    (
        "ecosse",
        "Elle habite [en Écosse] depuis dix ans.",
        "Elle y habite depuis dix ans.",
        "Y also replaces a place after en, dans, sur or chez.",
    ),
    (
        "chez-paul",
        "Nous dînons [chez Paul] ce soir.",
        "Nous y dînons ce soir.",
        "Chez Paul is a place (Paul's home), so y.",
    ),
    (
        "vacances",
        "Je pense souvent [à mes vacances].",
        "J'y pense souvent.",
        "Penser à + a thing gives y; for a person, penser à lui or à elle.",
    ),
    (
        "politique",
        "Elle s'intéresse [à la politique].",
        "Elle s'y intéresse.",
        "Y comes after the reflexive pronoun.",
    ),
    (
        "message",
        "Il a répondu [à mon message].",
        "Il y a répondu.",
        "Répondre à + a thing gives y; for a person, lui (il lui a répondu).",
    ),
    (
        "marche",
        "Nous sommes allés [au marché] samedi.",
        "Nous y sommes allés samedi.",
        "Y comes before the auxiliary. The past participle agrees with the subject, "
        "as aller takes être, never with y.",
    ),
    (
        "acheter-du-pain",
        "Tu as pensé [à acheter du pain] ?",
        "Tu y as pensé ?",
        "Y can replace à + an infinitive.",
    ),
    (
        "poste",
        "Je dois aller [à la poste] cet après-midi.",
        "Je dois y aller cet après-midi.",
        "Y comes before the infinitive that it belongs to.",
    ),
    (
        "climat",
        "Il s'est habitué [au climat].",
        "Il s'y est habitué.",
        "The reflexive pronoun, then y, then the auxiliary.",
    ),
    (
        "aeroport",
        "Je t'emmène [à l'aéroport].",
        "Je t'y emmène.",
        "Me, te, se, nous and vous come before y.",
    ),
    (
        "cles-tiroir",
        "Il a mis [les clés] [dans le tiroir].",
        "Il les y a mises.",
        "Les comes before y, and the past participle agrees with les (les clés, "
        "feminine plural).",
    ),
    (
        "lyon",
        "J'irai [à Lyon] demain.",
        "J'irai demain.",
        "Y is dropped before the future and conditional of aller (irai, irais…): "
        "not j'y irai.",
    ),
    (
        "piscine",
        "Je ne vais pas [à la piscine] aujourd'hui.",
        "Je n'y vais pas aujourd'hui.",
        "Ne comes before y, as n'y.",
    ),
    (
        "italie",
        "Ils ne sont pas retournés [en Italie].",
        "Ils n'y sont pas retournés.",
        "Ne … pas goes around y and the auxiliary.",
    ),
    (
        "echecs",
        "Je ne veux pas jouer [aux échecs] ce soir.",
        "Je ne veux pas y jouer ce soir.",
        "Jouer à + a game gives y. The negation goes around the modal verb, and y "
        "before the infinitive.",
    ),
    (
        "vie-en-ville",
        "Elle ne s'est jamais habituée [à la vie en ville].",
        "Elle ne s'y est jamais habituée.",
        "The past participle agrees with s' (elle), the direct object.",
    ),
    (
        "qu-il-vienne",
        "Je ne m'attendais pas [à ce qu'il vienne].",
        "Je ne m'y attendais pas.",
        "Y can replace à ce que + a clause.",
    ),
    (
        "boulangerie",
        "Va [à la boulangerie] !",
        "Vas-y !",
        "In an affirmative imperative the pronoun follows the verb, with a hyphen, "
        "and va takes back its s before y.",
    ),
    (
        "fete",
        "Ne va pas [à cette fête] !",
        "N'y va pas !",
        "In a negative imperative the pronoun comes before the verb.",
    ),
]

EN = [
    (
        "pain",
        "Je voudrais [du pain].",
        "J'en voudrais.",
        "En replaces a partitive: du, de la or des + a noun.",
    ),
    (
        "avoir-gagne",
        "Elle est contente [d'avoir gagné].",
        "Elle en est contente.",
        "An adjective + de + an infinitive gives en. Compare ils sont contents → ils "
        "le sont.",
    ),
    (
        "trois-freres",
        "J'ai [trois frères].",
        "J'en ai trois.",
        "With a number, en replaces the noun, and the number stays after the verb.",
    ),
    (
        "amis",
        "Nous avons [beaucoup d'amis] ici.",
        "Nous en avons beaucoup ici.",
        "So does an adverb of quantity, such as beaucoup, peu or assez.",
    ),
    (
        "pommes",
        "Il a acheté [un kilo de pommes].",
        "Il en a acheté un kilo.",
        "The quantity stays after the verb, and the past participle never agrees with "
        "en.",
    ),
    (
        "livre",
        "Tu as besoin [de ce livre] ?",
        "Tu en as besoin ?",
        "Avoir besoin de + a thing gives en; for a person, de lui or d'elle.",
    ),
    (
        "travail",
        "Elle parle souvent [de son travail].",
        "Elle en parle souvent.",
        "Parler de + a thing gives en.",
    ),
    (
        "il-pleuvait",
        "Je me souviens [qu'il pleuvait].",
        "Je m'en souviens.",
        "Se souvenir takes de, so a clause after it gives en too. Compare je sais "
        "qu'il pleuvait → je le sais.",
    ),
    (
        "marseille",
        "Ils reviennent [de Marseille].",
        "Ils en reviennent.",
        "En replaces a place introduced by de (where from).",
    ),
    (
        "bureau",
        "Elle est sortie [du bureau] à six heures.",
        "Elle en est sortie à six heures.",
        "En comes before the auxiliary.",
    ),
    (
        "oeufs",
        "Il y a [des œufs] dans le frigo.",
        "Il y en a dans le frigo.",
        "Y comes before en: il y en a.",
    ),
    (
        "il-viendra",
        "Je suis sûr [qu'il viendra].",
        "J'en suis sûr.",
        "Être sûr takes de, so a clause after it gives en too, even though it begins "
        "with que.",
    ),
    (
        "chocolats",
        "Il a offert [des chocolats] [à sa mère].",
        "Il lui en a offert.",
        "Lui comes before en.",
    ),
    (
        "voiture",
        "Je n'ai pas [de voiture].",
        "Je n'en ai pas.",
        "Pas de + a noun gives en.",
    ),
    (
        "viande",
        "Il n'a pas mangé [de viande].",
        "Il n'en a pas mangé.",
        "Ne … pas goes around en and the auxiliary.",
    ),
    (
        "rendez-vous",
        "Il ne s'est pas souvenu [de son rendez-vous].",
        "Il ne s'en est pas souvenu.",
        "The reflexive pronoun, then en, then the auxiliary.",
    ),
    (
        "lait",
        "Il n'y a plus [de lait].",
        "Il n'y en a plus.",
        "Ne … plus works like ne … pas.",
    ),
    (
        "probleme",
        "Je ne veux pas parler [de ce problème].",
        "Je ne veux pas en parler.",
        "The negation goes around the modal verb, and en before the infinitive.",
    ),
    (
        "soupe",
        "Mange [de la soupe] !",
        "Manges-en !",
        "In an affirmative imperative, the tu form of an -er verb takes back its s "
        "before en or y.",
    ),
    (
        "bonbons",
        "N'achète pas [de bonbons] !",
        "N'en achète pas !",
        "In a negative imperative the pronoun comes before the verb.",
    ),
]

LE = [
    (
        "fatiguee",
        "Elle est [fatiguée].",
        "Elle l'est.",
        "The neuter le replaces an adjective, and never changes: not la.",
    ),
    (
        "contents",
        "Ils sont [contents].",
        "Ils le sont.",
        "Not les. Compare elle est contente d'avoir gagné → elle en est contente.",
    ),
    (
        "medecin",
        "Mon frère est [médecin].",
        "Mon frère l'est.",
        "Le replaces a noun used without an article after être.",
    ),
    (
        "avocate",
        "Elle deviendra [avocate].",
        "Elle le deviendra.",
        "As after être, so after devenir, sembler and paraître.",
    ),
    (
        "il-est-parti",
        "Je sais [qu'il est parti].",
        "Je le sais.",
        "Le replaces a whole clause that is the direct object.",
    ),
    (
        "elle-a-raison",
        "Je crois [qu'elle a raison].",
        "Je le crois.",
        "Croire que gives le; j'y crois means I believe in it.",
    ),
    (
        "beau-temps",
        "J'espère [qu'il fera beau].",
        "Je l'espère.",
        "Le becomes l' before a vowel or a mute h.",
    ),
    (
        "promettre-de-venir",
        "Je te promets [de venir].",
        "Je te le promets.",
        "Promettre takes de + an infinitive as its direct object, so le, not en. Te "
        "comes before le.",
    ),
    (
        "il-viendrait",
        "Elle m'a dit [qu'il viendrait].",
        "Elle me l'a dit.",
        "Me comes before le.",
    ),
    (
        "elle-etait-partie",
        "J'ai appris [qu'elle était partie].",
        "Je l'ai appris.",
        "The past participle never agrees with the neuter le. Compare cette nouvelle, "
        "je l'ai apprise.",
    ),
    (
        "demissionner",
        "Elle a décidé [de démissionner].",
        "Elle l'a décidé.",
        "Décider de + an infinitive is a direct object, so le, not en, and décidé "
        "does not agree.",
    ),
    (
        "malade",
        "Il a été [malade] la semaine dernière.",
        "Il l'a été la semaine dernière.",
        "Le comes before the auxiliary.",
    ),
    (
        "prete",
        "Elle n'est pas [prête].",
        "Elle ne l'est pas.",
        "Ne comes before le, as ne l'.",
    ),
    (
        "il-etait-malade",
        "Je ne savais pas [qu'il était malade].",
        "Je ne le savais pas.",
        "Ne … pas goes around le and the verb.",
    ),
    (
        "il-pleuve",
        "Je ne pense pas [qu'il pleuve].",
        "Je ne le pense pas.",
        "The clause after je ne pense pas takes the subjonctif (qu'il pleuve).",
    ),
    (
        "riches",
        "Elles n'ont jamais été [riches].",
        "Elles ne l'ont jamais été.",
        "Still le, though elles and riches are feminine plural.",
    ),
    (
        "il-partait",
        "Il ne m'a pas dit [qu'il partait].",
        "Il ne me l'a pas dit.",
        "Ne … pas goes around me l' and the auxiliary.",
    ),
    (
        "ce-que-tu-penses",
        "Dis-moi [ce que tu penses].",
        "Dis-le-moi.",
        "In an affirmative imperative, le comes before moi, with hyphens.",
    ),
    (
        "je-suis-ici",
        "Ne dis à personne [que je suis ici].",
        "Ne le dis à personne.",
        "In a negative imperative the pronoun comes before the verb.",
    ),
    (
        "en-retard",
        "Je vais lui expliquer [pourquoi je suis en retard].",
        "Je vais le lui expliquer.",
        "Le comes before lui, and both come before the infinitive.",
    ),
]

REFERENCE = """\
*Y* replaces a place (*à la gare*, *en Écosse*, *chez Paul*), and a thing, an
infinitive or a clause introduced by *à* (*penser à ses vacances*, *penser à acheter
du pain*, *s'attendre à ce qu'il vienne*). *En* replaces a partitive (*du pain*,
*pas de voiture*); a noun after a number or a quantity, which stays after the verb
(*j'en ai trois*, *il en a acheté un kilo*); a place introduced by *de* (*revenir de
Marseille*); and a thing, an infinitive or a clause after a verb or an adjective
that takes *de* (*parler de son travail*, *être contente d'avoir gagné*, *se
souvenir qu'il pleuvait*, *être sûr qu'il viendra*). The neuter *le* replaces an
adjective, or a noun without an article, after *être*, *devenir*, *sembler* or
*paraître* (*elle l'est*, never *la*); and a clause or an infinitive that is the
direct object of its verb (*je le sais*), including *de* + an infinitive after
*promettre*, *décider* and *oublier* (*je te le promets*). For a person, *à* +
the person gives *lui* or *leur*, and *de* + the person usually gives *de lui* or
*d'elle*, not *y* or *en*.

The pronoun comes before the conjugated verb (*j'y vais*), before the auxiliary in
the passé composé (*il en a acheté*), and before the infinitive that it belongs to
(*je dois y aller*). *Ne* comes before the pronoun, and *pas* after the verb or the
auxiliary (*je n'y suis pas allé*). In an affirmative imperative the pronoun follows
the verb, with a hyphen (*vas-y*, *dis-le-moi*), and *va* and the tu form of an -er
verb take back their s before *y* and *en* (*manges-en*); in a negative imperative it
comes before the verb (*n'y va pas*). *Y* is dropped before the future and
conditional of *aller* (*j'irai*, not *j'y irai*).

With other pronouns, the order is *me*, *te*, *se*, *nous*, *vous*; then *le*,
*la*, *les*; then *lui*, *leur*; then *y*; then *en* (*je t'y emmène*, *il les y a
mises*, *il lui en a offert*, *il y en a*). A past participle with *avoir* agrees
with a direct object that comes before it (*il les y a mises*), but never with *y*,
*en* or the neuter *le* (*il en a acheté un kilo*, *je l'ai appris*)."""


def typeset(text):
    """French apostrophes, and a narrow no-break space before ! and ?."""
    return text.replace("'", "’").replace(" !", " !").replace(" ?", " ?")


def deck():
    cards = [
        {
            "key": key,
            "prompt": f"{typeset(sentence)}\n{INSTRUCTION}",
            "answers": [{"text": typeset(answer)}],
            "notes": typeset(note),
        }
        for key, sentence, answer, note in Y + EN + LE
    ]
    keys = [card["key"] for card in cards]
    if len(set(keys)) != len(keys):
        raise ValueError("Two pronoun cards share a key")
    random.Random(SEED).shuffle(cards)
    return {
        "slug": "pronouns",
        "title": "Pronouns: y, en and le",
        "public": False,
        "reference": typeset(REFERENCE),
        "cards": cards,
    }
