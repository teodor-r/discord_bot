import discord
import asyncio
import base_parser as prs
import game_session as gs
import config

current_guilds = {}
current_channels  = {}
global_status = True

prs.Parser.read_requests_patterns("chgkbase_requests.txt")
prs.Parser.print_headers(prs.requests_patterns['Home_req']['Headers'])
print("Templates of the requests have been loaded")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    prs.Parser.global_session = await init_session()
@client.event
async def on_guild_join(guild):
    print("here")
    for channel in guild.channels:
        if channel.name == "основной" or channel.name=="general":
            await channel.send(config.INFO)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.channel.type) != "text":
        return

    channel = message.channel
    guild_id = message.channel.guild
    messages = message.content.split(" ")

    if messages[0].strip().startswith('..'):
        if len(messages)==1:
            await message.channel.send("Вводите команды через пробел ");


        elif messages[1] == "info":
            await message.channel.send(config.INFO)

        elif channel.id in current_channels.keys():
            handle_message_task = asyncio.create_task(gs.GameSession.handle_message(self = current_channels[channel.id],
                                                              messages=messages, message = message))

            await handle_message_task


        elif not (guild_id in current_guilds.keys()):
            await channel.send("Создаю новую игровую сессию...")
            current_guilds.update({guild_id: 1})
            new_session = gs.GameSession()
            new_session.channel = channel
            current_channels.update({channel.id: new_session})
            await channel.send("Сессия успешно создана! Поиграем? 😉 \nВведите .. start")

        elif (guild_id in current_guilds.keys()):
            await message.channel.send("Создаю новую игровую сессию...")
            if current_guilds[guild_id] <3:
                current_guilds[guild_id]+=1
                new_session = gs.GameSession()
                new_session.channel = message.channel
                current_channels.update({channel.id: new_session})
                await channel.send("Сессия успешно создана! Поиграем? 😉 \nВведите .. start")
            else:
                await(channel.send("Превышен лимит уникальный сессий на одном сервере 🎮"))


async def  init_session():
    parser = prs.Parser
    session = await parser.create_session()
    prs.Parser.global_session = session
    task =   asyncio.create_task(parser.send_request(prs.requests_patterns["Home_req"],
                                    parser.global_session))

    home_page = await task
    print(home_page)
    #print(await home_page.text(encoding='utf-8'))
    task = asyncio.create_task(parser.send_request(prs.requests_patterns["random_packet"],
                                    session))

    pack_response = await task
    print(pack_response)
    print("************************")
    if home_page.status == 200 and pack_response.status == 200:
        global global_status
        print('Удалось подключиться к базе вопросов')
        global_status = False
    else:
        print('Не удалось подключиться к базе вопросов')
        global_status = True

    #print(await pack_response.text())
    #print(await pack_response.text(encoding='utf-8'))
    return session


client.run(config.TOKEN)




