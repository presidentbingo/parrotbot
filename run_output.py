import discord
import asyncio

import ctypes

import random

import json
import requests
import codecs

import configparser
import ast

import os
import logging

import datetime
import time

LOG_NUM = 0
log_num_exists = True

while log_num_exists == True:
    if os.path.exists("logs/" + str(LOG_NUM) + "_bot.log"):
        #print("exists")
        LOG_NUM += 1
    else:
        #print("no exists")
        log_num_exists = False

FILENAME = str(LOG_NUM) + '_bot.log'

file_handler = logging.FileHandler('logs/' + FILENAME, 'w', 'utf-8')
#stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler] # handlers = [file_handler, stdout_handler] # to print to console as well as to the log

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

#ctypes.windll.kernel32.SetConsoleTitleW("ParrotBot OUTPUT")

client = discord.Client()

OWNER_ID = '192023544480137225'
TOKEN = 'NTU4MzMzNjY0NzM2MzEzMzU1.D3VUkg.OvIm2BdluTsHawKnARakplX2H7A' #bot token
#TOKEN = 'MTkyMDIzNTQ0NDgwMTM3MjI1.D3VjRw.ZsXbPa9LheJvY3FzP3C4hf9lJiA' #personal token
#TOKEN = 'NDE3MTY4NTUxNzIwNTE3NjQy.XJ-dbQ.cZAql1vTGShuKVBJFOyx3_HS3Jk'
PREFIX = '>parrot>'

AFTER_DELETE_MESSAGE_TIME = 15

COMMAND_LIST = [
    [PREFIX + 'help :question:', 'shows commands'], [PREFIX + 'img :frame_photo:', 'searches for an image'],
    [PREFIX + 'moveout :bow_and_arrow:', 'moves out a member'], [PREFIX + 'flip :red_circle:', 'flips a coin'],
    [PREFIX + 'clear :put_litter_in_its_place:', 'clears amount of messages'], [PREFIX + 'roll :game_die:', 'rolls a die'],
    [PREFIX + 'watchchannel :bird:', 'manage watched channels'], [PREFIX + 'outputchannel :bird:', 'manage output channels'],
    [PREFIX + 'watchuser :bird:', 'manage watched users'], [PREFIX + 'pair :bird:', 'manage paired channels'], [PREFIX + 'watchalluserchannel :bird:', 'manage watched all user channels']
]
COMMAND_LIST.sort()

CONFIG_NICKNAME_NAME = ''
CONFIG_GAME_NAME = ''
CONFIG_STATUS_NAME = ''
CONFIG_WATCHED_CHANNELS = []
CONFIG_WATCHED_ALL_USERS_CHANNELS = []
CONFIG_WATCHED_USERS = []
CONFIG_OUTPUT_CHANNELS = []
CONFIG_PAIRS = [[]]
config = configparser.ConfigParser()

config.read('config.ini')
CONFIG_NICKNAME_NAME = config['ParrotBot']['Nickname']
CONFIG_GAME_NAME = config['ParrotBot']['Game']
CONFIG_STATUS_NAME = config['ParrotBot']['Status']
CONFIG_WATCHED_CHANNELS = ast.literal_eval(config.get("ParrotBot", "Watched_Channels"))
CONFIG_WATCHED_ALL_USERS_CHANNELS = ast.literal_eval(config.get("ParrotBot", "Watched_All_Users_Channels"))
CONFIG_WATCHED_USERS = ast.literal_eval(config.get("ParrotBot", "Watched_Users"))
CONFIG_OUTPUT_CHANNELS = ast.literal_eval(config.get("ParrotBot", "Output_Channels"))
CONFIG_PAIRS = ast.literal_eval(config.get("ParrotBot", "Pairs"))

#print(CONFIG_NICKNAME_NAME + CONFIG_GAME_NAME + CONFIG_STATUS_NAME) #print config details

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def fixEmojiString(string):
    encoded_string = string.encode('ascii', errors='replace')
    return encoded_string.decode('ascii', errors='replace')

def make_image_request(MESSAGE):
    page = 1 + random.randint(5, 10)
    url = "https://www.googleapis.com/customsearch/v1?key=" + "AIzaSyAa4lxOV83yqRpRdueGruVuNCqr-JxBfQs" + "&cx=" + "000148466820596494456:fbex4pzkewo" + "&q=" + (MESSAGE.replace(" ", '+')) + "&searchType=image&alt=json&num=10&start=" + str(page)
    r = requests.get(url=url)
    dictFromJSON = json.loads(r.content.decode('utf-8'))
    dictFromJSON['http_code'] = r.status_code
    return dictFromJSON

def saveConfig():
    config['ParrotBot'] = {'Nickname': CONFIG_NICKNAME_NAME, 'Status': CONFIG_STATUS_NAME, 'Game': CONFIG_GAME_NAME, 'Watched_Channels': CONFIG_WATCHED_CHANNELS, 'Watched_All_Users_Channels': CONFIG_WATCHED_ALL_USERS_CHANNELS, 'Watched_Users': CONFIG_WATCHED_USERS, 'Output_Channels': CONFIG_OUTPUT_CHANNELS, 'Pairs': CONFIG_PAIRS} # write to the config file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

@client.event
async def on_ready():    

    config.read('config.ini')
    CONFIG_NICKNAME_NAME = config['ParrotBot']['Nickname']
    CONFIG_STATUS_NAME = config['ParrotBot']['Status']
    CONFIG_GAME_NAME = config['ParrotBot']['Game']
    CONFIG_WATCHED_CHANNELS = config['ParrotBot']['Watched_Channels']
    CONFIG_WATCHED_USERS = config['ParrotBot']['Watched_Users']
    CONFIG_OUTPUT_CHANNELS = config['ParrotBot']['Output_Channels']

    FIXED_CONFIG_NICKNAME_NAME, FIXED_CONFIG_GAME_NAME, FIXED_CONFIG_STATUS_NAME = fixEmojiString(CONFIG_NICKNAME_NAME), fixEmojiString(CONFIG_GAME_NAME), fixEmojiString(CONFIG_STATUS_NAME)

    status = discord.Status.online

    if CONFIG_STATUS_NAME.lower() == "online":
        status = discord.Status.online
    elif CONFIG_STATUS_NAME.lower() == "offline" or CONFIG_STATUS_NAME.lower() == "invisible":
        status = discord.Status.offline
    elif CONFIG_STATUS_NAME.lower() == "idle":
        status = discord.Status.idle
    elif CONFIG_STATUS_NAME.lower() == "dnd" or CONFIG_STATUS_NAME.lower() == "do_not_disturb":
        status = discord.Status.dnd

    '''
    if CONFIG_NICKNAME_NAME != client.user.display_name:
        server = discord.utils.get(client.servers, id="297939129222692864")
        if server != None:
            await client.change_nickname(server.me, CONFIG_NICKNAME_NAME)
        server = discord.utils.get(client.servers, id="197913149985259520")
        if server != None:
            await client.change_nickname(server.me, CONFIG_NICKNAME_NAME)
    await client.change_presence(status=status, game=discord.Game(type=0, name=CONFIG_GAME_NAME))
    '''

#    config['ParrotBot'] = {'Nickname': 'ParrotBot', 'Status': 'online', 'Game': '@michaelvuolo_ on twitter', 'Watched_Channels': ['197913149985259520'], 'Watched_Users': ['192023544480137225'], 'Output_Channels': ['347556527189524480']} # to write the new config file
#    with open('config.ini', 'w') as configfile:
#        config.write(configfile)
    
    print('-------------------------------')
    print(' Successfully logged in.\n')
    print(' Client Name: ' + client.user.name)
    print(' Client ID: ' + client.user.id)
    print(' Connected Servers: ' + str(len(client.servers)))
    print('')
    print(' Current Nickname: ' + FIXED_CONFIG_NICKNAME_NAME)
    print(' Current Status: ' + FIXED_CONFIG_STATUS_NAME)
    print(' Current Game: ' + FIXED_CONFIG_GAME_NAME)
    print('-------------------------------\n')
    print('Log:\n')

@client.event
async def on_voice_state_update(before, after):
    if before.voice_channel != after.voice_channel:
        if before.voice_channel != None and after.voice_channel != None:
            print('! ' + before.display_name + ' has switched from \'' + before.voice_channel.name + '\' to \'' + after.voice_channel.name + '\'.')
        elif before.voice_channel != None:
            print('! ' + before.display_name + ' has left \'' + before.voice_channel.name + '\'.')
        elif after.voice_channel != None:
            print('! ' + after.display_name + ' has joined \'' + after.voice_channel.name + '\'.')

@client.event
async def on_message(message):

    #print(message.author.name + "(" + message.server.name + " -> " + message.channel.name + "): " + message.content)
    #client.send_message(client.get_channel('347556527189524480'), message.content)

    # ------------------------------------------------------------- AUTO REPEAT STOLEN MESSAGE TO PERSONAL CHANNEL ------------------------------------------------------------- #

    if message.channel.id == '562455296174194702': # AUTO REPEAT STOLEN MESSAGE IN PERSONAL CHANNEL
        
        fixed_display_name, fixed_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            author_url = message.author.avatar_url
                
            if len(author_url) < 1:
                author_url = message.author.default_avatar_url
            
            if len(message.embeds) > 0:                
                curEmbed = message.embeds[0]

                embed = discord.Embed.from_data(curEmbed)

            else:
                embed = discord.Embed(description=fixed_message, color=0xfbb35a, timestamp=datetime.datetime.utcnow())
                if len(message.attachments) > 0:
                    print('found attachments')
                    for attachment in message.attachments:
                        url = attachment['url']
                        embed.set_image(url=url)
                        print(attachment['filename'].lower())
                        if attachment['filename'].lower().find('.png') == -1:
                            if attachment['filename'].lower().find('.jpeg') == -1:
                                if attachment['filename'].lower().find('.jpg') == -1:
                                    if attachment['filename'].lower().find('.gif') == -1:
                                        print('NON-IMAGE FILE DETECTED... sending file as link')
                                        embed.description = fixed_message + '\n\nAttached file: ' + url
                embed.set_author(name=message.author.display_name, icon_url=author_url)

            try:
                outChannel = message.content
                
                await client.send_message(client.get_channel(outChannel), embed=embed) # output to personal channel
            except Exception as ex:
                print("ERROR WRITING TO CHANNEL ID: " + outChannel)
                print(ex)
            print('! ' + fixed_display_name + ':')
            if fixed_message == '' and len(message.attachments) > 0:
                print('\t➡ [attachment]')
            else:
                print('\t➡ \'' + fixed_message + '\'')
    
    # =========================================================================== COMMANDS =========================================================================== #

    # ------------------------------------------------------------- help ------------------------------------------------------------- #
    
    if message.content.lower().startswith(PREFIX + 'help'): # help command

        await client.delete_message(message)
        COMMAND_NAME = 'help'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'help', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            author_url = message.author.avatar_url
                
            if len(author_url) < 1:
                author_url = message.author.default_avatar_url

            #command_list_description = ', '.join(COMMAND_LIST)

            embed = discord.Embed(title="Current Commands:", color=0x00cc66, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=message.author.display_name, icon_url=author_url)
            for x in range(0, len(COMMAND_LIST)):
                embed.add_field(name=COMMAND_LIST[x][0], value=COMMAND_LIST[x][1], inline=True)
            bot_sent_message = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME + 15)
            await client.delete_message(bot_sent_message)
            print('! ' + fixed_display_name + ' has used the \'help\' command.')

    # ------------------------------------------------------------- pair ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'pair'): # pair command

        await client.delete_message(message)
        COMMAND_NAME = 'pair'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'pair', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add` (separate the two channels with a comma , --> first channel: watched, second channel: output)), `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add` (separate the two channels with a comma , --> first channel: watched, second channel: output)), `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            if "add" in cut_message:

                stringChannels = cut_message[4:].replace(' ', '')
                firstChannel = stringChannels[:stringChannels.find(',')]
                secondChannel = stringChannels[stringChannels.find(',')+1:]

                pairChannels = []
                pairChannels.append(firstChannel)
                pairChannels.append(secondChannel)
                CONFIG_PAIRS.append(pairChannels)
                saveConfig()

                bot_sent_message = await client.send_message(message.channel, 'Added channel ids `' + cut_message[4:] + '` to the currently paired channels')
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has added channel ids ' + cut_message[4:].replace(' ', '').replace(',', ' to ') + ' to the currently paired channels')
            elif "remove" in cut_message:
                if int(cut_message[7:]) < len(CONFIG_PAIRS) and int(cut_message[7:]) > -1:
                    del CONFIG_PAIRS[int(cut_message[7:])]
                    saveConfig()

                    bot_sent_message = await client.send_message(message.channel, 'Removed list id `' + cut_message[7:] + '` from the currently paired channels')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' has removed list id ' + cut_message[7:] + ' from the currently paired channels')
                else:
                    bot_sent_message = await client.send_message(message.channel, 'Could not find list id `' + cut_message[7:] + '` in the currently paired channels list')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
            elif "list" in cut_message:
                author_url = message.author.avatar_url
                    
                if len(author_url) < 1:
                    author_url = message.author.default_avatar_url

                numEmbeds = int(len(CONFIG_PAIRS)/20) + 1

                startOffset = 0
                numLeftOffset = 0

                bot_sent_messages = []

                for x in range(0,numEmbeds):
                    if len(CONFIG_PAIRS) > 0:
                        embed = discord.Embed(title="Paired channels list (NOTE: PAIRS WILL ONLY WORK IF WATCHED & OUTPUT CHANNELS ARE SETUP FIRST FOR BOTH CHANNELS):", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        if len(CONFIG_PAIRS) >= 20:
                            for x in range(0 + startOffset, 20 + numLeftOffset):
                                embed.add_field(name="`" + str(x) + "` " + "From: " + CONFIG_PAIRS[x][0] + " To: " + CONFIG_PAIRS[x][1], value="From: " + str(discord.utils.get(client.get_all_channels(), id=CONFIG_PAIRS[x][0])) + " To: " + str(discord.utils.get(client.get_all_channels(), id=CONFIG_PAIRS[x][1])), inline=True)
                            startOffset += 20
                            if len(CONFIG_PAIRS) - startOffset < 20:
                                numLeftOffset += len(CONFIG_PAIRS) - startOffset
                            else:
                                numLeftOffset += 20
                        else:
                            for x in range(0, len(CONFIG_PAIRS)):
                                embed.add_field(name="`" + str(x) + "` " + "From: " + CONFIG_PAIRS[x][0] + " To: " + CONFIG_PAIRS[x][1], value="From: " + str(discord.utils.get(client.get_all_channels(), id=CONFIG_PAIRS[x][0])) + " To: " + str(discord.utils.get(client.get_all_channels(), id=CONFIG_PAIRS[x][1])), inline=True)
                    else:
                        embed = discord.Embed(description="There are currently no watched all users channels specified.", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        
                    bot_sent_messages.append(await client.send_message(message.channel, embed=embed))
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)    #to delete both messages, you must make a list of the messages as being sent-> then delete each item in list
                for message in bot_sent_messages:
                    await client.delete_message(message)
                print('! ' + fixed_display_name + ' has listed the currently paired channels')
            else:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add` (separate the two channels with a comma , --> first channel: watched, second channel: output), `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- watchchannel ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'watchchannel'): # watchchannel command

        await client.delete_message(message)
        COMMAND_NAME = 'watchchannel'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'watchchannel', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            if "add" in cut_message:
                CONFIG_WATCHED_CHANNELS.append(cut_message[4:])
                saveConfig()

                bot_sent_message = await client.send_message(message.channel, 'Added channel id `' + cut_message[4:] + '` to the currently watched channels')
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has added channel id ' + cut_message[4:] + ' to the currently watched channels')
            elif "remove" in cut_message:
                if int(cut_message[7:]) < len(CONFIG_WATCHED_CHANNELS) and int(cut_message[7:]) > -1:                
                    del CONFIG_WATCHED_CHANNELS[int(cut_message[7:])]
                    saveConfig()

                    bot_sent_message = await client.send_message(message.channel, 'Removed list id `' + cut_message[7:] + '` from the currently watched channels')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' has removed list id ' + cut_message[7:] + ' from the currently watched channels')
                else:
                    bot_sent_message = await client.send_message(message.channel, 'Could not find list id `' + cut_message[7:] + '` in the currently watched channels list')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
            elif "list" in cut_message:
                author_url = message.author.avatar_url
                    
                if len(author_url) < 1:
                    author_url = message.author.default_avatar_url

                numEmbeds = int(len(CONFIG_WATCHED_CHANNELS)/20) + 1

                startOffset = 0
                numLeftOffset = 0

                bot_sent_messages = []

                for x in range(0,numEmbeds):
                    if len(CONFIG_WATCHED_CHANNELS) > 0:
                        embed = discord.Embed(title="Channel watch list (watched users only):", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        if len(CONFIG_WATCHED_CHANNELS) >= 20:
                            for x in range(0 + startOffset, 20 + numLeftOffset):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_WATCHED_CHANNELS[x]), inline=True)
                            startOffset += 20
                            if len(CONFIG_WATCHED_CHANNELS) - startOffset < 20:
                                numLeftOffset += len(CONFIG_WATCHED_CHANNELS) - startOffset
                            else:
                                numLeftOffset += 20
                        else:
                            for x in range(0, len(CONFIG_WATCHED_CHANNELS)):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_WATCHED_CHANNELS[x]), inline=True)
                    else:
                        embed = discord.Embed(description="There are currently no watched channels specified.", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        
                    bot_sent_messages.append(await client.send_message(message.channel, embed=embed))
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)    #to delete both messages, you must make a list of the messages as being sent-> then delete each item in list
                for message in bot_sent_messages:
                    await client.delete_message(message)
                print('! ' + fixed_display_name + ' has listed the currently watched channels')
            else:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- watchalluserchannel ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'watchalluserchannel'): # watchalluserchannel command

        await client.delete_message(message)
        COMMAND_NAME = 'watchalluserchannel'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'watchalluserchannel', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            if "add" in cut_message:
                CONFIG_WATCHED_ALL_USERS_CHANNELS.append(cut_message[4:])
                saveConfig()

                bot_sent_message = await client.send_message(message.channel, 'Added channel id `' + cut_message[4:] + '` to the currently watched channels')
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has added channel id ' + cut_message[4:] + ' to the currently watched all users channels')
            elif "remove" in cut_message:
                if int(cut_message[7:]) < len(CONFIG_WATCHED_ALL_USERS_CHANNELS) and int(cut_message[7:]) > -1:                
                    del CONFIG_WATCHED_ALL_USERS_CHANNELS[int(cut_message[7:])]
                    saveConfig()

                    bot_sent_message = await client.send_message(message.channel, 'Removed list id `' + cut_message[7:] + '` from the currently watched all users channels')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' has removed list id ' + cut_message[7:] + ' from the currently watched all users channels')
                else:
                    bot_sent_message = await client.send_message(message.channel, 'Could not find list id `' + cut_message[7:] + '` in the currently watched all users channels list')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
            elif "list" in cut_message:
                author_url = message.author.avatar_url
                    
                if len(author_url) < 1:
                    author_url = message.author.default_avatar_url

                numEmbeds = int(len(CONFIG_WATCHED_ALL_USERS_CHANNELS)/20) + 1

                startOffset = 0
                numLeftOffset = 0

                bot_sent_messages = []

                for x in range(0,numEmbeds):
                    if len(CONFIG_WATCHED_ALL_USERS_CHANNELS) > 0:
                        embed = discord.Embed(title="Channel watch list (ALL USERS):", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        if len(CONFIG_WATCHED_ALL_USERS_CHANNELS) >= 20:
                            for x in range(0 + startOffset, 20 + numLeftOffset):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_ALL_USERS_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_WATCHED_ALL_USERS_CHANNELS[x]), inline=True)
                            startOffset += 20
                            if len(CONFIG_WATCHED_ALL_USERS_CHANNELS) - startOffset < 20:
                                numLeftOffset += len(CONFIG_WATCHED_ALL_USERS_CHANNELS) - startOffset
                            else:
                                numLeftOffset += 20
                        else:
                            for x in range(0, len(CONFIG_WATCHED_ALL_USERS_CHANNELS)):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_ALL_USERS_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_WATCHED_ALL_USERS_CHANNELS[x]), inline=True)
                    else:
                        embed = discord.Embed(description="There are currently no watched all users channels specified.", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        
                    bot_sent_messages.append(await client.send_message(message.channel, embed=embed))
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)    #to delete both messages, you must make a list of the messages as being sent-> then delete each item in list
                for message in bot_sent_messages:
                    await client.delete_message(message)
                print('! ' + fixed_display_name + ' has listed the currently watched all users channels')
            else:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- watchuser ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'watchuser'): # watchuser command

        await client.delete_message(message)
        COMMAND_NAME = 'watchuser'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'watchuser', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            if "add" in cut_message:
                CONFIG_WATCHED_USERS.append(cut_message[4:])
                saveConfig()

                bot_sent_message = await client.send_message(message.channel, 'Added user id `' + cut_message[4:] + '` to the currently watched users')
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has added user id ' + cut_message[4:] + ' to the currently watched users')
            elif "remove" in cut_message:
                if int(cut_message[7:]) < len(CONFIG_WATCHED_USERS) and int(cut_message[7:]) > -1:
                    del CONFIG_WATCHED_USERS[int(cut_message[7:])]
                    saveConfig()

                    bot_sent_message = await client.send_message(message.channel, 'Removed user list id `' + cut_message[7:] + '` from the currently watched users')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' has removed user list id ' + cut_message[7:] + ' from the currently watched channels')
                else:
                    bot_sent_message = await client.send_message(message.channel, 'Could not find user list id `' + cut_message[7:] + '` in the currently watched users list')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
            elif "list" in cut_message:
                author_url = message.author.avatar_url
                    
                if len(author_url) < 1:
                    author_url = message.author.default_avatar_url

                numEmbeds = int(len(CONFIG_WATCHED_USERS)/20) + 1

                startOffset = 0
                numLeftOffset = 0

                bot_sent_messages = []

                for x in range(0,numEmbeds):
                    if len(CONFIG_WATCHED_USERS) > 0:
                        embed = discord.Embed(title="User watch list:", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        if len(CONFIG_WATCHED_USERS) >= 20:
                            for x in range(0 + startOffset, 20 + numLeftOffset):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_USERS[x], value=discord.utils.get(client.get_all_members(), id=CONFIG_WATCHED_USERS[x]), inline=True)
                            startOffset += 20
                            if len(CONFIG_WATCHED_USERS) - startOffset < 20:
                                numLeftOffset += len(CONFIG_WATCHED_USERS) - startOffset
                            else:
                                numLeftOffset += 20
                        else:
                            for x in range(0, len(CONFIG_WATCHED_USERS)):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_WATCHED_USERS[x], value=discord.utils.get(client.get_all_members(), id=CONFIG_WATCHED_USERS[x]), inline=True)
                    else:
                        embed = discord.Embed(description="There are currently no watched users specified.", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        
                    bot_sent_messages.append(await client.send_message(message.channel, embed=embed))
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)    #to delete both messages, you must make a list of the messages as being sent-> then delete each item in list
                for message in bot_sent_messages:
                    await client.delete_message(message)
                    
                bot_sent_message = await client.send_message(message.channel, embed=embed)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has listed the currently watched users')
            else:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- outputchannel ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'outputchannel'): # outputchannel command

        await client.delete_message(message)
        COMMAND_NAME = 'outputchannel'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'outputchannel', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            if "add" in cut_message:
                CONFIG_OUTPUT_CHANNELS.append(cut_message[4:])
                saveConfig()

                bot_sent_message = await client.send_message(message.channel, 'Added channel id `' + cut_message[4:] + '` to the current output channels')
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                print('! ' + fixed_display_name + ' has added channel id ' + cut_message[4:] + ' to the current output channels')
            elif "remove" in cut_message:
                if int(cut_message[7:]) < len(CONFIG_OUTPUT_CHANNELS) and int(cut_message[7:]) > -1:
                    del CONFIG_OUTPUT_CHANNELS[int(cut_message[7:])]
                    saveConfig()

                    bot_sent_message = await client.send_message(message.channel, 'Removed list id `' + cut_message[7:] + '` from the current output channels')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' has removed list id ' + cut_message[7:] + ' from the currently watched channels')
                else:
                    bot_sent_message = await client.send_message(message.channel, 'Could not find list id `' + cut_message[7:] + '` in the current output channels list')
                    await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                    await client.delete_message(bot_sent_message)
                    print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
            elif "list" in cut_message:
                author_url = message.author.avatar_url
                    
                if len(author_url) < 1:
                    author_url = message.author.default_avatar_url

                numEmbeds = int(len(CONFIG_OUTPUT_CHANNELS)/20) + 1

                startOffset = 0
                numLeftOffset = 0

                bot_sent_messages = []

                for x in range(0,numEmbeds):
                    if len(CONFIG_OUTPUT_CHANNELS) > 0:
                        embed = discord.Embed(title="Output channel list (`ID 0 is the default channel if no paired channels are found`):", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        if len(CONFIG_OUTPUT_CHANNELS) >= 20:
                            for x in range(0 + startOffset, 20 + numLeftOffset):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_OUTPUT_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_OUTPUT_CHANNELS[x]), inline=True)
                            startOffset += 20
                            if len(CONFIG_OUTPUT_CHANNELS) - startOffset < 20:
                                numLeftOffset += len(CONFIG_OUTPUT_CHANNELS) - startOffset
                            else:
                                numLeftOffset += 20
                        else:
                            for x in range(0, len(CONFIG_OUTPUT_CHANNELS)):
                                embed.add_field(name="`" + str(x) + "` " + CONFIG_OUTPUT_CHANNELS[x], value=discord.utils.get(client.get_all_channels(), id=CONFIG_OUTPUT_CHANNELS[x]), inline=True)
                    else:
                        embed = discord.Embed(description="There are currently no output channels specified.", color=0xfe2964, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=message.author.display_name, icon_url=author_url)
                        
                    bot_sent_messages.append(await client.send_message(message.channel, embed=embed))
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)    #to delete both messages, you must make a list of the messages as being sent-> then delete each item in list
                for message in bot_sent_messages:
                    await client.delete_message(message)

                print('! ' + fixed_display_name + ' has listed the current output channels')
            else:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid argument for the `' + COMMAND_NAME + '` command. Valid arguments: `add`, `remove` (type index number from list), `list`')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
    
    # ------------------------------------------------------------- img ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'img'): # img command

        await client.delete_message(message)
        COMMAND_NAME = 'img'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'img', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)

        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid keyword for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid keyword for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            try:

                dictFromJSON = make_image_request(cut_message)
                link = dictFromJSON['items'][0]['link']

                await client.send_message(message.channel, message.author.mention + ', image result for `' + cut_message + '`: ' + link)
                print('! ' + fixed_display_name + ' has searched for the image:')
                print('\t➡ \'' + fixed_cut_message + '\'')
            
            except:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', error whilst searching for `' + cut_message + '`.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- moveout ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'moveout'): # moveout command

        await client.delete_message(message)
        COMMAND_NAME = 'moveout'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'moveout', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid member for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid member for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            try:

                if len(message.mentions) > 0:
                    victim = message.mentions[0]
                else:
                    victim = discord.utils.find(lambda x: cut_message.lower() in x.display_name.lower(), message.server.members)
                kick_channel = await client.create_channel(message.server, "bye bye! @michaelvuolo_ ;)", type=discord.ChannelType.voice)
                await client.move_member(victim, kick_channel)
                await client.delete_channel(kick_channel)

            except:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please type a valid user.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- move ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'move'): # move command

        await client.delete_message(message)
        COMMAND_NAME = 'move'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'move', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid channel name for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid channel name for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            try:

                final_channel = discord.utils.find(lambda x: cut_message.lower() in x.name.lower(), message.server.channels)
                
                start_voice_channel = message.author.voice.voice_channel
                members_in_channel = len(start_voice_channel.voice_members)
                moved_member_names = [x.name for x in start_voice_channel.voice_members]

                while members_in_channel > 0:
                    try:
                        await client.move_member(start_voice_channel.voice_members[0], final_channel)
                        members_in_channel = len(start_voice_channel.voice_members)
                        await asyncio.sleep(0.15)
                    except:
                        break

                encoded_moved_member_names = [x.encode('ascii', errors='replace') for x in moved_member_names]
                fixed_moved_member_names = [x.decode('ascii', errors='replace') for x in encoded_moved_member_names]

                print('! ' + fixed_display_name + ' has moved', len(message.author.voice.voice_channel.voice_members), 'member(s) to the voice channel:', final_channel.name, '')
                print('\t➡ \'' + ' & '.join(fixed_moved_member_names) + '\'')

            except:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please type a valid channel.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # ------------------------------------------------------------- flip ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'flip'): # flip command

        await client.delete_message(message)
        COMMAND_NAME = 'flip'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'flip', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            random_flip = random.randint(0, 1) # 0 = heads 1 = tails
            
            tmp = await client.send_message(message.channel, ':red_circle: :large_blue_circle:')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, ':red_circle: :large_blue_circle:')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, ':large_blue_circle: :red_circle:')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, ':red_circle: :large_blue_circle:')
            await asyncio.sleep(0.5)
            if random_flip == 0:
                await client.edit_message(tmp, message.author.mention + ', you\'ve landed on :large_blue_circle: heads!')
                flip_title = 'heads'
            else:
                await client.edit_message(tmp, message.author.mention + ', you\'ve landed on :red_circle: tails!')
                flip_title = 'tails'
            print('! ' + fixed_display_name + ' has flipped a coin and landed on: ' + flip_title)

    # ------------------------------------------------------------- roll ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'roll'): # roll command

        await client.delete_message(message)
        COMMAND_NAME = 'roll'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'roll', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)
                
        if message.author != client.user:

            random_roll = random.randint(1, 6)

            if len(cut_message) > 0:
                random_roll = cut_message[1:]
            
            tmp = await client.send_message(message.channel, '♠ ♣ ♥ ♦')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, '♥ ♦ ♠ ♣')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, '♦ ♠ ♣ ♥')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, '♣ ♥ ♠ ♦')
            await asyncio.sleep(0.5)
            await client.edit_message(tmp, message.author.mention + ', you\'ve rolled a :game_die: ' + str(random_roll) + '!')
            print('! ' + fixed_display_name + ' has rolled a dice and landed on: ' + str(random_roll))

    # ------------------------------------------------------------- clear ------------------------------------------------------------- #
    
    elif message.content.lower().startswith(PREFIX + 'clear'): # clear command

        await client.delete_message(message)
        COMMAND_NAME = 'clear'
        cut_message = remove_prefix(message.content, PREFIX + COMMAND_NAME)
        #cut_message = message.content.lower().replace(PREFIX + 'clear', '')

        fixed_display_name, fixed_message, fixed_cut_message, fixed_channel_name = fixEmojiString(message.author.display_name), fixEmojiString(message.content), fixEmojiString(cut_message), fixEmojiString(message.channel.name)

        if message.author != client.user:

            if len(cut_message) == 0:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid number for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            elif cut_message[0] != ' ':
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please enter a valid number for the `' + COMMAND_NAME + '` command.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return
            cut_message = (cut_message[1:])
            fixed_cut_message = (fixed_cut_message[1:])

            try:
        
                msgs = []
                number = int(fixed_cut_message)
        
                async for x in client.logs_from(message.channel, limit = number):
                    msgs.append(x)

                encoded_msgs = [x.content.encode('ascii', errors='replace') for x in msgs]
                fixed_msgs = [x.decode('ascii', errors='replace') for x in encoded_msgs]
            
                if len(msgs) == 1:
                    await client.delete_message(msgs[0])
                    print('! ' + fixed_display_name + ' has cleared', number, 'message:')
                    print('\t➡ \'' + fixed_msgs[0] + '\'')
                else:
                    await client.delete_messages(msgs)
                    print('! ' + fixed_display_name + ' has cleared', number, 'messages:')
                    for x in fixed_msgs:
                        print('\t➡ \'' + x + '\'')
                    
            except ValueError:
                bot_sent_message = await client.send_message(message.channel, message.author.mention + ', please type a value from 1-100.')
                print('! ' + fixed_display_name + ' (' + fixed_channel_name + '): ' + fixed_message)
                await asyncio.sleep(AFTER_DELETE_MESSAGE_TIME)
                await client.delete_message(bot_sent_message)
                return

    # =========================================================================== COMMANDS =========================================================================== #

client.run(TOKEN) #run as bot
#client.run(TOKEN, bot=False) #run as personal
