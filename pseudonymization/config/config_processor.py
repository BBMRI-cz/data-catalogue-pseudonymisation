import os
import requests

class ConfigProcessor:
    def __init__(self):
        self.pseudo_api = os.getenv("PSEUDONYMIZATION_API")
        self.export_api = os.getenv("EXPORT_API")

        if not self.pseudo_api or not self.export_api:
            raise RuntimeError(
                "Missing required environment variables: "
                "PSEUDONYMIZATION_API and/or EXPORT_API"
            )
        self._check_health(self.pseudo_api)
        self._check_health(self.export_api)

    def _check_health(self, base_url: str):
        url = f"{base_url.rstrip('/')}/health"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Health check failed for {base_url}: {e}")

    def get_pseudo_API(self):
        return self.pseudo_api

    def get_export_API(self):
        return self.export_api
