"""Management command to load the sample Burt's Books catalog."""

from typing import Dict

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from populate_books import CATEGORY_LABELS, load_books


class Command(BaseCommand):
    help = "Load the bundled Burt's Books catalog into the database."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Reload the catalog even if books already exist.",
        )

    def handle(self, *args, **options) -> None:
        book_model = apps.get_model("bookstore", "Book")
        force_reload: bool = options.get("force", False)

        try:
            has_books = book_model.objects.exists()
        except OperationalError:
            self.stderr.write(
                self.style.ERROR(
                    "Database tables are missing. Run 'python manage.py migrate' first."
                )
            )
            return

        if has_books and not force_reload:
            self.stdout.write(
                self.style.WARNING(
                    "Book catalog already exists. Use --force to refresh the sample data."
                )
            )
            return

        summary = load_books(delete_existing=force_reload)
        created: int = int(summary.get("created", 0))
        updated: int = int(summary.get("updated", 0))
        duplicates: int = int(summary.get("duplicates", 0))
        total: int = int(summary.get("total", created))
        categories: Dict[str, int] = summary.get("categories", {})

        self.stdout.write(
            self.style.SUCCESS(f"✓ Catalog synchronized ({total} total items).")
        )

        if created:
            self.stdout.write(f"  • Created: {created}")
        if updated:
            self.stdout.write(f"  • Updated: {updated}")
        if duplicates:
            self.stdout.write(f"  • Duplicates encountered: {duplicates}")

        for key, label in CATEGORY_LABELS.items():
            count = categories.get(key, 0)
            self.stdout.write(f"  • {label}: {count}")

        extra_categories = {
            key: value for key, value in categories.items() if key not in CATEGORY_LABELS
        }
        for key, value in extra_categories.items():
            pretty_key = key.replace("_", " ").title()
            self.stdout.write(f"  • {pretty_key}: {value}")
