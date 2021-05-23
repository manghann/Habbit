import discord
import pyrebase
import math
import datetime
import time
from discord.ext import commands
from collections import OrderedDict 


config = {
  "apiKey": "AIzaSyDRRANWbc40FBWLETEsqGRjhY2CcX1Ydos",
  "authDomain": "habbit-62caa.firebaseapp.com",
  "databaseURL": "https://habbit-62caa-default-rtdb.firebaseio.com",
  "storageBucket": "habbit-62caa.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Habbit_Tracker(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def add(self, ctx,*, task = None):
    global data, user_id, value, title
    user_id = ctx.message.author.id

    if task == None:
      await ctx.send(f"{ctx.author.mention}, **no task created**! Add one by typing `*add <description>`.")
 
    else:
      try:
        OrderedDict =  db.child("Users").child(user_id).child("Count").get().val()
        count = OrderedDict["Count"]

        if count > 10:
          await ctx.send(f"{ctx.author.mention}, chill~ You can only create **10** tasks at a time. Finish them first!")
          newcount = 1
          db.child("Users").child(str(user_id)).child("Count").set(newcount)   
                      
        else: 
          data={("Task "+str(count)):task}
          title="Task "+str(count)
          await ctx.send(f"{ctx.author.mention}, **task created**! Add some more by typing `*add <description>`.")
          db.child("Users").child(user_id).child("Count").set({"Count":int(count)+1})

      except:
        data={"Task 1": task}
        points={"Points": 0}
        count={"Count": 1}
        title = "Task 1"

        db.child("Users").child(str(user_id)).child("Points").set(points)
        db.child("Users").child(str(user_id)).child("Count").set(count)
      db.child("Users").child(str(user_id)).child(title).set(data)

  #---#
  @commands.command() # WIP
  async def edit(self, ctx, task = None, *,new_task = None):
    user_id = ctx.message.author.id    

    if  (task == None) or (new_task == None):
      await ctx.send(f"{ctx.author.mention}, **no task edited**! Try `*edit <task_number> <new_description>`.")

    else:
      print("Task:", task, "New Desc:", new_task)
      new_data={("Task "+str(task)):new_task}
      db.child("Users").child(user_id).child("Task " + str(task)).set(new_data)      
      await ctx.send(f"{ctx.author.mention}, **task edited**! Use `*mytasks` to see your updated to-do list.")

  #---#
  @commands.command()
  async def mytasks(self, ctx):
    user_id = ctx.message.author.id
    entries = db.child("Users").child(user_id).get().val()
    OrderedDict = db.child("Users").child(user_id).child("Count").get().val()
    #count = OrderedDict["Count"]

    task_list =[]
    try:
      td = ''
      for entry in entries:
        if (entry != "Count") and (entry != "Points"):
          OrderedDict=db.child("Users").child(user_id).child(entry).get().val()
          task_list.append(entry)
          print(entry)
          #show_tasks.add_field(name = entry, value = "•  " + OrderedDict[entry], inline = False)
          td += '**{}**: {}\n'.format(entry, OrderedDict[entry])
    
      show_td = (discord.Embed(title = '**Habbit** ━ *To-do List*   🗒️', description = f'You can add a task to your list by typing `*add <description>`!\n\n{td}', color=discord.Color.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
        .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
      show_td.timestamp = datetime.datetime.utcnow()   

      await ctx.send(embed = show_td)

    except:
        await ctx.send(f"{ctx.author.mention}, **no task avaiable**! You may create a new one using `.add <description>.`")

  @commands.command()
  async def finish(self, ctx,*, task = None):
      user_id = ctx.message.author.id
      OrderedDict=db.child("Users").child(user_id).child("Points").get().val()
      points = OrderedDict["Points"]

      emsg = f"{ctx.author.mention}, **no task found**! ***Usage:*** `*finish <task_number>`."
      
      if task == None:
        await ctx.send(emsg)   
      elif (task.isalpha()):
        await ctx.send(emsg)
    
      else:
          OrderedDict = db.child("Users").child(user_id).child("Count").get().val()
          count = OrderedDict["Count"]
          print(count)
          
          if (int(task) <= count) or (count == 1):
            db.child("Users").child(user_id).child("Task " + str(task)).remove()

            if points >= 100:
              username = ctx.author.display_name
              GG = discord.Embed(title = 'Good job~  '+ username +', ', description = f' A hundred 🥕 points! Enjoy this carrot cake worth of 20 points!  🥮\n\n You can also see your current standing & see who\'s leading through `*leaderboard` or `*lead`!', color = discord.Color.orange())
              await ctx.send(embed = GG)

              db.child("Users").child(user_id).child("Points").set({"Points": int(points) + 20}) 
              OrderedDict=db.child("Users").child(user_id).child("Points").get().val()
              points = OrderedDict["Points"]

            else:
              db.child("Users").child(user_id).child("Points").set({"Points": int(points) + 1})
              OrderedDict=db.child("Users").child(user_id).child("Points").get().val()
              points = OrderedDict["Points"]
          
            task_done = (discord.Embed(title = '**To-do List** ━ 🗒️',description = f'Task ' + task + ' finished! You now have '+str(points)+' 🥕!', colour = discord.Colour.orange()) 
              .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}')
              .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))   
            await ctx.send(embed=task_done)

          else:    
            await ctx.send(f"{ctx.author.mention}, **task not found**! ***Usage:*** `*finish <task_number>`")  

  # Temporarily replace quote function
  def noquote(s):
    return s
  pyrebase.pyrebase.quote = noquote

  @commands.command(name='leaderboard', aliases=['lead'])       # Displays leaderboard (top to bottom) 
  async def leaderboard(self, ctx, *, page: int = 1):      
    user_id=ctx.message.author.id
    all_user_ids = db.child("Users").shallow().get().val()      # Gets all UserID

    items_per_page = 10
    pages = math.ceil((len(all_user_ids)) / items_per_page)
    
    start = (page - 1) * items_per_page
    end = start + items_per_page

    leaderboard = []
    for userid in all_user_ids:         
        a = db.child("Users").child(userid).child("Points").get().val()  # points - value
        b = await ctx.bot.fetch_user(userid)
        user = str(b)
        points = a["Points"]

        lb = {'Name':user, 'Points':points}
        leaderboard.append(lb)  
        
    # Sort users by points (Descending order)
    leaderboard.sort(key=lambda x: x.get('Points'), reverse=True)

    leading = ''
    for rank, i in enumerate(leaderboard[start:end], start=start):
      leading += '**{}. {}** ━ `{} points`\n'.format(rank+1, i['Name'], i['Points'])

    leaderboard = (discord.Embed(title = '**Habbit** ━ *Leaderboard*   🏆', description = '**Habbit** is connected to different servers and \nhere are the standings so far: \n\n{}'.format(leading), color = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
        .set_footer(icon_url=ctx.author.avatar_url, text = '{} | Page {}/{} '.format(ctx.author.display_name,page, pages))) 
    leaderboard.timestamp = datetime.datetime.utcnow()   
    await ctx.send(embed=leaderboard) 

  @commands.command()
  async def mypoints(self, ctx):
    user_id = ctx.message.author.id
    OrderedDict = db.child("Users").child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]

    myPoints = (discord.Embed(title = '**Habbit** ━  *My Points*  🥕', description = "", colour = discord.Colour.orange())
      .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
      .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))    
    
    if points == 0:
      myPoints.add_field(name = '\u200b', value = f'Hey `{ctx.author.display_name}`, it looks like you recently got 100 points! Cool! For that, your points are back to 0. Time to work!', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send("Oops! you have no points yet.")
    else: 
      myPoints.add_field(name = '\u200b', value = f'Hey `{ctx.author.display_name}`, you currently have '+ str(points) +' 🥕. Nice!', inline = False)
      
      myPoints.timestamp = datetime.datetime.utcnow()
      await ctx.send(embed = myPoints)


  @commands.command(pass_context = True)
  @commands.cooldown(1, 60*60*12, commands.BucketType.user)
  async def daily(self, ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child("Users").child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    print(points)
    db.child("Users").child(user_id).child("Points").set({"Points" : int(points) + 3})

    daily = (discord.Embed(title = '**Habbit** ━  *Daily Points*  🥕', description = "Let's kick off your day~ Here is a gift... `3` 🥕!", colour = discord.Colour.orange())
    .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
    .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}')) 
    daily.timestamp = datetime.datetime.utcnow()      
    await ctx.send(embed=daily)

  @daily.error
  async def daily_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        daily_error = (discord.Embed(title = '**Habbit** ━  *Daily Points*  🥕', description = '', colour = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
        .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}')) 
        
        msg = 'This command is ratelimited, please try again after 12 hours!'.format(error.retry_after)              
        daily_error.add_field(name = f'️Did you just try and get extra points? ₍ᐢ｡ܫ｡ᐢ₎', value = f'*Oops!* '+msg, inline = False)
        daily_error.timestamp = datetime.datetime.utcnow()   
        await ctx.send(embed = daily_error)

    else:
        raise error  


def setup(client):
    client.add_cog(Habbit_Tracker(client))    