import discord
import pyrebase
from discord.ext import commands
#from collections import OrderedDict 

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
    #user = db.child(user_id).get()

    if task == None:
      await ctx.send('No task created. Add one!')
    else:
      try:
        OrderedDict = db.child(user_id).child("Count").get().val()
        count = OrderedDict["Count"]
        data={("Task "+str(count+1)):task}
        title="Task "+str(count+1)
        db.child(user_id).child("Count").set({"Count":int(count)+1})
      
      except:
        data={"Task 1": task}
        points={"Points": 0}
        count={"Count": 1}
        title = "Task 1"
        db.child(str(user_id)).child("Points").set(points)
        db.child(str(user_id)).child("Count").set(count)
    db.child(str(user_id)).child(title).set(data)
    #await ctx.send(data)
    await ctx.send('Task added to list! ꉂ₍ᐢ﹘ܫ﹘ᐢ₎')

  @commands.command()
  async def show(self, ctx):
    user_id = ctx.message.author.id
    entries = db.child(user_id).get().val()
    OrderedDict=db.child(user_id).child("Count").get().val()
    count = OrderedDict["Count"]

    try:
        await ctx.send('TO-DO List:')
        for entry in entries:
            if (entry != "Count") and (entry != "Points"):
            #if (entry == "Count"):
                OrderedDict=db.child(user_id).child(entry).get().val()
                await ctx.send(entry+": "+OrderedDict[entry])
    except:
        await ctx.send("No More Tasks! Here's a 🥕 for you!")

  @commands.command()
  async def finish(self, ctx, task):
      user_id = ctx.message.author.id
      OrderedDict=db.child(user_id).child("Points").get().val()
      points = OrderedDict["Points"]
     
      # need to have an option to finish ALL pending tasks  
          
      if task == "All":
        await ctx.send("All tasks removed. charrr")
        db.child(user_id).child("Task " + str(task)).remove()
        # count finished tasks
        # add total points here

      else:  
        try:
          db.child(user_id).child("Task " + str(task)).remove()
          await ctx.send('Yay!~ Now on to the next task!')
          db.child(user_id).child("Points").set({"Points" : int(points) + 1})
          OrderedDict=db.child(user_id).child("Points").get().val()
          points = OrderedDict["Points"]
          await ctx.send("Task " + task + " finished! You have "+str(points)+' 🥕!')
        except:
            await ctx.send("Task not found. Enter a task number, please!")
      
  @commands.command()
  async def lead(self,ctx):
    user_id = ctx.message.author.id  
    await ctx.send('Here are the standings so far:')
    clan = db.shallow().get().val()
    
    for usernum in clan:
      a = db.child(usernum).child("Points").get().val()
      b = str(ctx.bot.get_user(int(usernum)))
      points = a["Points"]
      if b == "None": b = "Someone in your server "
      await ctx.send( str(b) + ": " + str(points) + " Points")
    await ctx.send('Keep it up! ʚ₍⑅ᐢ‸ ̫ ‸ᐢ₎ɞ')

  @commands.command()
  async def mypoints(self, ctx):
    user_id = ctx.message.author.id
    OrderedDict = db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    if points == 0:
      await ctx.send("Oops! you have no points yet.")
    else: 
      await ctx.send("Nice~ You have "+str(points)+" 🥕!")

  @commands.command(pass_context = True)
  @commands.cooldown(1, 60*60*12, commands.BucketType.user)
  async def daily(self, ctx):
    user_id=ctx.message.author.id
    OrderedDict=db.child(user_id).child("Points").get().val()
    points = OrderedDict["Points"]
    db.child(user_id).child("Points").set({"Points" : int(points) + 3})
    await ctx.send('Here is a gift... +3 🥕!')

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