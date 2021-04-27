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
      no_task = discord.Embed(
        title = '🗒️ To-do List', 
        description = f'No task created. Add one!', 
        colour = discord.Colour.orange())
      await ctx.send(embed=no_task)
 
    else:
      try:
        OrderedDict = db.child(user_id).child("Count").get().val()
        count = OrderedDict["Count"]

        if count >= 11: 
          chill = discord.Embed(
            title = '🗒️ To-do List', 
            description = f'Chill~ 10 tasks at a time.', 
            colour = discord.Colour.orange())
          await ctx.send(embed=chill)
          db.child(user_id).child("Count").set({"Count":1})      
        else:  
          data={("Task "+str(count)):task}
          title="Task "+str(count)
          added = discord.Embed(
            title = '🗒️ To-do List', 
            description = f'Task added to list! ꉂ₍ᐢ﹘ܫ﹘ᐢ₎', 
            colour = discord.Colour.orange())
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
    

  @commands.command()
  async def show(self, ctx):
    user_id = ctx.message.author.id
    entries = db.child(user_id).get().val()
    OrderedDict = db.child(user_id).child("Count").get().val()
    count = OrderedDict["Count"]

    try:
        show_tasks = discord.Embed(
          title = '🗒️ To-do List', 
          description = f'', 
          colour = discord.Colour.orange())
        await ctx.send(embed = show_tasks) 

        for entry in entries:
            if (entry != "Count") and (entry != "Points"):
                OrderedDict=db.child(user_id).child(entry).get().val()
                await ctx.send(entry+": "+OrderedDict[entry])
                #print(entry)
                #print(OrderedDict[entry])
    except:
        await ctx.send('No More Tasks! 🥕')

  @commands.command()
  async def finish(self, ctx,*, task = None):
      user_id = ctx.message.author.id
      OrderedDict=db.child(user_id).child("Points").get().val()
      points = OrderedDict["Points"]
      
      no_task = discord.Embed(
        title = '🗒️ To-do List', 
        description = f'No task found.', 
        colour = discord.Colour.orange())

      if task == None:
        await ctx.send(embed=no_task)   
      elif (task.isalpha()):
        await ctx.send(embed=no_task)
      # another condition for inputs unavailable
      elif (len(task) > 2): # An option to finish multiple pending tasks
        db.child(user_id).child("Task " + str(task)).remove()
        pts = (len(task)-1)
        db.child(user_id).child("Points").set({"Points" : int(points) + int(pts)})
        OrderedDict=db.child(user_id).child("Points").get().val()
        points = OrderedDict["Points"]
        
        task_done = discord.Embed(
          title = '🗒️ To-do List', 
          description = f'Tasks ' + task + " finished! + "+str(pts)+' !\n You now have ' + str(points) + '🥕!',
          colour = discord.Colour.orange()) 
        await ctx.send(embed=task_done)  
    
      else:
        try:
          db.child(user_id).child("Task " + str(task)).remove()
          db.child(user_id).child("Points").set({"Points": int(points) + 1})
          OrderedDict=db.child(user_id).child("Points").get().val()
          points = OrderedDict["Points"]
          task_done = discord.Embed(
            title = '🗒️ To-do List', 
            description = f'Task ' + task + ' finished! You now have '+str(points)+' 🥕!',
            colour = discord.Colour.orange()) 
          await ctx.send(embed=task_done)

        except:
          no_task = discord.Embed(
            title = '🗒️ To-do List', 
            description = f'No task found.', 
            colour = discord.Colour.orange())
          await ctx.send(embed=no_task)  

  # ADD leaderboards

  @commands.command()
  async def mypoints(self, ctx, user: discord.User = None):
    user_id = ctx.message.author.id
    OrderedDict = db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    
    if user == None:
      no_user = discord.Embed(title = '🥕 My Points', description = "Please provide a user to get info on!", colour = discord.Colour.orange())
      await ctx.send(embed=no_user)

    myPoints = discord.Embed(title = '🥕 My Points', description = "", colour = discord.Colour.orange())

    if points == 0:
      myPoints.add_field(name = f'Hey {user.name},', value = f'Oops! you have no points yet.', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send("Oops! you have no points yet.")
    elif points >= 100:  
      myPoints.add_field(name = f'Hey {user.name},', value = f'Good job~ A hundred 🥕 points!', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send('Good job! A hundred 🥕 points!')
      db.child(user_id).child("Points").set({"Points": 0}) # resets after reaching 100
      points = OrderedDict["Points"]
    else: 
      myPoints.add_field(name = f'{user.name}', value = f'Nice~ You have '+str(points)+' 🥕!', inline = False)
      await ctx.send(embed = myPoints)
      #await ctx.send("Nice~ You have "+str(points)+" 🥕!")

  @commands.command(pass_context = True)
  @commands.cooldown(1, 60*60*12, commands.BucketType.user)
  async def daily(self, ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    db.child(user_id).child("Points").set({"Points" : int(points) + 3})
    await ctx.send('Here is a gift... 3 🥕!')

  @daily.error
  async def daily_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Did you just try and get extra points? ₍ᐢ｡ܫ｡ᐢ₎')
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error  



def setup(client):
    client.add_cog(Habbit_Tracker(client))    