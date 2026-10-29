"""License-only BaseCore transport retaining JSON:API error bodies.

BaseCore.request discards non-2xx bodies and runs scraper challenge handlers.
Use its managed curl session directly here so licensing can interpret Keygen
errors without logging response bodies or executing website challenges.
Retries and deadlines are owned by LicenseClient.
"""
from src.shared.service_transport import ServiceCore


class LicensingCore(ServiceCore):
    """Retries and error interpretation remain owned by LicenseClient."""
