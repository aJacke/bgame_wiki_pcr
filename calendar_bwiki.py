import hoshino
from hoshino import R
from . import spider
import os

img_path = R.img("bwiki").path

HELP_STR = '''
日历 : 查看公主连结活动日历
'''.strip()

sv = hoshino.Service('bwiki日程', enable_on_default=False, help_=HELP_STR, bundle='bwiki日程')

async def get_calendar():
    await spider.spider()

@sv.scheduled_job('cron', hour='5')
async def daily_send_calendar():
    await get_calendar()
    msg = R.img(f'{img_path}\\date_cal.png').cqcode
    await sv.broadcast(msg)

@sv.on_rex(r'^(更新|)日历')
async def cmd_send_calendar(bot, ev):
    que_type = ev['match'].group(1)
    if not os.path.exists(f'{img_path}\\date_cal.png'):
        await get_calendar()
    if que_type == '更新':
        await get_calendar()
    msg = R.img(f'{img_path}\\date_cal.png').cqcode
    await bot.send(ev, msg)
