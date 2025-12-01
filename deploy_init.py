"""Deployment initialization script for Burt's Books."""

import os
import sys

import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()


def check_database() -> bool:
    """Verify that the database connection is available."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"✗ Database connection failed: {exc}")
        return False


def run_migrations() -> None:
    """Apply all database migrations."""
    print("📦 Running database migrations...")
    call_command("migrate", interactive=False)
    print("✓ Migrations complete")


def load_sample_catalog() -> None:
    """Load the bundled catalog data."""
    print("📚 Loading sample catalog...")
    try:
        call_command("load_sample_data")
        print("✓ Catalog ready")
    except Exception as exc:  # noqa: BLE001
        print(f"⚠ Unable to load sample catalog: {exc}")


def collect_static() -> None:
    """Collect static assets for production."""
    print("🎨 Collecting static files...")
    call_command("collectstatic", interactive=False, verbosity=0)
    print("✓ Static files collected")


def main() -> None:
    print("=" * 60)
    print("📚 Burt's Books - Deployment Initialization")
    print("=" * 60)

    if not check_database():
        sys.exit(1)

    try:
        run_migrations()
        load_sample_catalog()
        collect_static()
    except Exception as exc:  # noqa: BLE001
        print(f"✗ Deployment failed: {exc}")
        sys.exit(1)

    print("=" * 60)
    print("✅ Initialization complete. Happy reading!")
    print("=" * 60)


if __name__ == "__main__":
    main()
