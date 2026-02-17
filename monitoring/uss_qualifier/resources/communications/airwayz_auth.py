from typing import Optional
import requests
from implicitdict import ImplicitDict
from monitoring.monitorlib.auth import AuthAdapter


class AirwayzAuthAdapter(AuthAdapter):
    """Custom auth adapter for Airwayz registration-based authentication"""
    
    _token: Optional[str] = None
    
    def __init__(self, register_url: str, api_key: str, uss_id: str):
        """Initialize with registration credentials.
        
        Args:
            register_url: URL for registration endpoint (e.g., http://localhost:5000/v2.1/register)
            api_key: API key for registration
            uss_id: USS ID for registration
        """
        super().__init__()
        self.register_url = register_url
        self.api_key = api_key
        self.uss_id = uss_id
        self._register()
    
    def _register(self):
        """Call /v2.1/register to get authentication token"""
        try:
            response = requests.post(
                self.register_url,
                json={
                    "apiKey": self.api_key,
                    "ussId": self.uss_id
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            AirwayzAuthAdapter._token = result.get('token')
            if not AirwayzAuthAdapter._token:
                raise ValueError("Registration did not return a token")
        except Exception as e:
            raise ValueError(f"Failed to register with Airwayz: {e}")
    
    def issue_token(self, intended_audience: str, scopes: list[str]) -> str:
        """Return the token obtained from registration"""
        if not AirwayzAuthAdapter._token:
            self._register()
        return AirwayzAuthAdapter._token

