import discord
import datetime

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils import get_expire_time

sched = AsyncIOScheduler()
sched.start()

class Pomodoro(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command(name='pmdr-start')
  async def start_pomodoro_timer(self,ctx, work_time: int = None, break_time: int = None):
    """ Start pomodoro timer
    Action:
        Start break_time timer after work_time timer
    Args:
        work_time : work timer (minute)
        break_time : break timer after work_time (minute)
    """    
    # Check if Pomodoro is already working
    if len(sched.get_jobs()) > 0:
        started = (discord.Embed(title="**Pomodoro Timer** ━ *Start*  🍅", description="Pomodoro timer is already working! \nLet's wait for it to finish. ₍ ᐢ. ̫ .ᐢ ₎و", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may also use `*pmdr-stop`.')
                 .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
                 .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
        started.timestamp = datetime.datetime.utcnow()         
        await ctx.send(embed=started)
        return        

    # Sets default timer values if parameters are not satisfied
    if work_time == None:
        work_time = 25
        break_time = 5
    
    # Actions
    async def break_schedule(work_time, break_time):
        bt_end = (discord.Embed(title="**Pomodoro Timer** ━ *Work Time*  🍅", description=f"{ctx.author.mention} , break time's over! \nLet's get back to work! ₍ ᐢ. ̫ .ᐢ ₎و✺", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.')
                 .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
                 .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))   
        bt_end.timestamp = datetime.datetime.utcnow()              
        await ctx.send(embed=bt_end)        

        work_expire_time = get_expire_time(work_time)
        sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[
                      work_time, break_time], misfire_grace_time=300)                      
        pass

    async def work_schedule(work_time, break_time):
        wt_end = (discord.Embed(title="**Pomodoro Timer** ━ *Short Break Time*  🍅", description=f"{ctx.author.mention} , work time's over! \nEnjoy your break! ₍ ᐢ. ̫ .ᐢ ₎و ♡", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.')
                 .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
                 .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
        wt_end.timestamp = datetime.datetime.utcnow()                         
        await ctx.send(embed=wt_end)            

        break_expire_time = get_expire_time(break_time)
        sched.add_job(break_schedule, 'date', run_date=break_expire_time,
                      args=[work_time, break_time], misfire_grace_time=300)
        pass

    work_expire_time = get_expire_time(work_time)
    sched.add_job(work_schedule, 'date', run_date=work_expire_time,
                  args=[work_time, break_time], misfire_grace_time=300)

    start = (discord.Embed(title="**Pomodoro Timer** ━ *Start*  🍅", description=f"**Work Time:** `{work_time} mins` | **Break Time:** `{break_time} mins`", color=discord.Color.orange())
            .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.', inline=False)
            .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png") 
            .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
    start.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=start)


  @commands.command(name='pmdr-stop')       # Stops Pomodoro timer.
  async def stop_pomodoro_timer(self, ctx):
    if len(sched.get_jobs()) > 0:
      sched.remove_all_jobs()
      stop = (discord.Embed(title="**Pomodoro Timer** ━ *Stop*  🍅", description=f"☒ Pomodoro timer is **stopped** by `{ctx.author.name}`!", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'If you want to set a timer again, \nuse `*pmdr-start [work_mins] [break_mins]`.')
                 .set_thumbnail(url = "https://i.imgur.com/Hy5KW52.png")
                 .set_footer(icon_url=ctx.author.avatar_url, text = f'{ctx.author.display_name}'))
      stop.timestamp = datetime.datetime.utcnow()           
      await ctx.send(embed=stop)
    else:
      await ctx.send(f"{ctx.author.mention}, **timer is already stopped**! You should start the timer before you can stop it!")


def setup(client):
    client.add_cog(Pomodoro(client))      