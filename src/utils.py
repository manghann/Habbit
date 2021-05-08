import datetime
import re
from discord.ext import commands
from datetime import timezone


# POMODORO
def get_expire_time(minutes: int) -> datetime.datetime:
    """ get expire time after minutes from now
    args
        minutes: int
    return
        expire_time: datetime.datetime
    """
    now = datetime.datetime.now()
    expire_time = now + datetime.timedelta(minutes=minutes)
    return expire_time

def sched():
  sched = AsyncIOScheduler()
  async def on_ready():
    sched.start()  
