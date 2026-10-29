"""Feature-focused workflows used by the interactive CLI."""

from .accounts import handle_account_auth
from .downloads import handle_download_single, handle_resume_paused, handle_scrape_profile
from .models import handle_batch_management
from .settings import handle_license_management, handle_settings
from .statistics import handle_statistics_dashboard

__all__ = [
    "handle_account_auth",
    "handle_batch_management",
    "handle_download_single",
    "handle_license_management",
    "handle_resume_paused",
    "handle_scrape_profile",
    "handle_settings",
    "handle_statistics_dashboard",
]
