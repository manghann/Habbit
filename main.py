import discord
from discord.ext import commands
import pyrebase
import os
from keep_alive import keep_alive

client = commands.Bot(command_prefix = '.') 
status = ['building habits ₍ᐢ ̥ ̞ ̥ᐢ₎☆']

cogs = ['cogs.tracker'] # add more cogs here

config = {
  "apiKey": "AIzaSyDRRANWbc40FBWLETEsqGRjhY2CcX1Ydos",
  "authDomain": "habbit-62caa.firebaseapp.com",
  "databaseURL": "https://habbit-62caa-default-rtdb.firebaseio.com",
  "storageBucket": "habbit-62caa.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

for cog in cogs:
  try:
    client.load_extension(cog)
  except Exception as e:
    print(f'Unable to load cog {cog}: {str(e)}')  
    
@client.event
async def on_ready():
  print('{0.user} is READY!'
  .format(client))       
  
#for filename in os.listdir('./cogs'):
  #if filename.endswith('.py'):
    #client.load_extension(f'cogs.{filename[:-3]}')
    
  #else:
    #print(f'Unable to load {filename[:-3]}')

#@client.event
#async def on_message(message):
  #if message.author == client.user:
  #  return
  #if message.content.startswith('Habbit!'):
  #  await message.channel.send('Hello! ꉂ₍ᐢ﹘ܫ﹘ᐢ₎ What do you want to do?') #include /help
  #await client.process_commands(message)  

keep_alive()
client.run(os.getenv('TOKEN'))  

#---#
client.run('TOKEN')