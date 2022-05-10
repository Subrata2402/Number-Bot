import aiohttp, asyncio, json

class NumberApi(object):
    def __init__(self):
        self.access_code = ""
        self.host = "https://autobuyotp.com/sms/sms2.php"
    
    async def fetch(self, method = "GET", function = "", headers = None, data = None):
        async with aiohttp.ClientSession() as session:
            response = await session.request(method = method, url = self.host + function, headers = headers, data = data)
            content = await response.text()
            return json.loads(content)

    async def get_number(self, service):
        return await self.fetch("GET", "?act=getnumber&service={}&accessCode={}".format(service, self.access_code))
        
    async def get_sms(self, activation_id):
        return await self.fetch("GET", "?act=getotp&id={}&accessCode={}".format(activation_id, self.access_code))
        
    async def cancel_order(self, activation_id):
        return await self.fetch("GET", "?act=cancel&id={}".format(activation_id))
        
    async def get_message_history(self, activation_id):
        return await self.fetch("GET", "?act=otp&number={}".format(activation_id))
