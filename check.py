"""Checks every bundle in this repository (each folder holding a cards.yaml) by
importing it, with django-flashdeck, into a throwaway database, and writes each as
a zip file in dist/, ready to upload to a site (Flashcards → Import and export).

    uv run python check.py
"""

import sys
import tempfile
import zipfile
from pathlib import Path

import django
from django.conf import settings

ROOT = Path(__file__).resolve().parent


def set_up(media):
    settings.configure(
        SECRET_KEY="check",
        USE_TZ=True,
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "modelcluster",
            "flashdeck",
        ],
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        MEDIA_ROOT=media,
    )
    django.setup()
    from django.core.management import call_command

    call_command("migrate", verbosity=0)


def write_zip(bundle, path):
    """The bundle's cards.yaml and images (not its generator)."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        out.write(bundle / "cards.yaml", "cards.yaml")
        for file in sorted((bundle / "images").rglob("*")):
            if file.is_file():
                out.write(file, file.relative_to(bundle).as_posix())


def main():
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    failed = False
    with tempfile.TemporaryDirectory() as media:
        set_up(media)
        from flashdeck.bundles import BundleError, import_bundle

        for bundle in sorted(path.parent for path in ROOT.glob("*/cards.yaml")):
            try:
                counts = import_bundle(bundle)
            except BundleError as error:
                print(f"{bundle.name}: {error}")
                failed = True
                continue
            write_zip(bundle, dist / f"{bundle.name}.zip")
            summary = ", ".join(f"{n} {what}" for what, n in counts.items())
            print(f"{bundle.name}: {summary}; dist/{bundle.name}.zip")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
