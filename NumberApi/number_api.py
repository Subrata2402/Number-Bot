import aiohttp, asyncio, json, requests, bs4

class NumberApi(object):
    def __init__(self):
        self.access_code = "AUTOBUYOTP"
        self.host_one = "https://autobuyotp.com/sms/sms.php"
        self.host_two = "https://autobuyotp.com/sms/sms2.php"
        self.host_three = "https://autobuyotp.com/sms/amz.php"
    
    async def fetch(self, method = "GET", function = "", headers = None, data = None):
        async with aiohttp.ClientSession() as session:
            response = await session.request(method = method, url = self.host_two + function, headers = headers, data = data)
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

    async def get_history(self):
        r = requests.get("https://autobuyotp.com/server/history.php?accessCode=" + self.access_code)
        soup = bs4.BeautifulSoup(r.text , "html.parser")
        response = soup.find_all("tr")
        history = [data.text.split("\n") for data in response]
        history.remove(history[0])
        return history

    async def get_balance(self):
        r = requests.get("https://autobuyotp.com/server/history.php?accessCode=" + self.access_code)
        soup = bs4.BeautifulSoup(r.text , "html.parser")
        response = soup.find("font").text
        s = response.find("Total")
        balance = response[:s]
        otps = response[s:]
        return balance, otps
        
