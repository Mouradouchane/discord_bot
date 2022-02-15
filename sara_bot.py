import random
import discord # discord moduel important for dealing with discord API's & BOT 

#  *** token key important for anything , you need one ***
token = ""

# discord client object for access discord API's & services 
client = discord.Client()

@client.event
async def on_ready():
    print("bot {0.user} is online now".format(client))

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
        if user_msg.lower() == "hello": 
            # sara say hello + his name
            await message.channel.send(f"hello {username}")
            return

        if user_msg.lower() == "!random":
            await message.channel.send(random.randint(-100,100))

    if user_msg.lower() == "sara":
        await message.channel.send("hi there i can't response in this channel")

# run bot
client.run(token)