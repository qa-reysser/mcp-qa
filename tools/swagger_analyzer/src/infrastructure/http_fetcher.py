"""
Implementaciones de infraestructura - Fetcher HTTP
Responsable de obtener contratos desde URLs
"""
import requests
from typing import Optional
from ..domain.interfaces import IContractFetcher


class HttpContractFetcher(IContractFetcher):
    """Implementación de fetcher usando requests para HTTP/HTTPS"""
    
    def __init__(self, timeout: int = 30, verify_ssl: bool = True):
        """
        Inicializa el fetcher HTTP
        
        Args:
            timeout: Tiempo máximo de espera en segundos
            verify_ssl: Si se debe verificar el certificado SSL
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
    
    def fetch(self, url: str) -> str:
        """
        Obtiene el contenido del contrato desde una URL
        
        Args:
            url: URL del contrato Swagger/OpenAPI
            
        Returns:
            Contenido del contrato como string
            
        Raises:
            ValueError: Si la URL no es válida
            requests.RequestException: Si hay un error en la petición HTTP
        """
        if not url or not isinstance(url, str):
            raise ValueError("La URL debe ser una cadena de texto válida")
        
        if not url.startswith(('http://', 'https://')):
            raise ValueError("La URL debe comenzar con http:// o https://")
        
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                headers={'Accept': 'application/json, application/yaml, text/yaml, */*'}
            )
            response.raise_for_status()
            return response.text
        except requests.Timeout:
            raise Exception(f"Timeout al intentar obtener el contrato desde {url}")
        except requests.ConnectionError:
            raise Exception(f"Error de conexión al intentar acceder a {url}")
        except requests.HTTPError as e:
            raise Exception(f"Error HTTP {e.response.status_code}: {e.response.reason}")
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el contrato: {str(e)}")
