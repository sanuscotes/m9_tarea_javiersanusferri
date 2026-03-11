from flask_caching import Cache

cache = Cache()

def init_cache(app, config):
    cache.init_app(app, config={
        "CACHE_TYPE": config.CACHE_TYPE,
        "CACHE_DEFAULT_TIMEOUT": config.CACHE_DEFAULT_TIMEOUT
    })