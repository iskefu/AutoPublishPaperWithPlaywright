import asyncio
import os
import random
import re
from playwright.async_api import Playwright, async_playwright, expect
from dotenv import load_dotenv
load_dotenv()
from func.title_content import content, title

async def init_browser(playwright):    
    
        # 打开浏览器
        browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=f'data',
        executable_path=os.getenv('CHROME_BIN'),
        # 要想通过这个下载文件这个必然要开  默认是False
        accept_downloads=True,
        # 设置不是无头模式
        headless=False,
        bypass_csp=True,
        slow_mo=10,
        #跳过检测
        args=['--disable-blink-features=AutomationControlled']
        )
        browser.set_default_timeout(60*1000)
        return browser

def get_title(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename 

def get_content(filepath):
    with open(filepath, 'r',encoding='utf-8') as f:
        content = f.read()
    return content
def get_cover(folder_path):
    # 列出文件夹下所有的文件名
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # 筛选出图片文件，这里以.jpg和.png为例
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # 随机选择一张图片
    random_image = random.choice(images) if images else None
    # 返回图片的完整路径
    return os.path.join(folder_path, random_image) if random_image else None

async def bilibili(file_path) -> None:
    async with async_playwright() as playwright:
            
        browser =await init_browser(playwright)
        page=await browser.new_page()

        # go to url
        url='https://www.bilibili.com/'
        await page.goto(url)
        await page.wait_for_load_state('load')

        #  if login
        logined_element = '.v-popover-wrap.header-avatar-wrap'
        is_login = await page.is_visible(logined_element)
        if not is_login:
            try:
                await page.get_by_text("登录", exact=True).click()
                await page.locator("div").filter(has_text=re.compile(r"^微信登录$")).click()
                await page.wait_for_selector(logined_element)
            except Exception as e:
                print('login failed, try again \n error:', e)
                await page.close()
                return
        
        # publish

        async with page.expect_popup() as p1_info:
            await page.get_by_role("link", name="投稿", exact=True).click()
        page1 = await p1_info.value
        await page1.wait_for_load_state('load')
        
        await page1.locator("#video-up-app").get_by_text("专栏投稿").click()

        # title
        name = get_title(file_path)
        await page1.frame_locator("div.iframe-comp-container iframe").locator("textarea").fill(name)
        
        # content
        cont = get_content(file_path)
        await page1.frame_locator("div.iframe-comp-container iframe").locator("div.ql-editor.ql-blank").fill(cont)

        # origin
        await page1.frame_locator("div.iframe-comp-container iframe").get_by_text("更多设置").click()
        await page1.frame_locator("div.iframe-comp-container iframe").get_by_role("checkbox", name="我声明此文章为原创").click()
        await page1.frame_locator("div.iframe-comp-container iframe").locator(".bre-modal__close").click()

        # cover
        page1.on("filechooser", lambda file_chooser: file_chooser.set_files(get_cover(os.getenv('COVER_PATH'))))
        await page1.frame_locator("div.iframe-comp-container iframe").locator(".bre-settings__coverbox__img").click()
        await page1.frame_locator("div.iframe-comp-container iframe").get_by_role("button", name="确定").click()
        await page1.frame_locator("div.iframe-comp-container iframe").get_by_role("button", name="提交文章").click()
        await page1.frame_locator("div.iframe-comp-container iframe").locator(".success-image").wait_for()
        await browser.close()

if __name__ == '__main__':
    file_path = os.getenv('FILE_PATH')
    
    asyncio.run(bilibili(file_path))
