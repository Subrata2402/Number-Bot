import aiohttp, asyncio

class BaseHQApi:
    def __init__(self, access_code: str = None):
        self.access_code = access_code
        
    
 