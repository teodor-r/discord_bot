import aiohttp
import json


requests_patterns = {}

class Parser(object):
    pull_sessions = []
    global_session = None
    pull_proxies = []

    @classmethod
    def print_headers(cls,headers: dict):
        """
        Печатает заголовки запроса в окно вывода
        :param headers: словарь с заголовками
        :return:
        """
        for item in headers:
            print(item + ":" + headers[item])

    @classmethod
    async def create_session(cls):
        session =  aiohttp.ClientSession()
        return session

    @classmethod
    async def send_request(cls,requst:dict, session, data = None):
        print("Send  request in URL  {}".format(requst["Url"]))
        """
        Отправляет все виды http запросов

        :param req: заголовки запроса
        :param session: объект сессии
        :return: возвращает ответ веб-ресурса
        """
        response = None
        if requst["Request"] == "post":
            response = await session.post(url=requst["Url"], data=data, headers=requst["Headers"], ssl=False)
        elif requst["Request"] == "get":
            response = await session.get(url=requst["Url"], headers=requst["Headers"],ssl=False)
        elif requst["Request"] == "head":
            response = await session.head(url=requst["Url"], headers=requst["Headers"], ssl=False)


        return response

    @classmethod
    def read_requests_patterns(cls,filename):
        global requests_patterns
        with open(filename, 'r', encoding='utf-8') as file:
            requests_patterns = json.loads(file.read())

