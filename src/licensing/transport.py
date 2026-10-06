"""License-only BaseCore transport retaining JSON:API error bodies.

BaseCore.request discards non-2xx bodies and runs scraper challenge handlers.
Use its managed curl session directly here so licensing can interpret Keygen
errors without logging response bodies or executing website challenges.
Retries and deadlines are owned by LicenseClient.
"""
from base_api import BaseCore
from base_api.modules.config import RuntimeConfig


class LicensingCore(BaseCore):
    def __init__(self):
        configuration = RuntimeConfig()
        configuration.verify_ssl = True
        configuration.trust_env = False
        configuration.cookies = None
        configuration.request_attempts = 1
        super().__init__(configuration=configuration)

    async def request(self, url, *, method="GET", headers=None, json_data=None,
                      timeout=(5, 20), allow_redirects=False, retry_non_idempotent=False):
        self.initialize_session()
        return await self.session.request(
            method=method, url=url, headers=headers, json=json_data,
            timeout=timeout, allow_redirects=False, verify=True,
        )
