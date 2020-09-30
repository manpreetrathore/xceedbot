from dotenv import load_dotenv
from discord.utils import get
import requests
import aiohttp
import discord
import asyncio
import json
import random
import os
import urllib.request
import commandhelp
import quotesystem
import customcommands
import errors
from datetime import datetime
from libneko import pag
from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from datetime import datetime
bot=commands.Bot(command_prefix="!")
mge=['Ello, gov\'nor!',
    'Top of the mornin’ to ya!',
    'What’s crackin\' ? ',
    'GOOOOOD MORNING!',
    'Sup, homeslice?',
    'Howdy, howdy ,howdy! 🤠',
    'How does a lion greet the other animals in the field? A: Pleased to eat you.',
    'I\'m Batman. 🦇',
    'I\'m Captain Marvel. 🦸‍♀️‍',
    'Avengers!! Assemble.🦸‍♂️ ',
    'At least, we meet for the first time for the last time!',
    'Hello, who\'s there, I\'m talking.',
    'Here\'s Johnny!',
    'You know who this is.',
    'Ghostbusters, whatya want?',
    'Yo!',
    'Whaddup.',
    'Greetings and salutations!',
    'Peek-a-boo! 👻',
    'Put that 🍪 down!',
    'Ahoy, matey!',
    'Hiya!',
    'Wacch ya doing? You just brightened up my day! ✨',
    'Bella Ciao',
    'Hello! There is my pumpkin! I miiiissed you 😄'
    ]
with open('config.json', 'r') as f:
    config = json.load(f)
initial_extensions = ['cogs.geet','cogs.random']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


with open('logins.json', 'r') as f:
    logins = json.load(f)

with open('servers.json', 'r') as f:
    servers = json.load(f)
load_dotenv()
TOKEN = open("token.txt", "r").read()
defaultprefix = config['prefix']
botownerid = config['botownerid']
#discordtoken = logins['discordtoken']
client = discord.Client()


@bot.event
async def on_ready():

    print(f'\nLogged as: {bot.user.name} - {bot.user.id}')
    # # await bot.change_presence(activity=Game(name=''))
    # rant=random.randint(0,len(config['statuses']))
    # print(config['statuses'][rant])
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Game(type=-1, name=config['statuses'][rant]))
    print(f'Bot ready on {len(servers)} server(s).')
    print(f'Bot is ready to go!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to Help"))
    await random_status_change()
bot.remove_command('help')
def community_report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline

def make_pages(text, page_length=2000):
    pages = []

    for i in range(0, len(text), page_length):
        pages.append(text[i:i+page_length])

    return pages
# @bot.command(paginate)
async def paginate(ctx,msg,channel,title):
    rant = random.randint(0, 0xffffff)
    if len(msg)<996:
        embeds = [
        # discord.Embed(title="Help", description="Command Description", color=rant),
        discord.Embed(title=title, description=msg[:996], color=rant).set_thumbnail(url=bot.user.avatar_url),


        #discord.Embed(title="test page 2", description=dummy_text[1000:2000], color=0x5599ff),
        #discord.Embed(title="test page 3", description=dummy_text[2000:3000], color=0x191638),

        ]
    elif len(msg)>=996 and len(msg)<1996:
        embeds = [
        #discord.Embed(title="Help", description="Command Description", color=rant),

        discord.Embed(title=title, description=msg[:996], color=rant).set_thumbnail(url=bot.user.avatar_url).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[996:1996], color=rant).set_thumbnail(url=bot.user.avatar_url),

        #discord.Embed(title="test page 3", description=dummy_text[2000:3000], color=0x191638),

        ]
    elif len(msg)>=2000 and len(msg)<3000:
        embeds = [
        # discord.Embed(title="Help", description="Command Description", color=rant),

        discord.Embed(title=title, description=msg[:996], color=rant).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[996:1996], color=rant).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[1996:2996], color=rant).set_thumbnail(url=bot.user.avatar_url),

        ]
    elif len(msg)>=3000 and len(msg)<4000:
        embeds = [
        # discord.Embed(title="Help", description="Command Description", color=rant),

        discord.Embed(title=title, description=msg[:996], color=rant).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[996:1996], color=rant).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[1996:2996], color=rant).set_thumbnail(url=bot.user.avatar_url),
        discord.Embed(title=title, description=msg[2996:3996], color=rant).set_thumbnail(url=bot.user.avatar_url)
        ]
    paginator = BotEmbedPaginator(ctx,embeds)
    await paginator.run(channel=channel)
def add_server_to_config(serverid, servername, serverownerid, prefix):
    print('Adding server to servers.json...')
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    serverjsondata  = { "servername": servername,
                        "serverownerid": serverownerid,
                        "prefix": prefix,
                        "disabledcommands": ["8ball", "tf"],
                        "modrolename": "Moderator",
                        "adminrolename": "Admin",
                        "quotes": [] }

    servers[f'sid{serverid}'] = serverjsondata

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def update_server_config(serverid, servername, serverownerid):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        server = servers[f'sid{serverid}']
    except KeyError:
        # server config missing
        add_server_to_config(serverid, servername, serverownerid, defaultprefix)
        return

    server['servername'] = servername
    server['serverownerid'] = serverownerid

    servers[f'sid{serverid}'] = server

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def set_default_prefix(prefix):
    global defaultprefix

    with open('config.json', 'r') as f:
        config = json.load(f)

    config['prefix'] = prefix
    defaultprefix = prefix

    print(f'Set default prefix to {prefix}. Writing to config file...')
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def set_server_prefix(serverid, prefix):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    server = servers[f'sid{serverid}']
    server['prefix'] = prefix
    servers[f'sid{serverid}'] = server

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)
def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check
def set_userlevel_rolenames(serverid, modrolename, adminrolename):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    server = servers[f'sid{serverid}']
    server['modrolename'] = modrolename
    server['adminrolename'] = adminrolename
    servers[f'sid{serverid}'] = server

    print(f'Set ul rolenames to {modrolename} (mod), {adminrolename} (admin)')

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)
def get_userlevel(member, server):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    # there's probably a more efficient way to do this
    roles = []
    for role in member.roles:
        roles.append(str(role))

    if member.id == botownerid:
        return 4
    elif member.id == server.owner.id:
        return 3
    elif servers[f'sid{server.id}']['adminrolename'] in roles:
        return 2
    elif servers[f'sid{server.id}']['modrolename'] in roles:
        return 1
    else:
        return 0
laststatus = 'Listening to Help'
async def random_status_change():
    global laststatus
    statuses = config['statuses']
    timeout = int(config['statustimeout'])

    while True:
        randomnum = random.randint(0, len(statuses) - 1)
        print(f'Now playing: {statuses[randomnum]}')
        if not statuses[randomnum] == laststatus:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=statuses[randomnum]), status=discord.Status.idle)
        laststatus = statuses[randomnum]
        if timeout != 0:
            await asyncio.sleep(timeout)
        else:
            break

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            mse=random.choice(mge)
            rant = random.randint(0, 0xffffff)
            em2=discord.Embed(title=mse, description=f"""Welcome to the server {member.mention}""", color=rant)
            await channel.send_message(embed=em2)

# @bot.event
# async def on_ready():
#     print('Logged in as')
#     print(bot.user.name)
#     print(bot.user.id)
#     print('------')
#ON SERVER JOIN MESSAGE
#@bot.event
#async def on_ready():
#  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

@bot.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    xcd_guild = bot.get_guild(752580094312185927)
    if message.guild == None and not message.author.bot:
        mse=random.choice(mge)
        rant = random.randint(0, 0xffffff)
        em1=discord.Embed(title=mse, description="Commands can only be used in Commands Channel of your server 😐", color=rant,)
        em1.set_author(name="Xceed",
                         icon_url=bot.user.avatar_url,
                         )
        await message.channel.send(embed=em1)
        #em1.set_image(url="https://www.google.com/search?q=google+image&client=firefox-b-d&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjAtNKJ2-3rAhWHzjgGHdfDDSEQ_AUoAXoECA0QAw&biw=766&bih=762#imgrc=tarj9Uj56GD3xM")
        return
    elif message.guild != None:

        update_server_config(message.guild.id, message.guild.name, message.guild.owner.id)

        with open('servers.json', 'r') as f:
            servers = json.load(f)

        disabledcommands = servers[f'sid{message.guild.id}']['disabledcommands']
        prefix = servers[f'sid{message.guild.id}']['prefix']

        usecounter = 0

        try:
            usecounter = int(config['usecounter'])
        except KeyError:
            print('usecounter key is missing from config.json. Setting use counter to 0.')
        if not message.author.bot:
            if message.content.startswith(prefix):
                # Increase use counter in case command is found
                # (If it's not found, it gets decremented again later.)
                usecounter += 1

                args = message.content.split("--")
                print(args)
                if args[0] == f'{prefix}help':
                    commandname = None
                    if len(args) > 1:
                        commandname = args[1]
                    messagestr = commandhelp.get_command_help_string(message.guild.id,
                                                                     get_userlevel(message.author,
                                                                                   message.guild),
                                                                     commandname)
                    author= message.author
                    channel = await author.create_dm()
                    # rant = random.randint(0, 0xffffff)
                    # embed=discord.Embed(title="Help", description="Command Description", color=rant)
                    # embed.set_author(name="Xceed",
                    #                  icon_url=bot.user.avatar_url,
                    #                  )
                    # embed.add_field(name=" Use all Commands with prefix", value=messagestr, inline=False)
                    #
                    # #embed.add_field(name="Novo chalein ?", value="hi2", inline=True)
                    # embed.set_thumbnail(url=bot.user.avatar_url)
                    # await channel.send(embed=embed)
                    mse=random.choice(mge)
                    rant=random.randint(0, 0xffffff)
                    emb1=discord.Embed(title=mse, description=f'Check your PMs : <@{message.author.id}>', color=rant)
                    emb1.set_author(name="Xceed",
                                     icon_url=bot.user.avatar_url,
                                     )
                    mse=random.choice(mge)
                    rant=random.randint(0, 0xffffff)
                    em1=discord.Embed(title=mse, description=f'Use all Commands with prefix and arguments with SEPERATOR', color=rant)
                    em1.set_author(name="Xceed",
                                     icon_url=bot.user.avatar_url,
                                     )

                    ctx = await bot.get_context(message)

                    await  message.channel.send(embed=emb1)
                    await channel.send(embed=em1)
                    title="Help"
                    await message.delete()
                    await paginate(ctx,messagestr,channel,title)

                    # await channel.send(msg)

                elif args[0] == f'{prefix}setprefix':
                        if get_userlevel(message.author, message.guild) == 4:
                            if len(args) > 1:
                                if not args[1].isspace() or args[1] != '':
                                    if len(args) > 2:
                                        if args[2] == 'server':
                                            set_server_prefix(message.guild.id, args[1])
                                            mse=random.choice(mge)
                                            rant = random.randint(0, 0xffffff)
                                            em1=discord.Embed(title=mse, description=f'Set server prefix to {args[1]}', color=rant,)
                                            em1.set_author(name="Xceed",
                                                             icon_url=bot.user.avatar_url,
                                                             )
                                            await message.channel.send(embed=em1)
                                        else:
                                            set_default_prefix(args[1])
                                            mse=random.choice(mge)
                                            rant = random.randint(0, 0xffffff)
                                            em1=discord.Embed(title=mse, description=f'Set default prefix to {args[1]}', color=rant,)
                                            em1.set_author(name="Xceed",
                                                             icon_url=bot.user.avatar_url,
                                                             )
                                            await message.channel.send(embed=em1)
                                    else:
                                        set_default_prefix(args[1])
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=f'Set default prefix to {args[1]}', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await message.channel.send(embed=em1)

                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Prefix cannot be null, whitespace, or empty.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)

                            else:
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description=f'Prefix cannot be null, whitespace, or empty.', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await message.channel.send(embed=em1)

                        elif get_userlevel(message.author, message.guild) > 1:
                            if len(args) > 1:
                                if not args[1].isspace() or args[1] != '':
                                    set_server_prefix(message.guild.id, args[1])
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Set server prefix to {args[1]}', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                            else:
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description=f'Prefix cannot be null, whitespace, or empty.', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await  message.channel.send(embed=em1)
                        else:
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description=f'The {prefix}setprefix command may only be used by ' + \
                                                      'the bot or server owner.', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await  message.channel.send(embed=em1)
                elif args[0] == f'{prefix}toggle':
                    if get_userlevel(message.author, message.guild) >= 1:
                        if len(args) > 1:
                            print (f'Disabled Commands for {message.guild.name}: {disabledcommands}')
                            if args[1] not in disabledcommands:
                                print (f'{args[1]} is enabled. Disabling it.')

                                if args[1] != 'enable' and args[1] != 'disable' \
                                   and args[1] != 'setprefix' and args[1] != 'help':
                                    disabledcommands.append(args[1])
                                    print (f'New disabled command array: {disabledcommands}')

                                    servers[f'sid{message.guild.id}']['disabledcommands'] = disabledcommands

                                    with open('servers.json', 'w') as f:
                                        json.dump(servers, f, indent=4)

                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description='Disabled command ' \
                                                              + f'{prefix}{args[1]} on this server.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.delete()
                                    await  message.channel.send(embed=em1)
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description='You cannot disable that command.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.delete()
                                    await  message.channel.send(embed=em1)
                            else:
                                print (f'{args[1]} is disabled. Enabling it.')

                                disabledcommands.remove(args[1])
                                print (f'New disabled command array: {disabledcommands}')

                                servers[f'sid{message.guild.id}']['disabledcommands'] = disabledcommands

                                with open('servers.json', 'w') as f:
                                    json.dump(servers, f, indent=4)
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description='Enabled command ' \
                                                              + f'{prefix}{args[1]} on this server.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                        else:
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description='Specify a command to toggle.', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await  message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=f'The {prefix}toggle command may ' \
                                                  + 'only be used by the server or bot owner.', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await  message.channel.send(embed=em1)
                elif args[0] == f'{prefix}addcom':
                    if get_userlevel(message.author, message.guild) > 1:
                        if len(args) > 1:
                            if args[1] == 'simple':
                                if len(args) > 5:
                                    # args[1] = type
                                    # args[2] = command name
                                    # args[3] = userlevel
                                    # args[4] = reply in pm? 0/1
                                    # args[5] = description
                                    # args[6:] = content

                                    try:
                                        content = ''
                                        for arg in args[6:]:
                                            content += f'{arg} '
                                        print(content)

                                        customcommands.add_simple_command(message.guild.id, args[2],
                                                                          int(args[3]), int(args[4]),
                                                                                            args[5],content)
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully added custom command.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except errors.CustomCommandNameError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='A custom command with that name already ' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await message.channel.send(embed=em1)
                                    except ValueError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Userlevel/replyinpm must be an integer.' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await message.channel.send(embed=em1)
                            elif args[1] == 'quotesys':
                                if len(args) > 6:
                                    # args[2] = quotesysname
                                    # args[3] = userlevel
                                    # args[4] = addquote name
                                    # args[5] = addquote userlevel
                                    # args[6] = delquote name
                                    # args[7] = delquote userlevel

                                    try:
                                        customcommands.add_quote_command(message.guild.id,
                                                                         args[2], int(args[3]))
                                        customcommands.add_addquote_command(message.guild.id,
                                                                            args[4], int(args[5]),
                                                                            args[2])
                                        customcommands.add_delquote_command(message.guild.id,
                                                                            args[6], int(args[7]),
                                                                            args[2])
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully added custom quote system.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except errors.CustomCommandNameError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='A custom command with that name already ' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except ValueError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Userlevel must be an integer.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Usage: `{prefix}addcom quotesys [name] ' +
                                                              '[userlevel] [addcomname] [addcomuserlevel] ' +
                                                              '[delcomname] [delcomuserlevel]`', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                            elif args[1] == 'quote':
                                if len(args) > 3:
                                    # args[1] = type
                                    # args[2] = quotesys name
                                    # args[3] = userlevel

                                    try:
                                        customcommands.add_quote_command(message.guild.id,
                                                                            args[2], int(args[3]))
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully added custom command.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except errors.CustomCommandNameError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='A custom command with that name already ' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send()
                                    except ValueError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Userlevel must be an integer.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)

                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Usage: `{prefix}addcom quote [name] ' +
                                                              '[userlevel]`', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                            elif args[1] == 'addquote':
                                if len(args) > 4:
                                    # args[1] = type
                                    # args[2] = command name
                                    # args[3] = userlevel
                                    # args[4] = quote system name

                                    try:
                                        customcommands.add_addquote_command(message.guild.id,
                                                                            args[2], int(args[3]),
                                                                            args[4])
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully added custom command.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except errors.CustomCommandNameError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='A custom command with that name already ' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except ValueError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Userlevel must be an integer.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)

                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Usage: `{prefix}addcom addquote [name] ' +
                                                              '[userlevel] [quotesys]`', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                            elif args[1] == 'delquote':
                                if len(args) > 4:
                                    # args[1] = type
                                    # args[2] = command name
                                    # args[3] = userlevel
                                    # args[4] = quote system name

                                    try:
                                        customcommands.add_delquote_command(message.guild.id,
                                                                            args[2], int(args[3]),
                                                                            args[4])
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully added custom command.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except errors.CustomCommandNameError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='A custom command with that name already ' +
                                                                  'exists.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    except ValueError:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Userlevel must be an integer.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'Usage: `{prefix}addcom delquote [name] ' +
                                                              '[userlevel] [quotesys]`', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                            else:
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description=f'Unknown type. Supported types: ' +
                                                          '`simple`, `quote`, `addquote`, `delquote`', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await  message.channel.send(embed=em1)
                        else:
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description= f'Usage: `{prefix}addcom [type] [command-options]`', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await  message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=f'You do not have permission to use that command.', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await  message.channel.send(embed=em1)
                elif args[0] == f'{prefix}delcom':
                    if get_userlevel(message.author, message.guild) > 1:
                        if len(args) > 1:
                            customcommandarray = servers[f'sid{message.guild.id}']['customcommands']

                            for command in customcommandarray:
                                if command['name'] == args[1]:
                                    servers[f'sid{message.guild.id}']['customcommands'].remove(command)

                                    with open('servers.json', 'w') as f:
                                        json.dump(servers, f, indent=4)
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description='Successfully removed command.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                    return

                            # If command isn't found, fallback to this.
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description='That command does not exist.', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await  message.channel.send(embed=em1)
                        else:
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description=f'Usage: `{prefix}delcom [name]`', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await  message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=f'You do not have permission to use that command.', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await  message.channel.send(embed=em1)
                elif args[0] == f'{prefix}userlevel' and 'userlevel' not in disabledcommands:
                    userlevel = get_userlevel(message.author, message.guild)
                    mse=random.choice(mge)
                    rant = random.randint(0, 0xffffff)
                    em1=discord.Embed(title=mse, description=f'<@{message.author.id}>: You have userlevel {userlevel}.', color=rant,)
                    em1.set_author(name="Xceed",
                                     icon_url=bot.user.avatar_url,
                                     )
                    await message.delete()
                    await message.channel.send(embed=em1)
                elif args[0] == f'{prefix}8ball' and '8ball' not in disabledcommands:
                    if len(args) > 1:
                        randomnum = random.randint(1,20);
                        quote = '';
                        if randomnum == 1:
                            quote = 'It is certain.'
                        elif randomnum == 2:
                            quote = 'It is decidedly so.'
                        elif randomnum == 3:
                            quote = 'Without a doubt, yes.'
                        elif randomnum == 4:
                            quote = 'Yes, definitely.'
                        elif randomnum == 5:
                            quote = 'You may rely on it.'
                        elif randomnum == 6:
                            quote = 'As I see it, yes.'
                        elif randomnum == 7:
                            quote = 'It is most likely.'
                        elif randomnum == 8:
                            quote = 'The outlook is good.'
                        elif randomnum == 9:
                            quote = 'Yes.'
                        elif randomnum == 10:
                            quote = 'Signs point to yes.'
                        elif randomnum == 11:
                            quote = 'Reply hazy. Try again.'
                        elif randomnum == 12:
                            quote = 'Ask again later.'
                        elif randomnum == 13:
                            quote = 'It\'s better not to tell you now.'
                        elif randomnum == 14:
                            quote = 'I cannot predict that now.'
                        elif randomnum == 15:
                            quote = 'Concentrate and ask again.'
                        elif randomnum == 16:
                            quote = 'Don\'t count on it.'
                        elif randomnum == 17:
                            quote = 'My reply is no.'
                        elif randomnum == 18:
                            quote = 'My sources say no.'
                        elif randomnum == 19:
                            quote = 'The outlook is not so good.'
                        elif randomnum == 20:
                            quote = 'It is very doubtful.'

                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=f'<@{message.author.id}>: {quote}', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=f'<@{message.author.id}>: I cannot answer ' \
                                                  + 'a question I have not been asked.', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await message.channel.send(embed=em1)
                elif args[0] == f'{prefix}quote' and 'quote' not in disabledcommands:
                    if len(args) > 1:
                        try:
                            await message.channel.send(quotesystem.get_quote(message.guild.id,
                                                                            int(args[1])))
                        except ValueError:
                            if args[1] == 'list':
                                quotes = quotesystem.list_quotes(message.guild.id)
                                if quotes != None:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=quotes, color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                                    channel=message.author.create_dm()
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'<@{message.author.id}>: Check your PMs', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await channel.send(embed=em1)
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=f'There are no quotes to list.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                            else:
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description=f'Failed to get quote; argument given ' +
                                                          'was not an integer.', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description=quotesystem.get_quote(message.guild.id,
                                                                        None), color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await message.channel.send(embed=em1)
                elif args[0] == f'{prefix}addquote':
                    if get_userlevel(message.author, message.guild) > 0:
                        if len(args) > 1:
                            quotestring = ''
                            for arg in args[1:]:
                                quotestring += f'{arg} '
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description=quotesystem.add_quote(message.guild.id,
                                                                            quotestring), color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await message.delete()
                            await message.channel.send(embed=em1)
                elif args[0] == f'{prefix}delquote':
                    if get_userlevel(message.author, message.guild) > 0:
                        if len(args) > 1:
                            if args[1] == "all":
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description='**Hold it!** ' +
                                                          'This will remove every quote on this server. ' +
                                                          'Continue? [y/N]', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await message.channel.send(embed=em1)
                                #msg = await client.wait_for_message(author=message.author)
                                msg = await client.wait_for('message', check=check(context.author))
                                if msg.content == 'y':
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=quotesystem.remove_all_quotes(message.guild.id), color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                            else:
                                try:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description=quotesystem.remove_quote(message.guild.id,
                                                                                       int(args[1])), color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                                except ValueError:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description='Couldn\'t remove quote; argument given ' +
                                                              'was not an integer.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                        else:
                            mse=random.choice(mge)
                            rant = random.randint(0, 0xffffff)
                            em1=discord.Embed(title=mse, description='Couldn\'t delete quote; ' +
                                                          'No index given.', color=rant,)
                            em1.set_author(name="Xceed",
                                             icon_url=bot.user.avatar_url,
                                             )
                            await message.channel.send(embed=em1)
                    else:
                        mse=random.choice(mge)
                        rant = random.randint(0, 0xffffff)
                        em1=discord.Embed(title=mse, description='Permission denied.', color=rant,)
                        em1.set_author(name="Xceed",
                                         icon_url=bot.user.avatar_url,
                                         )
                        await message.channel.send(embed=em1)
                elif args[0] == f'{prefix}tf' and 'tf' not in disabledcommands:
                    mse=random.choice(mge)
                    rant = random.randint(0, 0xffffff)
                    em1=discord.Embed(title=mse, description='(╯°□°）╯︵ ┻━┻ FLIP THIS TABLE\n' \
                                        + '┻━┻ ︵ ヽ(°□°ヽ) FLIP THAT TABLE\n' \
                                        + '┻━┻ ︵ \\\\(°□°)/ ︵ ┻━┻ FLIP **ALL** THE TABLES', color=rant,)
                    em1.set_author(name="Xceed",
                                     icon_url=bot.user.avatar_url,
                                     )
                    await message.channel.send(embed=em1)
                    await message.delete()
#
                elif args[0] == f'{prefix}setulrolenames':
                    if get_userlevel(message.author, message.guild) > 1:
                        if len(args) > 2:
                            set_userlevel_rolenames(message.guild.id, args[1], args[2])
                            await message.channel.send(
                                                      f'Set userlevel rolenames to {args[1]} (mod), ' +
                                                      f'{args[2]} (admin).')
                        elif len(args) > 1:
                            set_userlevel_rolenames(message.guild.id, args[1],
                                                    servers[f'sid{message.guild.id}']['adminrolename'])
                            await message.channel.send(
                                                      f'Set userlevel rolenames to {args[1]} (mod), ' +
                                                      f'{args[2]} (admin).')
                        else:
                            await message.channel.send(
                                                      'Please specify the moderator and admin role names ' \
                                                      + '(mod first, admin second).')
                    else:
                        await message.channel.send(
                                                  f'The {prefix}setulrolenames command may only be used by ' \
                                                  + 'admins, the server owner, or the bot owner.')
                elif args[0] == f'{prefix}report' == message.content.lower():

                    mse=random.choice(mge)
                    rant=random.randint(0, 0xffffff)
                    online, idle, offline = community_report(message.guild)
                    emb1=discord.Embed(title=mse, description=f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```", color=rant)
                    emb1.set_author(name="Xceed",
                                     icon_url=bot.user.avatar_url,
                                     )
                    await message.channel.send(embed=emb1)
                else:
                    customcommandarray = servers[f'sid{message.guild.id}']['customcommands']
                    for command in customcommandarray:
                        if args[0][len(prefix):] == command['name'] and command['name'] not in disabledcommands:
                            if command['type'] == 'simple':
                                if get_userlevel(message.author, message.guild) >= int(command['userlevel']):
                                    if command['replyinpm'] == 1:
                                        author=message.author
                                        channel=await author.create_dm()
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=command['content'], color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await channel.send(embed=em1)
                                        await message.delete()
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=f'<@{message.author.id}>: Check your PMs', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await message.channel.send(embed=em1)
                                    else:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=command['content'], color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await message.channel.send(embed=em1)
                                        await message.delete()
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description='You do not have permission to use that command.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await message.channel.send(embed=em1)
                            elif command['type'] == 'quote' or command['type'] == 'quotesys':
                                if get_userlevel(message.author, message.guild) >= int(command['userlevel']):
                                    if len(args) > 1:
                                        try:
                                            mse=random.choice(mge)
                                            rant = random.randint(0, 0xffffff)
                                            em1=discord.Embed(title=mse, description=quotesystem.get_quote(message.guild.id,
                                                                  int(args[1]),
                                                                  command['name']), color=rant,)
                                            em1.set_author(name="Xceed",
                                                             icon_url=bot.user.avatar_url,
                                                             )
                                            await message.channel.send(embed=em1)
                                        except ValueError:
                                            if args[1] == 'list':
                                                quotes = quotesystem.list_quotes(message.guild.id, command['name'])
                                                if quotes != None:
                                                    author= message.author
                                                    channel = await author.create_dm()
                                                    mse=random.choice(mge)
                                                    rant = random.randint(0, 0xffffff)
                                                    em1=discord.Embed(title=mse, description=quotes, color=rant,)
                                                    em1.set_author(name="Xceed",
                                                                     icon_url=bot.user.avatar_url,
                                                                     )
                                                    await  channel.send(embed=em1)
                                                    mse=random.choice(mge)
                                                    rant = random.randint(0, 0xffffff)
                                                    em3=discord.Embed(title=mse, description=f'<@{message.author.id}>: Check your PMs', color=rant,)
                                                    em3.set_author(name="Xceed",
                                                                     icon_url=bot.user.avatar_url,
                                                                     )
                                                    await  message.channel.send(embed=em3)
                                                else:
                                                    mse=random.choice(mge)
                                                    rant = random.randint(0, 0xffffff)
                                                    em1=discord.Embed(title=mse, description=f'There are no quotes to list.', color=rant,)
                                                    em1.set_author(name="Xceed",
                                                                     icon_url=bot.user.avatar_url,
                                                                     )
                                                    await  message.channel.send(embed=em1)
                                            else:
                                                mse=random.choice(mge)
                                                rant = random.randint(0, 0xffffff)
                                                em1=discord.Embed(title=mse, description=f'Failed to get quote; argument given ' +
                                                'was not an integer.', color=rant,)
                                                em1.set_author(name="Xceed",
                                                                 icon_url=bot.user.avatar_url,
                                                                 )
                                                await  message.channel.send(embed=em1)
                                    else:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=quotesystem.get_quote(message.guild.id,
                                                              None, command['name']), color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                            elif command['type'] == 'addquote':
                                if get_userlevel(message.author, message.guild) >= int(command['userlevel']):
                                    if len(args) > 1:
                                        quotestring = ''
                                        for arg in args[1:]:
                                            quotestring += f'{arg} '
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description=quotesystem.add_quote(message.guild.id,
                                                              quotestring,
                                                              command['content']), color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                            elif command['type'] == 'delquote':
                                if get_userlevel(message.author, message.guild) >= int(command['userlevel']):
                                    if len(args) > 1:
                                        if args[1] == "all":
                                            mse=random.choice(mge)
                                            rant = random.randint(0, 0xffffff)
                                            em1=discord.Embed(title=mse, description='**Hold it!** ' +
                                            'This will remove every quote on this server. ' +
                                            'Continue? [y/N]', color=rant,)
                                            em1.set_author(name="Xceed",
                                                             icon_url=bot.user.avatar_url,
                                                             )
                                            await  message.channel.send(embed=em1)
                                            msg = await client.wait_for_message(author=message.author)
                                            if message.content == 'y':
                                                mse=random.choice(mge)
                                                rant = random.randint(0, 0xffffff)
                                                em1=discord.Embed(title=mse, description= quotesystem.remove_all_quotes(
                                                     message.guild.id,
                                                     command['content']), color=rant,)
                                                em1.set_author(name="Xceed",
                                                                 icon_url=bot.user.avatar_url,
                                                                 )
                                                await  message.channel.send(embed=em1)
                                        else:
                                            try:
                                                mse=random.choice(mge)
                                                rant = random.randint(0, 0xffffff)
                                                em1=discord.Embed(title=mse, description= quotesystem.remove_quote(message.guild.id,
                                                                         int(args[1]),
                                                                         command['content']), color=rant,)
                                                em1.set_author(name="Xceed",
                                                                 icon_url=bot.user.avatar_url,
                                                                 )
                                                await  message.channel.send(embed=em1)
                                            except ValueError:
                                                mse=random.choice(mge)
                                                rant = random.randint(0, 0xffffff)
                                                em1=discord.Embed(title=mse, description= 'Couldn\'t remove quote; argument given ' +
                                                'was not an integer.', color=rant,)
                                                em1.set_author(name="Xceed",
                                                                 icon_url=bot.user.avatar_url,
                                                                 )
                                                await  message.channel.send(embed=em1)
                                    else:
                                        mse=random.choice(mge)
                                        rant = random.randint(0, 0xffffff)
                                        em1=discord.Embed(title=mse, description= 'Couldn\'t delete quote; ' +
                                                                  'No index given.', color=rant,)
                                        em1.set_author(name="Xceed",
                                                         icon_url=bot.user.avatar_url,
                                                         )
                                        await  message.channel.send(embed=em1)
                                else:
                                    mse=random.choice(mge)
                                    rant = random.randint(0, 0xffffff)
                                    em1=discord.Embed(title=mse, description= 'Permission denied.', color=rant,)
                                    em1.set_author(name="Xceed",
                                                     icon_url=bot.user.avatar_url,
                                                     )
                                    await  message.channel.send(embed=em1)
                            else:
                                mse=random.choice(mge)
                                rant = random.randint(0, 0xffffff)
                                em1=discord.Embed(title=mse, description= 'Error: Custom command is of ' +
                                                          'unknown type.', color=rant,)
                                em1.set_author(name="Xceed",
                                                 icon_url=bot.user.avatar_url,
                                                 )
                                await  message.channel.send(embed=em1)

                                break
                            return
                            usecounter -= 1

                # And now we save the new usecounter to the json.
                config['usecounter'] = usecounter

                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)

    await bot.process_commands(message)

# mmsg = messagestr[::1000]
#
# index = 0
# while True:
#     msg = await Bot.send_file(ctx.message.channel, mmsg[index])
#     l = index != 0
#     r = index != len(mmsg) - 1
#     if l:
#         await Bot.add_reaction(msg, left)
#     if r:
#         await Bot.add_reaction(msg, right)
#     Bot.wait_for_reaction
#     reaction, ctx.message.author = await Bot.wait_for_reaction(check=predicate(msg, l, r))
#     if reaction.emoji == left:
#         index -= 1
#     elif reaction.emoji == right:
#         index += 1
#     await Bot.delete_message(msg)

@bot.command(name="atclink", description="atc class link demo")
async def atclink(ctx):
    author= ctx.message.author
    channel = await author.create_dm()
    mse=random.choice(mge)
    rant = random.randint(0, 0xffffff)
    em1=discord.Embed(title=mse, description='https://meet.google.com/ose-yyjs-poh', color=rant,)
    em1.set_author(name="Xceed",
                     icon_url=bot.user.avatar_url,
                     )
    await channel.send(embed=em1)
    await ctx.message.delete()
@bot.command(name="echo", description="Prints the Given Text")
async def echo(ctx,*args):
    output=''
    for word in args:
        output+=word
        output+=' '
    mse=random.choice(mge)
    rant = random.randint(0, 0xffffff)
    em1=discord.Embed(title=mse, description=output, color=rant,)
    em1.set_author(name="Xceed",
                     icon_url=bot.user.avatar_url,
                     )
    await ctx.send(embed=em1)
    await ctx.message.delete()
# @bot.command()
# async def poll(ctx,*,message):
#     mse=random.choice(mge)
#     rant = random.randint(0, 0xffffff)
#     emb=discord.Embed(title="Question : ", description=f"{message}", color=rant,)
#     emb.set_author(name="Xceed",
#                      icon_url=bot.user.avatar_url,
#                      )
#     msg=await ctx.send(embed=emb)
#     await msg.add_reaction('1️⃣')
#     await msg.add_reaction('2️⃣')
#     await msg.add_reaction('3️⃣')
#     await msg.add_reaction('4️⃣')
@bot.command(brief='!poll "[question]" [choices]', description='Create a poll (9 maximum choices)')
async def poll(ctx):
    items=ctx.message.content.split(",")
    question = items[0]
    answers = '\n'.join(items[1:])
    answers=answers.split(",")
    # type(answer)
    # type(answer)
    print(answers)
    rant=random.randint(0, 0xffffff)
    reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    embed = discord.Embed(title=':clipboard: New Question', description=f"{question}", color=rant)
    embed.set_author(name=f'By {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

    #await message.delete()
    for i in range(1, len(items)):
        embed.add_field(name=f"{reactions[i-1]} Option no.{i}", value=items[i], inline=False)
    msg=await ctx.send(embed=embed)

    for i in range(len(items[1:])):
        await msg.add_reaction(reactions[i])
    await ctx.message.delete()
@bot.command()
async def meme(ctx):
    #embed = discord.Embed(title=" ", description=" ")
    # print(1)
    async with aiohttp.ClientSession() as cs:
        # print(1)
        async with cs.get("https://meme-api.herokuapp.com/gimme") as r:
            # print(1)
            res = await r.json()
            #print(1)
            url=res['url']

            embed = discord.Embed(title=res['title'],
                       url=res['postLink'],
                       description=' ')
            # embed.add_field(name='✍', value=res['author'], inline=False)
            # embed.add_field(name='👍', value=res['ups'], inline=True)
            embed.set_image(url=url)
            embed.set_footer(text=" 💬 {}    👍 {}  ".format(res['author'],res['ups']))
            # embed.set_footer(text=res['ups'])
            await ctx.message.delete()
            print(1)
            await ctx.send(embed=embed)
@bot.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):

    if ctx.voice_client is None:
        return await ctx.send("Not connected to voice channel")

    print(volume/100)

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

with open('servers.json', 'r') as f:
    servers = json.load(f)

@bot.command()
async def attendee(ctx):
    if get_userlevel(ctx.message.author, ctx.message.guild) >= 1:
        channel = ctx.message.author.voice.channel #gets the channel you want to get the list from
        id=ctx.message.guild.id
        members = channel.members #finds members connected to the channel
        memids = [] #(list)
        for member in members:
            memids.append(member.id)
        author=ctx.message.author
        mse=random.choice(mge)
        rant = random.randint(0, 0xffffff)
        # str1 = ''.join(str(e)+' ' for e in memids)
        # for i in memids:
        #     print(i)
        #     await ctx.send(f'<@{i}>')
        now = datetime.now()
        totalp=len(memids)
        dt_string = now.strftime("%A, %B %d,%Y, %I:%M%p ")
        em1=discord.Embed(title=f'Attendance of {ctx.message.author.voice.channel}', description=f' Asked by `{ctx.message.author}` \n Date:  `{dt_string}` 🕐\n Category: `{ctx.message.author.voice.channel.category}` \n ✅ Total Present: `{totalp}` ', color=rant,)
        for i, val in enumerate(memids):
            print (i, ",",val)
            em1.add_field(name=i+1, value=f'<@{val}>', inline=False)
        em1.set_thumbnail(url=author.avatar_url)
        em1.set_author(name="Xceed",
                         icon_url=bot.user.avatar_url,
                         )
        await ctx.send('Check Attendance ' + format(f'<@{author.id}>'))
        await ctx.message.delete()
        em1.set_thumbnail(url=author.avatar_url)
        await ctx.message.channel.send(embed=em1)
        print(memids)
    else:
        mse=random.choice(mge)
        rant = random.randint(0, 0xffffff)

        em1=discord.Embed(title=mse, description="you don't have permission to do that. 😬", color=rant)

        em1.set_author(name="Xceed",
                         icon_url=bot.user.avatar_url,
                         )
        em1.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=em1)
@bot.command()
async def comrep(ctx):
    community_report()
bot.run(TOKEN)
