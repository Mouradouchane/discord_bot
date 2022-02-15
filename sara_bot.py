from email import message_from_binary_file
import json
import random
import requests 
import discord # discord moduel important for dealing with discord API's & BOT 

# joke API for get jokes 
from jokeapi import Jokes # Import the Jokes class
import asyncio

# KEY for Discord API's & client "use yours"
token = ""
client = discord.Client()

# KEY for Tenor API's "use yours"
tenor_key = ""

# KEY & URL for Nasa API's
nasa_url = "https://api.nasa.gov/planetary/apod?api_key="
nasa_key = "" # use yours 

# when discord client is ready 
@client.event
async def on_ready():
    print("bot {0.user} is online now".format(client))

# when someone send message 
@client.event
async def on_message(message):
    # get user name only without #....
    username = str(message.author).split("#")[0]
    # get user message
    user_msg = str(message.content)
    # get channel when user send this message
    channel = str(message.channel.name)

    # just print message in console as & "log"
    print(f"[{channel}] {username} : {user_msg}")

    # if this bot it's self don't respont
    if( message.author == client.user):
        return

    # response to specific channel
    if message.channel.name == "__chat__💬":
        #
        # *** here where answers of messages & commands ***
        #

        # example if user sayed hello
        if user_msg.lower() == "hello sara": 
            # sara say hello + his name
            await message.channel.send(f"hi there , {username}")
            return


        # example : give reaction to message
        if user_msg.lower() == "give me hearth":
            # send reaction emoji as unicode
            # UNICODE list : https://unicode.org/emoji/charts/full-emoji-list.html#1f970
            await message.add_reaction("\U0001F970")


        # example : send a joke using jokes API
        if user_msg.lower() == "give me a joke" or user_msg.lower() == "sara 3tini nokta" or user_msg.lower() == "!joke":
            j = await Jokes() # Initialise the class
            joke = await j.get_joke() # Retrieve a random joke
            if joke["type"] == "single": 
                # send joke
                await message.channel.send(joke["joke"])
            else:
                await message.channel.send(joke["setup"])
                await message.channel.send(joke["delivery"])

        
        # example send gif using tenor API
        if user_msg.lower() == "!gif":
            # max result comming from gif API
            max_gifs_request = 8
            index = random.randint(0,max_gifs_request-1)
            # send requst for 'smart gift'
            request = requests.get( "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ("smart", tenor_key , max_gifs_request) )

            # if respone from server was 200 mean it's GOOD 
            if request.status_code == 200:
                # save response 
                data = json.loads(request.content)["results"]
                print(data[index]["media"][0]["gif"]["url"])
                # pick & random gif & send it 
                await message.channel.send( data[index]["media"][0]["gif"]["url"] )
            else : 
                await message.channel.send( "bad response from gif's api :sad:" )


        if user_msg.lower() == "!random":
            await message.channel.send(random.randint(-100,100))

    
        # example : using nasa API to get Photo Of the Day
        if user_msg.lower() == "!nasa":
            # send request for photo of the day
            request = requests.get(nasa_url+nasa_key)
            if request.status_code == 200:
                # load comming data from that response 
                data = json.loads(request.content)
                # send msg to discord 
                await message.channel.send("Nasa Photo of The Day")
                await message.channel.send(data["url"])
                await message.channel.send(data["explanation"])
            else:
                await message.channel.send("Bad Conncetion to Nasa API's")


# run bot
client.run(token)