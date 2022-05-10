import aiohttp, asyncio

class NumberApi(object):
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
        
    async def get_sms(self, activation_id):
        return await self.fetch("GET", "?act=getotp&id={}&accessCode={}".format(activation_id, self.access_code))
        
    async def cancel_order(self, activation_id):
        return await self.fetch("GET", "?act=cancel&id={}".format(activation_id))
        
    async def get_message_history(self, activation_id):
        return await self.fetch("GET", "?act=otp&number={}".format(activation_id))