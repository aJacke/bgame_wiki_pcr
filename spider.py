from pyppeteer import launch
import asyncio
from hoshino import R
from PIL import Image

# 等待时长 网络较慢时可以调高 但不能太低
waittime = 5
# 最大重连次数
max_retries = 5
# 重试等待时间
retrytime = 5
FILE_PATH = R.img('bwiki').path

# 设置一个连接网页的函数，用于重连
async def web_connect(page, url):
    retries = 0
    while retries < max_retries:
        try:
            await page.goto(url, {'waitUntil': 'domcontentloaded'})
            break
        except Exception as e:
            print(f"页面加载失败: {e}, 正在重试")
            retries += 1
            await asyncio.sleep(retrytime)
    else:
        print(f"已到达最大重试次数，请检查网络链接并重试。")
        exit()
    return page

async def spider():
    browser = await launch(headless = True, defaultViewport={"width": 1600, "height": 1200}, args=['--disable-popup-blocking', '--window-size=1600,1200'])
    page = await browser.newPage()
    
    url = f'https://wiki.biligame.com/pcr/%E9%A6%96%E9%A1%B5'
    page = await web_connect(page, url)
    await asyncio.sleep(waittime)
    # 分辨率缩放比影响截图，推荐使用无头模式截图
    elements = await page.xpath(f'//div[text()="活动日历"]/../..')
    element = elements[0]
    await element.screenshot({
        'path': 'date_cal.png'
    })
    img = Image.open('date_cal.png')
    img.save(FILE_PATH + r'\date_cal.png')

asyncio.get_event_loop().run_until_complete(spider())