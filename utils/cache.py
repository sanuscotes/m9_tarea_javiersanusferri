# Importación de la librería Flask-Caching
from flask_caching import Cache

# Instancia global del sistema de cache
cache = Cache()

# Función de inicialización del cache
def init_cache(app, config):
    """
    Inicializa el sistema de cache para la aplicación Flask.

    Parámetros
    ----------
    app : Flask
        Instancia de la aplicación Flask sobre la que se aplicará el sistema de cache.

    config : Config
        Clase de configuración que contiene los parámetros necesarios para configurar el cache.

    Funcionamiento
    --------------
    Esta función conecta la instancia de cache creada anteriormente con la aplicación Flask 
    y establece sus parámetros de funcionamiento.
    """
    cache.init_app(app, config={
        "CACHE_TYPE": config.CACHE_TYPE,
        "CACHE_DEFAULT_TIMEOUT": config.CACHE_DEFAULT_TIMEOUT
    })