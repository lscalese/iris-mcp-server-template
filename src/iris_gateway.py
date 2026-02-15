import httpx
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class IRISConfig:
    """Configuration pour la connexion à IRIS"""
    base_url: str
    username: str
    password: str
    namespace: str = "USER"


class IRISGateway:
    """Gateway pour abstraire les appels REST vers IRIS"""
    
    def __init__(self, config: IRISConfig):
        self.config = config
        self.base_url = config.base_url.rstrip('/')
        self.auth = (config.username, config.password)
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def get_version(self) -> str:
        """Récupère la version d'IRIS"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/atelier/v1/%25SYS/version",
                auth=self.auth,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data["result"]["content"]["version"]
    
    async def _get(self, path: str) -> Any:
        """Méthode utilitaire pour effectuer des requêtes GET"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{path}",
                auth=self.auth,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def _post(self, path: str, data: Optional[dict] = None) -> Any:
        """Méthode utilitaire pour effectuer des requêtes POST"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{path}",
                auth=self.auth,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
