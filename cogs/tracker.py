import discord
import pyrebase
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
      no_task = (discord.Embed(title = '**To-do List** ━ 🗒️', description = f'No task created.\nAdd one by typing `*add <task>`!', colour = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))
      await ctx.send(embed=no_task)
 
    else:
      try:
        OrderedDict = db.child(user_id).child("Count").get().val()
        count = OrderedDict["Count"]

        if count >= 11: 
          chill = (discord.Embed(title = '**To-do List** ━ 🗒️', description = f'Chill~ You can only create **10** tasks at a time. Finish them first!', colour = discord.Colour.orange())
            .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url))    
          db.child(user_id).child("Count").set({"Count":1}) 
          await ctx.send(embed=chill)
               
        else: 
          data={("Task "+str(count)):task}
          title="Task "+str(count) 
          added = (discord.Embed(title = '**To-do List** ━ 🗒️', description = f'Task added to list! ꉂ₍ᐢ﹘ܫ﹘ᐢ₎', colour = discord.Colour.orange())
          .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)  
          .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))

          await ctx.send(embed=added)
          db.child(user_id).child("Count").set({"Count":int(count)+1})
      except:
        data={"Task 1": task}
        points={"Points": 0}
        count={"Count": 1}
        title = "Task 1"
        db.child(str(user_id)).child("Points").set(points)
        db.child(str(user_id)).child("Count").set(count)
      db.child(str(user_id)).child(title).set(data)
      #print(db.child(str(user_id)).child(title).set(data))

  #---#
  @commands.command()
  async def edit(self, ctx,*, new_task = None, task = None):
    global data, user_id, value, title
    user_id = ctx.message.author.id    

    if (task == None) or (new_task == None):
      no_task = (discord.Embed(title = '**To-do List** ━ 🗒️', description = f'No task edited. Try `*edit <tasknumber> <newtask>`!', colour = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))
      await ctx.send(embed=no_task)
    else:
      print("test")

  #---#


  @commands.command()
  async def show(self, ctx):
    user_id = ctx.message.author.id
    entries = db.child(user_id).get().val()

    OrderedDict = db.child(user_id).child("Count").get().val()
    count = OrderedDict["Count"]
    #print(count)
    task_list = []

    show_tasks = (discord.Embed(title = '**To-do List** ━ 🗒️', description = 'You can add a task to your list by typing `*add <task>`!\n\n', color=discord.Color.orange())
          #.set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
          .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))
          



    try:
      for entry in entries:
        if (entry != "Count") and (entry != "Points"):
          OrderedDict=db.child(user_id).child(entry).get().val()
          task_list.append(entry)
          print(entry)
          show_tasks.add_field(name = entry, value = "•  " + OrderedDict[entry], inline = False)
      await ctx.send(embed = show_tasks)

    except:
        show_tasks.add_field(name=f'No More Tasks! 🥕', value="You may create a new one using `.add' <task>!", inline = False)
        await ctx.send(embed=show_tasks)

  @commands.command()
  async def finish(self, ctx,*, task = None):
      user_id = ctx.message.author.id
      OrderedDict=db.child(user_id).child("Points").get().val()
      points = OrderedDict["Points"]
      
      no_task = (discord.Embed(title = '**To-do List** ━ 🗒️', description = f'No task found. Try a different number please~', color = discord.Color.orange())
        .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url)
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))

      if task == None:
        await ctx.send(embed=no_task)   
      elif (task.isalpha()):
        await ctx.send(embed=no_task)
    
      else:
          OrderedDict = db.child(user_id).child("Count").get().val()
          count = OrderedDict["Count"]
          print(count)
          
          if (int(task) <= count) or (count == 1):
            db.child(user_id).child("Task " +str(task)).remove()

            if points >= 1:
              username = ctx.author.display_name
              GG = discord.Embed(title = 'Good job~  '+ username +', ', description = f' A hundred 🥕 points! Enjoy this carrot cake!  🥮', color = discord.Color.orange())
              await ctx.send(embed = GG)
              db.child(user_id).child("Points").set({"Points": 0}) # resets after reaching 100
              points = OrderedDict["Points"]

            else:
              db.child(user_id).child("Points").set({"Points": int(points) + 1})
              OrderedDict=db.child(user_id).child("Points").get().val()
              points = OrderedDict["Points"]
          
            task_done = (discord.Embed(title = '**To-do List** ━ 🗒️',description = f'Task ' + task + ' finished! You now have '+str(points)+' 🥕!', colour = discord.Colour.orange())
              .set_author(name=ctx.author.display_name +"'s", url=" ", icon_url=ctx.author.avatar_url) 
              .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))   
            await ctx.send(embed=task_done)

          else:       
            await ctx.send(embed=no_task)  

  @commands.command(name='leaderboard', aliases=['lead'])
  async def leaderboard(self, ctx): # Displays leaderboard (top to bottom)
    #user_id=ctx.message.author.id
    #print(user_id)
           
    lead = (discord.Embed(title = '**Habbit** ━ *Leaderboard*   🏆',description = f'Here are the standings so far:\n', color = discord.Colour.orange())
       .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))

    all_user_ids = db.shallow().get().val()
    print(all_user_ids)

    for user_id in all_user_ids:
           
      a = db.child(user_id).child("Points").get().val()
      b = str(ctx.bot.get_user(int(user_id)))
      #user = user_id
      user = await ctx.guild.fetch_member(user_id) 
      points = a["Points"]

      i = 1
      print(points)

      if b == "None": 
        b = f"**{i}**. "
        i = i+1

      lead.add_field(name='\u200b', value = f"{b} **{user}** - `{points} points`", inline = False)
      #await ctx.send(str(b) + str(points) + " Points")  

    lead.add_field(name = "\u200b", value = '\nGG! Keep it up!', inline = False)
    await ctx.send(embed=lead) 
  
  @commands.command()
  async def mypoints(self, ctx, user: discord.User = None):
    user_id = ctx.message.author.id
    OrderedDict = db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    
    if user == None:
      no_user = (discord.Embed(title = '**Habbit** ━  *My Points*  🥕', description = "Please provide a user to get info on!", colour = discord.Colour.orange())
      .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))

      await ctx.send(embed=no_user)

    myPoints = (discord.Embed(title = '**Habbit** ━  *My Points*  🥕', description = "", colour = discord.Colour.orange())
      .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png"))    
    
    if points == 0:
      myPoints.add_field(name = f'\u200b', value = f'Hey `{user.name}`, it looks like you recently got 100 points! Cool! For that, your points are back to 0. Time to work!', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send("Oops! you have no points yet.")
    elif points >= 100:  
      myPoints.add_field(name = f'\u200b,', value = f'Hey `{user.name}`, Good job~ A hundred 🥕 points! It\'s time to reward yourself!', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send('Good job! A hundred 🥕 points!')
      db.child(user_id).child("Points").set({"Points": 0}) # resets after reaching 100
      points = OrderedDict["Points"]
    else: 
      myPoints.add_field(name = f'\u200b', value = f'Hey `{user.name}`, you currently have '+ str(points) +' 🥕. Nice!', inline = False)
      
      await ctx.send(embed = myPoints)
      #await ctx.send("Nice~ You have "+str(points)+" 🥕!")

  @commands.command(pass_context = True)
  @commands.cooldown(1, 60*60*12, commands.BucketType.user)
  async def daily(self, ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    db.child(user_id).child("Points").set({"Points" : int(points) + 3})

    daily = (discord.Embed(title = '**Habbit** ━  *Daily Points*  🥕', description = "Let's kick off your day~ Here is a gift... `3` 🥕!", colour = discord.Colour.orange())
    .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")) 
       
    await ctx.send(embed=daily)

  @daily.error
  async def daily_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        daily_error = (discord.Embed(title = '**Habbit** ━  *Daily Points*  🥕', description = '', colour = discord.Colour.orange())
        .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")) 
        
        msg = 'This command is ratelimited, please try again after 12 hours!'.format(error.retry_after)              
        daily_error.add_field(name = f'️Did you just try and get extra points? ₍ᐢ｡ܫ｡ᐢ₎', value = f'*Oopsie!* '+msg +' !', inline = False)
        await ctx.send(embed = daily_error)
        #await ctx.send(msg)
    else:
        raise error  


def setup(client):
    client.add_cog(Habbit_Tracker(client))    