import time
import json
import copy
import memory_test as mt
from bs4 import BeautifulSoup
import  base_parser as prs
import asyncio
default_settings = {"limit": 10, "complexity": 3,
                    "from_date[day]": 1,
                    "from_date[month]": 1,
                    "from_date[year]": 1990,
                    "to_date[day]": 19,
                    "to_date[month]": 6,
                    "to_date[year]": 2020,
                    "op": "Получить пакет",
                    "form_build_id": "form-HV9cl-hkXg1JCmx30gSZ5D0iSxIWtRNjy5bK7QIjaFs",
                    "form_id": "chgk_db_get_random_form"}

class GameSession(object):
    __slots__ = ['session_settings', 'channel', 'questions', 'questions',
                 'setting_flag','in_play','current_question','right_answer',
                 'wrong_answer','answer_is_hidden','getting_settings_last_message_id']
    def __init__(self):
        self.session_settings = copy.deepcopy(default_settings)
        self.channel = None
        self.questions = []
        self.setting_flag = True
        self.in_play = False
        self.current_question = 0
        self.right_answer = 0
        self.wrong_answer = 0
        self.answer_is_hidden = True
        self.getting_settings_last_message_id = None
    async def check_settings(self):
        pass

    async def handle_message(self,messages:dict, message):
        print("Handle message from channel {}".format(self.channel.id))
        start = time.time()
        if messages[1].strip() == "set" and messages[2].strip() == "settings":
            if len(messages) != 3:
                for i in range(3, len(messages), 2):
                    key = messages[i]
                    if (self.session_settings.get(key) != None):
                        self.session_settings[key] = messages[i + 1]
                    else:
                        await message.channel.send("Нет параметра запроса")
                self.check_settings()
            else:
                    await message.channel.send("Настройки не введены")

            #здесь должны быть проверка на корректность настроек
            await message.channel.send("Настройки успешно изменены")

        elif messages[1].strip() == "get" and messages[2].strip() == "settings":
            await message.channel.send("Лимит вопросов {}, сложность {}, временой интервал: {}.{}.{} - {}.{}.{} ⚙️"
                                    .format(self.session_settings["limit"],self.session_settings["complexity"],
                                            self.session_settings["from_date[day]"],self.session_settings["from_date[month]"],self.session_settings["from_date[year]"],
                                            self.session_settings["to_date[day]"],self.session_settings["to_date[month]"], self.session_settings["to_date[year]"]))

        elif messages[1].strip() == "start":
            if self.in_play != True:
                self.questions.clear()
                get_packet_task = asyncio.create_task(prs.Parser.send_request(requst=prs.requests_patterns['random_packet']
                                                     , session=prs.Parser.global_session
                                                     , data= self.session_settings))
                resp = await get_packet_task
                if resp.status == 200:
                    async def parse_request_packet():
                            print("Parse request packet in  channel {}".format(self.channel.id))
                            soup = BeautifulSoup(await resp.text(), 'html.parser')
                            for foo in soup.find_all('div', attrs={'class': 'random-results'}):
                                for bar in foo.find_all('div', attrs={'class': 'random_question'}):
                                    item = {"question": "", "answer": ""}
                                    img_tag = bar.find('img')
                                    if img_tag != None:
                                        img_path = img_tag['src']
                                        item["question"] += img_path + '\n'

                                    num_split = bar.get_text().find('Ответ')
                                    text = bar.get_text()
                                    item["question"] += text[0:num_split]
                                    item["answer"] += text[num_split:]

                                    print(item)

                                    self.questions.append(item)
                    parse_request_task = asyncio.create_task(parse_request_packet())
                    await  parse_request_task

                    self.in_play = True
                    await message.channel.send('Запрос успешно обработан 👍')
                    await message.channel.send(self.questions[self.current_question]["question"])
                else:
                    await message.channel.send('Не удаётся подключиться к ресурсу. Код ошибки {}.'
                                               '  Проверьте настройки запроса'.format(resp.status))
            else:
                await message.channel.send('Чтобы запросить новый пакет, сбросьте текущий, написав .. reset')
        elif messages[1].strip() == "reset":
            if self.in_play:
                self.current_question = 0
                self.right_answer = 0;
                self.wrong_answer = 0
                self.questions.clear()
                self.in_play = False
                await message.channel.send('Пакет сброшен\n'
                                           'Верных ответов {0}, неверных {1} 📜'.format(self.right_answer, self.wrong_answer))
            else:
                await message.channel.send('Пакет и так был пуст')
        elif messages[1].strip() == "stat":
            await message.channel.send('Верных ответов {0}, неверных {1} 📜'.format(self.right_answer, self.wrong_answer))

        elif messages[1].strip() == "answer" and self.in_play and self.answer_is_hidden:
            await message.channel.send(self.questions[self.current_question]["answer"])
            await message.channel.send('+  ответ верен, - не верен')
            self.answer_is_hidden = False
        elif messages[1].strip() == "+" and self.in_play and self.answer_is_hidden != True:
            self.right_answer += 1
            await message.channel.send("Cчётчик обновлён 🎲")
        elif messages[1].strip() == "-" and self.in_play and self.answer_is_hidden != True:
            self.wrong_answer += 1
            await message.channel.send("Cчётчик обновлён 🎲")
        elif messages[1].strip() == "next" and self.in_play:
            self.answer_is_hidden = True
            if self.current_question < len(self.questions) - 1:
                self.current_question += 1
                await message.channel.send(self.questions[self.current_question]["question"])
            else:
                await message.channel.send("Закончились вопросы. Поищем новые ? 🔍 Для сброса пакета"
                                           "введите .. reset")
        end = time.time()
        print("Handling message from channel {} took {} seconds".format(self.channel.id, end-start))


gs = GameSession()
mt.dump(gs)
print ("GameSession object memory is {} bytes".format(mt.get_size(gs)))
