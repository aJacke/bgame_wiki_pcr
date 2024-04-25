import hoshino
from hoshino import R
from . import spider
import os

img_path = R.img("bwiki").path

HELP_STR = '''
日历 : 查看公主连结活动日历
'''.strip()

sv = hoshino.Service('bwiki日程', enable_on_default=False, help_=HELP_STR, bundle='bwiki日程')

@sv.scheduled_job('cron', hour='5')
async def get_and_send_calendar():
    await spider()
    msg = R.img(f'{img_path}\\date_cal.png').cqcode
    await sv.broadcast(msg)

@sv.on_fullmatch('日历')
async def cmd_send_calendar(bot, ev):
    if not os.path.exists(f'{img_path}\\date_cal.png'):
        await spider()
    msg = R.img(f'{img_path}\\date_cal.png').cqcode
    await bot.send(ev, msg)