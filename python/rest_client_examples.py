"""
Exemples d'utilisation du RestClient
"""
from rest_client import RestClient, AuthMode


def exemple_basic_auth():
    """Exemple avec Basic Auth"""
    print("=== Exemple Basic Auth ===")
    
    # Créer le client avec Basic Auth
    client = RestClient(
        base_url="https://api.example.com",
        auth_mode=AuthMode.BASIC,
        username="mon_utilisateur",
        password="mon_mot_de_passe"
    )
    
    try:
        # GET request
        users = client.get("/users")
        print(f"Users récupérés: {users}")
        
        # POST request
        new_user = client.post(
            "/users",
            json={
                "name": "Jean Dupont",
                "email": "jean@example.com"
            }
        )
        print(f"Nouvel utilisateur créé: {new_user}")
        
        # PUT request
        updated_user = client.put(
            "/users/123",
            json={
                "name": "Jean Dupont Modifié"
            }
        )
        print(f"Utilisateur modifié: {updated_user}")
        
        # DELETE request
        result = client.delete("/users/123")
        print(f"Utilisateur supprimé: {result}")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        client.close()


def exemple_jwt():
    """Exemple avec JWT"""
    print("\n=== Exemple JWT ===")
    
    # Créer le client avec JWT
    client = RestClient(
        base_url="https://api.example.com",
        auth_mode=AuthMode.JWT,
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    try:
        # GET avec paramètres
        products = client.get(
            "/products",
            params={"category": "electronics", "limit": 10}
        )
        print(f"Produits récupérés: {products}")
        
        # Mettre à jour le token si nécessaire
        client.set_token("nouveau_token_jwt...")
        
        # Continuer à faire des requêtes avec le nouveau token
        orders = client.get("/orders")
        print(f"Commandes récupérées: {orders}")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        client.close()


def exemple_context_manager():
    """Exemple avec context manager (recommandé)"""
    print("\n=== Exemple avec Context Manager ===")
    
    # Utilisation avec 'with' - fermeture automatique de la session
    with RestClient(
        base_url="https://api.example.com",
        auth_mode=AuthMode.JWT,
        token="mon_token_jwt"
    ) as client:
        try:
            # La session sera automatiquement fermée à la fin du bloc
            data = client.get("/data")
            print(f"Données récupérées: {data}")
        except Exception as e:
            print(f"Erreur: {e}")


def exemple_sans_auth():
    """Exemple sans authentification"""
    print("\n=== Exemple sans authentification ===")
    
    with RestClient(
        base_url="http://localhost:52773/csp/mcp",
        auth_mode=AuthMode.NONE
    ) as client:
        try:
            # Appel à une API publique
            response = client.get("/irisversion")
            print(f"Version IRIS: {response}")
        except Exception as e:
            print(f"Erreur: {e}")


def exemple_headers_personnalises():
    """Exemple avec headers personnalisés"""
    print("\n=== Exemple avec headers personnalisés ===")
    
    with RestClient(
        base_url="https://api.example.com",
        auth_mode=AuthMode.JWT,
        token="mon_token"
    ) as client:
        try:
            # Ajouter des headers personnalisés pour une requête spécifique
            response = client.get(
                "/data",
                headers={
                    "X-Custom-Header": "valeur",
                    "Accept-Language": "fr-FR"
                }
            )
            print(f"Réponse: {response}")
        except Exception as e:
            print(f"Erreur: {e}")


def exemple_gestion_erreurs():
    """Exemple de gestion d'erreurs"""
    print("\n=== Exemple gestion d'erreurs ===")
    
    with RestClient(
        base_url="https://api.example.com",
        auth_mode=AuthMode.BASIC,
        username="user",
        password="pass"
    ) as client:
        try:
            # Tentative d'accès à une ressource qui n'existe pas
            response = client.get("/endpoint-qui-nexiste-pas")
        except requests.HTTPError as e:
            # Gestion des erreurs HTTP (404, 500, etc.)
            print(f"Erreur HTTP: {e}")
            if e.response.status_code == 404:
                print("Ressource non trouvée")
            elif e.response.status_code == 401:
                print("Non autorisé - vérifier les credentials")
        except Exception as e:
            # Autres erreurs (réseau, timeout, etc.)
            print(f"Erreur générale: {e}")


if __name__ == "__main__":
    # Décommenter les exemples que vous voulez tester
    
    # exemple_basic_auth()
    # exemple_jwt()
    # exemple_context_manager()
    exemple_sans_auth()
    # exemple_headers_personnalises()
    # exemple_gestion_erreurs()
