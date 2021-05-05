import discord
from discord.ext import commands
import os
import platform
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from src.utils import get_expire_time
#from src.utils import sched

sched = AsyncIOScheduler()
sched.start()


class Pomodoro(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command(name='pmdr-start')
  async def start_pomodoro_timer(self,ctx, work_time: int, break_time: int):
    """ Start pomodoro timer
    Action:
        Start break_time timer after work_time timer
    Args:
        work_time : work timer (minute)
        break_time : break timer after work_time (minute)
    """
    if len(sched.get_jobs()) > 0:
        started = (discord.Embed(title="**Pomodoro Timer** ━ *Start*  🍅", description="Pomodoro timer is already working! Let's wait for it to finish. ₍ ᐢ. ̫ .ᐢ ₎و", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may also use `*pmdr-stop`.')
                 .set_footer(text='━━━━━━━━━━━━━━━━━━━━━━━━━ '))
        await ctx.send(embed=started)
        return

    async def break_schedule(work_time, break_time):
        bt_end = (discord.Embed(title="**Pomodoro Timer** ━ *Work Time*  🍅", description=f"{ctx.author.mention} , break time's over! Let's get back to work! ₍ ᐢ. ̫ .ᐢ ₎و ️☁", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.')
                 .set_footer(text='━━━━━━━━━━━━━━━━━━━━━━━━━ '))        
        await ctx.send(embed=bt_end)        
        #await ctx.channel.send(f"{ctx.author.mention}```css\n[🔥Break time end!] Let's work :)```")
        work_expire_time = get_expire_time(work_time)
        sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[
                      work_time, break_time], misfire_grace_time=300)
        pass

    async def work_schedule(work_time, break_time):
        wt_end = (discord.Embed(title="**Pomodoro Timer** ━ *Break Time*  🍅", description=f"{ctx.author.mention} , work time's over! Enjoy your break! ₍ ᐢ. ̫ .ᐢ ₎و ♡", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.')
                 .set_footer(text='━━━━━━━━━━━━━━━━━━━━━━━━━ '))        
        await ctx.send(embed=wt_end)            
        
        #await ctx.channel.send(f"{ctx.author.mention}```css\n[🏁Work time end!] Let's break :)```")
        break_expire_time = get_expire_time(break_time)
        sched.add_job(break_schedule, 'date', run_date=break_expire_time,
                      args=[work_time, break_time], misfire_grace_time=300)
        pass

    work_expire_time = get_expire_time(work_time)
    sched.add_job(work_schedule, 'date', run_date=work_expire_time,
                  args=[work_time, break_time], misfire_grace_time=300)

    start = (discord.Embed(title="**Pomodoro Timer** ━ *Start*  🍅", description=f"**Work Time:** `{work_time} mins` | **Break Time:** `{break_time} mins`", color=discord.Color.orange())
            #.add_field(name='Work Time', value=f'`{work_time} mins`', inline = True)
            #.add_field(name='Break Time', value=f'`{break_time} mins`', inline = True)
            .add_field(name='\u200b', value = 'You may opt use `*pmdr-stop` anytime.', inline=False)
            .set_footer(text='━━━━━━━━━━━━━━━━━━━━━━━━━ '))

    await ctx.send(embed=start)
    #await ctx.channel.send(f"```css\n[Work {work_time}min, Break {break_time}min] Pomodoro Timer START.\n - stop command : !pmdr_stop```")
        
  @commands.command(name='pmdr-stop')  
  async def stop_pomodoro_timer(self, ctx):
    # Stop pomodoro timer
      sched.remove_all_jobs()
      stop = (discord.Embed(title="**Pomodoro Timer** ━ *Stop*  🍅", description=f"☒ Pomodoro timer is **stopped** by `{ctx.author.name}`!", color=discord.Color.orange())
                 .add_field(name='\u200b', value = 'If you want to set a timer again, use `*pmdr-start <work_mins> <break_mins>`.')
                 .set_footer(text='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ '))
      await ctx.send(embed=stop)


      #await ctx.channel.send(f"```css\nPomodoro Timer STOP.\n - start command : *pmdr_start [work_min] [break_min]```")
        


def setup(client):
    client.add_cog(Pomodoro(client))      