import aiohttp, asyncio

class BaseHQApi:
    def __init__(self, access_code: str = None):
        self.access_code = access_code
        self.host = "https://autobuyotp.com/sms/sms2.php"
    
    async def fetch(self, method = "GET", function = "", headers = None, data = None):
        async with aiohttp.ClientSession() as session:
            response = await session.request(method = method, url = self.host + function, headers = headers, data = data)
            content = await response.json()
            error = content.get("error")
            if error:
                raise error
            return content

    async def get_number(self, service):
        return await self.fetch("GET", "?act=getnumber&service={}&accessCode={}".format(service, self.access_code))