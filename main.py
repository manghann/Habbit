import discord
import asyncio
import os

from random import choice
from discord.ext import commands, tasks
from keep_alive import keep_alive

intents = discord.Intents().all()
client = commands.Bot(command_prefix = '*', help_command=None) 
client.remove_command("help")
status = ["*help | build daily habits! 🌈", "*habbit - help | boost your productivity! 🌱", "*help | excel in your own pace! ⭐", "*habbit-help | time to work! 📚", "*help | reward yourself too! ☕"]

cogs = ['cogs.tracker','cogs.music','cogs.pomodoro','cogs.reminder'] # add more cogs here

for cog in cogs:
  try:
    client.load_extension(cog)
  except Exception as e:
    print(f'Unable to load cog {cog}: {str(e)}')

@client.event
async def on_ready():
  print('{0.user} has connected to Discord!'.format(client))
  print('Habbit is currently in ' + str(len(client.guilds)) + ' servers!')
  changeStatus.start()

@tasks.loop(minutes=8)
async def changeStatus():
    await client.change_presence(status = discord.Status.online, activity=discord.Game(choice(status)))
 
#--- Custom Help Pages ---#
@client.command(name='help', aliases=['habbit-help'])
async def help(ctx):

  invite = 'https://discord.com/api/oauth2/authorize?client_id=835746127231057990&permissions=2184703040&scope=bot'
  repo = 'https://github.com/manghann/Habbit.git'
  prefix = client.command_prefix  

  page1 = (discord.Embed(title = "Habbit | *Help Information*", description = "A Discord bot to help you build habits with your community and earn *carrot* points with every task you complete. This bot also includes some extra tools to boost your productivity!", color = discord.Color.orange())
       .add_field(name = " 📋 — To-do List\n⏰ — Reminder\n🎶 — Music Buddy\n🍅 — Pomodoro", value = '\u200b', inline = False)
       .add_field(name = " \u200b", value = f'**Command Prefix: ** {prefix}\n **Required** parameters are enclosed with < > while **optional** parameters are enclosed in brackets [ ].\n', inline = False)
       .add_field(name = "\n\nOther information", value = f"• Invite Habbit to your server [here]({invite}).\n• If you want to make a suggestion, report a bug, or reach out for the bot project, visit the repo [here]({repo}).\n\n**Disclaimer:** The bot send messages on the channel where the commands are being typed in so it's highly suggested to create separate text channels for Habbit's tools for a clean & organized look!", inline = False)
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(icon_url=ctx.author.avatar_url, text=f"Help 1/5 | Habbit is created by Hanna Mangampo (manghann_#0747) ☁️"))  

  page2 = (discord.Embed(title="📋 — To-do List", description=f"This tool features a to-do list that can handle up to ten tasks at once, as well as commands to *add*, *display*, and *complete* tasks on your personal list.\n\n\n**To-do Commands**\n`{prefix}mytasks` - Display your To-do List.\n`{prefix}add <description>` - Add a task to your list.\n`{prefix}edit <task_number> <new_description>` - Edit a task to your list.\n`{prefix}finish <task_number>` - Complete and remove a task from your list.\n\n`{prefix}mypoints` - Displays your current total points.\n`{prefix}daily` - Gives you free additional points every 12 hours.\n\nTo see who's leading and track your community member's points use `{prefix}leaderboard` or `{prefix}lead`.\n", colour=discord.Colour.orange())
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(icon_url=ctx.author.avatar_url, text="Help 2/5 | Reaction cooldown of 2 seconds •"))
  
  page3 = (discord.Embed(title="⏰ — Reminder", description=f"To help you not miss out an important meeting, event, or task, here's a simple reminder tool!\n\n\n**Reminder Commands:**\n`{prefix}remindme <time> <description>` - Creates a reminder.\n`{prefix}myreminders` - Displays your list of reminders. \n\n__**Note:**__ Required `time` parameter should be an integer followed by either **s**, **m**, **h**, or **d** which stands for seconds, minutes, hours, or days respectively as shown below:\n ```{prefix}remindme 5m Reminder Description```\n", colour=discord.Colour.orange())
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(icon_url=ctx.author.avatar_url, text="Help 3/5 | Reaction cooldown of 2 seconds •"))

  page4 = (discord.Embed(title="🎶 — Music Buddy", description=f"Whether it be during your working period or break time, music buddy is a great company!\n\n\n**Music Buddy Commands**\n`{prefix}summon [channel]` - Summons the bot to a voice channel.\n`{prefix}join`- Joins a voice channel.\n`{prefix}leave` - Clears the queue and leaves the voice channel.\n`{prefix}now` or `{prefix}playing`      - Displays the currently playing song.\n`{prefix}play <URL_or_phrase>` - Plays (and enqueues) a song.\n`{prefix}queue`- Shows what's currently playing & music buddy's queue.\n\n**Other Commands:**\n `{prefix}pause` `{prefix}resume` `{prefix}stop` `{prefix}shuffle` `{prefix}remove` `{prefix}loop`\n ", colour=discord.Colour.orange())
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")  
       .set_footer(icon_url=ctx.author.avatar_url, text="Help 4/5 | Reaction cooldown of 2 seconds •"))

  page5 = (discord.Embed(title="🍅 — Pomodoro", description=f"Pomodoro timer assists you and your peers in staying on track while studying together! Set a time to concentrate on your tasks and chat during the breaks.\n\n\n**Pomodoro Timer Commands**\nStart pomodoro session with optional custom settings (default values are 25 and 5) using\n```{prefix}pmdr-start [work_time] [break_time]```\nTo stop the ongoing timer use ```{prefix}pmdr-stop```", colour=discord.Colour.orange())
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
       .set_footer(icon_url=ctx.author.avatar_url, text="Help 5/5 | Reaction cooldown of 2 seconds •"))


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
            if reaction.emoji == u"🥕": pgnum = 0 
            elif reaction.emoji == u"📋": pgnum = 1  
            elif reaction.emoji == u"⏰": pgnum = 2
            elif reaction.emoji == u"🎶": pgnum = 3
            elif reaction.emoji == u"🍅": pgnum = 4

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            await msg.edit(embed = client.help_pages[pgnum])

keep_alive()
client.run(os.getenv('TOKEN'))  

