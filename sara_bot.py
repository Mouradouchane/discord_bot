import sys # sys for define external moduels
import os # for env
import json # for parse response data 
import requests 

def define_path(folder_path = ""):
    sys.path.append(folder_path)

import random
from email import message_from_binary_file
from logging import exception
from jokeapi import Jokes
import discord # discord moduel important for dealing with discord API's & BOT 

define_path("./gifs/")
define_path("./reactions/")

from gif_api import get_gif
from reaction import get_reaction

# dotenv moduel for loading hidden keys in envirement 
from dotenv import dotenv_values
keys = dotenv_values(".env") # load keys from env file
#import asyncio

# set key's
discord_key = keys["discord_key"]
tenor_key   = keys["tenor_key"]
nasa_key    = keys["nasa_key"]
nasa_url    = keys["nasa_url"]

# discord controller
client = discord.Client()

# function who handle sending gif's
# this function using moduel => "gif/gif_api.py" 
async def send_gif(message,msg):
    
    try: 
        # function get_gif will try to get gif for you 
        if len(message) >= 1 :

            gif_path = await get_gif(tenor_key , message[1]) # get gif
            await msg.channel.send( gif_path ) #send it

        else : 
            # argument message[1] is missing" 
            await msg.channel.send( "[!gif] command error 'missing second argument' :sad:" )
    
    #  if error happend we will send it as messages
    except Exception as err:
        await msg.channel.send("[!gif]  command error missing second argument")
        await msg.channel.send("```[ERROR] " + str(err)+"```")


@client.event
async def on_ready():
    print("bot {0.user} is online now".format(client))

@client.event
async def on_message(msg):
    # get user name only without #....
    username = str(msg.author).split("#")[0]
    # get user message
    message  = str(msg.content).split(" ")
    # get channel when user send this message
    channel  = str(msg.channel.name)

    # just print message in console as & "log"
    print(f"[{channel}] {username} : {message}")

    # if response comming from this bot it's self don't response "just skip"
    if( msg.author == client.user):
        return

    ### __chat__💬 channel ###

    # response to specific channel
    if msg.channel.name == "__chat__💬":
        #
        # *** here where answers of messages & commands ***
        #

        # example : give reaction to message
        if message[0].lower() == "give me hearth":
            # send reaction emoji as unicode
            # UNICODE list : https://unicode.org/emoji/charts/full-emoji-list.html
            await msg.add_reaction("\U0001F970")


        # example : send a joke using jokes API
        if message[0].lower() == "!joke":
            j = await Jokes() # Initialise the class
            joke = await j.get_joke() # Retrieve a random joke
            if joke["type"] == "single": 
                # send joke
                await msg.channel.send(joke["joke"])
            else:
                await msg.channel.send(joke["setup"])
                await msg.channel.send(joke["delivery"])


        if message[0].lower() == "!random":
            await msg.channel.send(random.randint(-100,100))

        # example : using nasa API to get Photo Of the Day
        if message[0].lower() == "!nasa":
            req = requests.get(nasa_url+nasa_key)
            if req.status_code == 200:
                data = json.loads(req.content)
                await msg.channel.send("Nasa Photo of The Day")
                await msg.channel.send(data["url"])
                await msg.channel.send(data["explanation"])
            else:
                await msg.channel.send("Bad Conncetion to Nasa API's")

        # help message 
        if message[0].lower() == "!help":
            await msg.channel.send("""
!help           : display commands
!help command   : display help & examples for specific commands
!nasa           : display photo of the day from nasa + article
!gif target     : display random gif about topic
!random         : display random number between range
!joke           : display random joke
!react          : let bot react last message
hello sara      : let bot say hello for you
            """)

        if message[0].lower() == "!gif":
            # send_gif function it's the handler for this task
            await send_gif(message , msg)

    ### general channel ###

    # send gif's using gif api 'tenor'
    if msg.channel.name == "general":

        if message[0].lower() == "!gif":
            # send_gif function it's the handler for this task
            await send_gif(message , msg)


    ### for all channels ###

    # example if user sayed hello
    if msg.content == "hello sara" or msg.content == "hi sara" : 
        # sara say hello + his name
        await msg.channel.send(f"hi there , {username}")
        return

    #send random reaction sometimes
    if(random.randint(1,100) % 2 == 0): 
        await msg.add_reaction(get_reaction("empty"))


# run bot
client.run(discord_key)