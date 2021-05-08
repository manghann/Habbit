import discord
import datetime
import asyncio
import math
from discord.ext import commands

import pyrebase
from collections import OrderedDict 

config = {
  "apiKey": "AIzaSyDRRANWbc40FBWLETEsqGRjhY2CcX1Ydos",
  "authDomain": "habbit-62caa.firebaseapp.com",
  "databaseURL": "https://habbit-62caa-default-rtdb.firebaseio.com",
  "storageBucket": "habbit-62caa.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Reminder(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def remindme(self, ctx, time, *, description):
    user_id = ctx.message.author.id

    emsg = f"{ctx.author.mention}, **no reminder created**! Add one by typing `*remindme <time> <description>`. *Note:* Time must be an integer."
 

    def convert(time):
      pos = ['s', 'm', 'h', 'd']
      time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
      unit = time[-1]

      if unit not in pos:
        return -1      
      try:
          val = int(time[:-1])
      except:
          return -2
 
      return val * time_dict[unit]  

    converted_time = convert(time)

    if (description == None) or (time == None):
      await ctx.send(emsg)
    if (converted_time == -1):
      await ctx.send(emsg)
      return
    if converted_time == -2:
      await ctx.send(emsg) 
      return

    db.child("Reminder-Users").child(str(user_id)).child("Reminders").child(str(time)).set(description)
    await ctx.send(f"{ctx.author.mention}, **got it**! Will be reminding you of `{description}` in **{time}**!")

    await asyncio.sleep(converted_time)

    reminder = (discord.Embed(title="**Reminders** ━ *What's up?*  📅", description=f"`TODAY`\n**Description:** {description}\n**Reminder for:** {ctx.author.mention}", color=discord.Color.orange())
      .add_field(name='\u200b', value = 'For other commands use `*help`.')
      .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
      .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
    reminder.timestamp = datetime.datetime.utcnow()        
    
    await ctx.send(embed=reminder)
    db.child("Reminder-Users").child(str(user_id)).child("Reminders").child(str(time)).remove()

    #await ctx.send(f"{ctx.author.mention} your reminder for `{description}`.")

  @commands.command()
  async def myreminders(self, ctx, page: int = 1):
    user_id = ctx.message.author.id
    
    reminders=db.child("Reminder-Users").child(str(user_id)).child("Reminders").get().val()
    print(reminders)

    res = ''
    for i, (k, v) in enumerate(reminders.items()):
      print(i, k, v)
      res += '**{}. {}** in `{}`\n'.format(i+1, v, k)

    my_reminders = (discord.Embed(title = "**Reminders** ━ *What's up?*  📅", description = '{}, some reminders for you:\n\n{}\n\nHope you don\'t miss something important!'.format(ctx.author.mention, res), color = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
        .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
    my_reminders.timestamp = datetime.datetime.utcnow()   
    await ctx.send(embed=my_reminders) 

  @commands.command()
  async def delreminder(self, ctx,*, reminder = None):
    user_id = ctx.message.author.id
    reminders=db.child("Reminder-Users").child(str(user_id)).child("Reminders").get().val()

    emsg = f"{ctx.author.mention}, **no reminder found**! Try `*delreminder <reminder number>`."

    if reminder == None:
      await ctx.send(emsg)   
    elif (reminder.isalpha()):
      await ctx.send(emsg)
    else:
      print('test delete reminder')


def setup(client):
    client.add_cog(Reminder(client))    