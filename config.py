TOKEN = 'NzIzMzkwNjc5MDEwNzcwOTg4.Xuw_rg.LHztjaErBQiO1q_cgIt22f-IYEI'

EMOJI = [":⚰️"," 💣 ", "🧨 ", '🧠']
INFO = "\n 🦉 " \
       "Что делает бот? С сайта https://db.chgk.info/ запрашивает случайный пакет вопросов в соотвествие" \
       " с настройкми, затем при переходе в режим игры выдаёт из этого пакета"\
       "вопросы в общий чат. Считает количество правильных и неправильных ответов и "\
       "выводит результат сессии после отыгранного пакета. \n\n"\
       "Какие есть команды? Прежде всего любую команду бота нужно начинать с '..'. Список команд\n"\
       "1. Получение данных о текущих настройках - 'get settings'. Значения параметров \n"\
       "\t limit - количество вопросов в пакете (от 0 до 100)\n"\
       "\t complexity - сложность вопросов в пакете ( от 0 до 5)\n"\
       " Далее настройка временного интервала вопросов\n"\
       "\t from_date[day] - (от 1 до 31)\n"\
       "\tfrom_date[month] - (от 1 до 12)\n"\
       "\tfrom_date[year] -  (от 1990 до текущего)\n"\
       "\tto_date[day] - (до текущего)\n"\
       "\tto_date[month] - (до текущего)\n"\
       "\tto_date[year] - (до текущего)\n"\
       "2. Изменение настроек - 'set settings'. Пример : .. set settings complexity 2 limit 10\n"\
       "3. Переход в режим игры - 'start'.\n"\
       "4. Получение следующего вопроса - 'next' .\n"\
       "5. Правильный ответ - + .\n"\
       "6. Правильный ответ - + .\n"\
       "7. Текущая статистка - 'stat'\n"\
       "8. Сброс текущего пакета - 'reset\n\n\n"\
       "Чтобы создать сессию, привязанную к данному каналу, введите любую команду из вышеперечисленных\n"\
       "Перед тем, как запросить новый пакет вопрос, нужно сбросить текущий командой .. reset\n\n"\
       "Найденные ошибки, пожелания, предложения писать на почту kuzinmails@yandex.ru\n 🦉 Приятной игры! 🦉 "
#await message.channel.send("limit {0}, complexity {1}, from {2}.{3}.{4} to {5}.{6}.{7}".
                  #                     format(self.session_settings[l]))
print(INFO)