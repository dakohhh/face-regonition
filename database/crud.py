from typing import List, Type, Union
from mongoengine import Document
from .schema import Users
from exceptions.custom_execption import ServerErrorException





async def fetchone_document(klass:Type[Document], *args, **kwargs)-> Union[Users, None]:
    try:
        return klass.objects.get(*args, **kwargs)
    
    except klass.DoesNotExist:
        return None
    
    except Exception as e:
        raise ServerErrorException(str(e))
    


async def fetchall_documents(klass:Type[Document], *args, **kwargs)-> List[Users]:

    try:
        return klass.objects(*args, **kwargs)
    
    except klass.DoesNotExist:
        return klass.objects(*args, **kwargs)
    
    except Exception as e:
        raise ServerErrorException(str(e))