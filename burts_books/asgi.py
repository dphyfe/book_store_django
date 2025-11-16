"""
ASGI config for burts_books project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")

application = get_asgi_application()
