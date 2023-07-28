import os
import json
from typing import Union, Any
from datetime import timedelta
from redis import from_url, exceptions
from exceptions.custom_execption import ServerErrorException
from dotenv import load_dotenv
load_dotenv()


redis = from_url(os.getenv("REDIS_HOST"), ssl_cert_reqs=None)


DEFAULT_CACHE_TIME_XXLARGE = timedelta(hours=1)

DEFAULT_CACHE_TIME_XLARGE = timedelta(minutes=30)

DEFAULT_CACHE_TIME_LARGE = timedelta(minutes=3)

DEFAULT_CACHE_TIME_SMALL = timedelta(seconds=20)






class RedisCache():
    def __init__(self, key:str):

        self.key = key

    def get_cache(self) -> Union[Any, None]:

        try:

            cache = redis.get(self.key)

            if cache:
                return json.loads(cache)
            
            return None
        
        except exceptions.RedisError as e:
            raise ServerErrorException(str(e))
        
        except Exception as e:
            raise ServerErrorException(str(e))
            

    def set_cache(self, data=None, expire:Union[float, timedelta]=None):        
        try:

            redis.set(self.key, json.dumps(data), expire)
            
        except exceptions.RedisError as e:
            raise ServerErrorException(str(e))
        
        except Exception as e:
            raise ServerErrorException(str(e))
        
    def delete_cache(self):
        try:

            redis.delete(self.key)
        
        except exceptions.RedisError as e:

            raise ServerErrorException(str(e))

        






        


