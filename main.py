import discord
from discord.ext import commands
import pyrebase
import os
from keep_alive import keep_alive
import asyncio


client = commands.Bot(command_prefix = '.', help_command=None) 
client.remove_command("help")
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
 
#--- Custom Help Page ---#
@client.command()
async def help(ctx):
  page1 = discord.Embed(title = "Habbit | Help Information", dexcription = "Use .help for more info.", color = discord.Color.orange())
  page1.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page1.add_field(name = " Contents:", value = " 1. To-do List\n 2. Sched Reminder\n 3. Music Buddy\n 4. Pomodoro", inline = False)
  page1.add_field(name = " 📋 — To-do List\n⏰ — Sched Reminder\n🎶 — Music Buddy\n🍅 — Pomodoro\n🏆 — Leaderboard", value = '\u200b', inline = False)
  page1.set_footer(text="Main Page | Habbit is developed by: Hanna ({})".format(ctx.author.display_name))

  page2 = discord.Embed(title="📋 — To-do List", description="Page 1", colour=discord.Colour.orange())
  page2.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page2.set_footer(text="Help 1/5 | Reaction cooldown of 2 seconds •")
  
  page3 = discord.Embed(title="⏰ — Sched Reminder", description="Page 2", colour=discord.Colour.orange())
  page3.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page3.set_footer(text="Help 2/5 | Reaction cooldown of 2 seconds •")

  page4 = discord.Embed(title="🎶 — Music Buddy", description="Page 3", colour=discord.Colour.orange())
  page4.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page4.set_footer(text="Help 3/5 | Reaction cooldown of 2 seconds •")

  page5 = discord.Embed(title="🍅 — Pomodoro", description="Page 4", colour=discord.Colour.orange())
  page5.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page5.set_footer(text="Help 4/5 | Reaction cooldown of 2 seconds •")

  page6 = discord.Embed(title="🏆 — Leaderboard", description="Page 5", colour=discord.Colour.orange())
  page6.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
  page6.set_footer(text="Help 5/5 | Reaction cooldown of 2 seconds •")


  client.help_pages = [page1, page2, page3, page4, page5, page6]
  buttons = [u"🏠",u"📋", u"⏰", u"🎶", u"🍅", u"🏆"]
  pgnum = 0
  msg = await ctx.send(embed=client.help_pages[pgnum])
  for button in buttons:
    await msg.add_reaction(button) # Adds reaction buttons

  while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("Timeout Error")

        else:
            #previous_page = current
            if reaction.emoji == u"🏠":
              pgnum = 0 
            elif reaction.emoji == u"📋":
              pgnum = 1  
            elif reaction.emoji == u"⏰":
              pgnum = 2
            elif reaction.emoji == u"🎶":
              pgnum = 3
            elif reaction.emoji == u"🍅":
              pgnum = 4
            elif reaction.emoji == u"🏆":
              pgnum = 5

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            await msg.edit(embed = client.help_pages[pgnum])



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