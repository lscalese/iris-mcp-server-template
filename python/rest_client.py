"""
Client REST réutilisable avec support pour Basic Auth et JWT
"""
import requests
from typing import Optional, Dict, Any
from enum import Enum


class AuthMode(Enum):
    """Modes d'authentification supportés"""
    BASIC = "basic"
    JWT = "jwt"
    NONE = "none"


class RestClient:
    """
    Client REST avec gestion de l'authentification Basic Auth ou JWT
    
    Exemple d'utilisation:
        # Avec Basic Auth
        client = RestClient(
            base_url="https://api.example.com",
            auth_mode=AuthMode.BASIC,
            username="user",
            password="pass"
        )
        
        # Avec JWT
        client = RestClient(
            base_url="https://api.example.com",
            auth_mode=AuthMode.JWT,
            token="your-jwt-token"
        )
        
        # Faire un appel
        response = client.get("/endpoint")
    """
    
    def __init__(
        self,
        base_url: str,
        auth_mode: AuthMode = AuthMode.NONE,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialise le client REST
        
        Args:
            base_url: URL de base de l'API (ex: https://api.example.com)
            auth_mode: Mode d'authentification (BASIC, JWT, NONE)
            username: Nom d'utilisateur pour Basic Auth
            password: Mot de passe pour Basic Auth
            token: Token JWT
            verify_ssl: Vérifier les certificats SSL
            timeout: Timeout par défaut pour les requêtes (secondes)
        """
        self.base_url = base_url.rstrip('/')
        self.auth_mode = auth_mode
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configuration de l'authentification
        self._setup_auth()
    
    def _setup_auth(self):
        """Configure l'authentification selon le mode choisi"""
        if self.auth_mode == AuthMode.BASIC:
            if not self.username or not self.password:
                raise ValueError("Username et password requis pour Basic Auth")
            self.session.auth = (self.username, self.password)
        
        elif self.auth_mode == AuthMode.JWT:
            if not self.token:
                raise ValueError("Token requis pour authentification JWT")
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}'
            })
    
    def set_token(self, token: str):
        """
        Met à jour le token JWT
        
        Args:
            token: Nouveau token JWT
        """
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def _build_url(self, endpoint: str) -> str:
        """
        Construit l'URL complète
        
        Args:
            endpoint: Endpoint de l'API (ex: /users)
            
        Returns:
            URL complète
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Gère la réponse HTTP
        
        Args:
            response: Réponse HTTP
            
        Returns:
            Données JSON de la réponse
            
        Raises:
            requests.HTTPError: Si la requête a échoué
        """
        try:
            response.raise_for_status()
            # Retourne le JSON si disponible, sinon le texte
            if response.content:
                try:
                    return response.json()
                except ValueError:
                    return {"text": response.text}
            return {}
        except requests.HTTPError as e:
            # Tente d'extraire le message d'erreur du serveur
            error_msg = str(e)
            try:
                error_data = response.json()
                error_msg = f"{e} - {error_data}"
            except:
                pass
            raise requests.HTTPError(error_msg, response=response)
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectue une requête GET
        
        Args:
            endpoint: Endpoint de l'API
            params: Paramètres de requête
            headers: Headers HTTP additionnels
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse
        """
        url = self._build_url(endpoint)
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            verify=self.verify_ssl,
            timeout=kwargs.get('timeout', self.timeout),
            **{k: v for k, v in kwargs.items() if k != 'timeout'}
        )
        return self._handle_response(response)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectue une requête POST
        
        Args:
            endpoint: Endpoint de l'API
            data: Données à envoyer (form data)
            json: Données JSON à envoyer
            headers: Headers HTTP additionnels
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse
        """
        url = self._build_url(endpoint)
        response = self.session.post(
            url,
            data=data,
            json=json,
            headers=headers,
            verify=self.verify_ssl,
            timeout=kwargs.get('timeout', self.timeout),
            **{k: v for k, v in kwargs.items() if k != 'timeout'}
        )
        return self._handle_response(response)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectue une requête PUT
        
        Args:
            endpoint: Endpoint de l'API
            data: Données à envoyer (form data)
            json: Données JSON à envoyer
            headers: Headers HTTP additionnels
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse
        """
        url = self._build_url(endpoint)
        response = self.session.put(
            url,
            data=data,
            json=json,
            headers=headers,
            verify=self.verify_ssl,
            timeout=kwargs.get('timeout', self.timeout),
            **{k: v for k, v in kwargs.items() if k != 'timeout'}
        )
        return self._handle_response(response)
    
    def patch(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectue une requête PATCH
        
        Args:
            endpoint: Endpoint de l'API
            data: Données à envoyer (form data)
            json: Données JSON à envoyer
            headers: Headers HTTP additionnels
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse
        """
        url = self._build_url(endpoint)
        response = self.session.patch(
            url,
            data=data,
            json=json,
            headers=headers,
            verify=self.verify_ssl,
            timeout=kwargs.get('timeout', self.timeout),
            **{k: v for k, v in kwargs.items() if k != 'timeout'}
        )
        return self._handle_response(response)
    
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectue une requête DELETE
        
        Args:
            endpoint: Endpoint de l'API
            params: Paramètres de requête
            headers: Headers HTTP additionnels
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse
        """
        url = self._build_url(endpoint)
        response = self.session.delete(
            url,
            params=params,
            headers=headers,
            verify=self.verify_ssl,
            timeout=kwargs.get('timeout', self.timeout),
            **{k: v for k, v in kwargs.items() if k != 'timeout'}
        )
        return self._handle_response(response)
    
    def close(self):
        """Ferme la session"""
        self.session.close()
    
    def __enter__(self):
        """Support pour context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support pour context manager"""
        self.close()
