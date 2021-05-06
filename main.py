import discord
from discord.ext import commands
import pyrebase
import os
from keep_alive import keep_alive
import asyncio

client = commands.Bot(command_prefix = '*', help_command=None) 
client.remove_command("help")
status = ['building habits ₍ᐢ ̥ ̞ ̥ᐢ₎☆']

cogs = ['cogs.tracker','cogs.music','cogs.pomodoro'] # add more cogs here

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
  print('{0.user} is READY!'.format(client))

 
#--- Custom Help Pages ---#
@client.command(name='help', aliases=['habbit-help'])
async def help(ctx):

  invite = 'https://discord.com/api/oauth2/authorize?client_id=835746127231057990&permissions=0&scope=bot'

  page1 = (discord.Embed(title = "Habbit | *Help Information*", description = "A Discord bot to help you build habits with your community and earn *carrot* points with every task you complete. This bot also includes some extra tools to boost your productivity!", color = discord.Color.orange())
       .set_author(name=ctx.author.display_name, url=" ", icon_url=ctx.author.avatar_url)
       .add_field(name = " 📋 — To-do List\n⏰ — Sched Reminder\n🎶 — Music Buddy\n🍅 — Pomodoro\n", value = '\u200b', inline = False)
       .add_field(name = "\n\nOther information", value = f"• Invite Habbit to your server [here]({invite}).\n• If you want to make a suggestion, report a bug, or reach out for the bot project, visit the repo [here]. ", inline = False)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(text="Main Page | Habbit is created by Hanna Mangampo (manghann_#0747) ☁️"))
  

  page2 = (discord.Embed(title="📋 — To-do List", description="**To-do Commands**\n`*add` - Add a task to your list.\n`*show` - Display your To-do List.\n`*finish` - Complete and remove a task from your list.\n\n`*mypoints` - Displays the total points of a user.\n`*daily` - For free additional points everyday.\n\nTo see who's leading and track your community member's points use `.leaderboard` or `lead`.\n", colour=discord.Colour.orange())
       .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(text="Help 1/4 | Reaction cooldown of 2 seconds •"))
  
  page3 = (discord.Embed(title="⏰ — Sched Reminder", description="Page 2", colour=discord.Colour.orange())
       .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(text="Help 2/4 | Reaction cooldown of 2 seconds •"))

  page4 = (discord.Embed(title="🎶 — Music Buddy", description="**Music Buddy Commands**\n`*summon` - Summons the bot to a voice channel.\n`*join`- Joins a voice channel.\n`*leave` - Clears the queue and leaves the voice channel.\n`*now` or `*playing`      - Displays the currently playing song.\n`*play` - Plays (and enqueues) a song.\n`*queue`- Shows music buddy's queue.\n\n**Other Commands:**\n `*pause` `*resume` `*stop` `*shuffle` `*remove` `*loop`\n ", colour=discord.Colour.orange())
       .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")  
       .set_footer(text="Help 3/4 | Reaction cooldown of 2 seconds •"))

  page5 = (discord.Embed(title="🍅 — Pomodoro", description="**Pomodoro Timer Commands**\n`*pmdr-start` - Must be followed by **<work_time>** **<break_time>** to start.\n`*pmdr-stop`- Stops the ongoing timer.\n", colour=discord.Colour.orange())
       .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(text="Help 4/4 | Reaction cooldown of 2 seconds •"))


  client.help_pages = [page1, page2, page3, page4, page5]
  buttons = [u"🥕",u"📋", u"⏰", u"🎶", u"🍅"]
  pgnum = 0
  msg = await ctx.send(embed=client.help_pages[pgnum])
  for button in buttons:
    await msg.add_reaction(button) # Adds reaction buttons

  while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=180.0)

        except asyncio.TimeoutError:
            return print("Timeout Error")

        else:
            #previous_page = current
            if reaction.emoji == u"🥕":
              pgnum = 0 
            elif reaction.emoji == u"📋":
              pgnum = 1  
            elif reaction.emoji == u"⏰":
              pgnum = 2
            elif reaction.emoji == u"🎶":
              pgnum = 3
            elif reaction.emoji == u"🍅":
              pgnum = 4

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            await msg.edit(embed = client.help_pages[pgnum])


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