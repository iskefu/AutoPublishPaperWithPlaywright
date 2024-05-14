import asyncio
import os
import re
from playwright.async_api import Playwright, async_playwright, expect
import pyautogui
import pyperclip
from dotenv import load_dotenv
load_dotenv()
from func.title_content import content, title

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
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
            print('wait for user img locator:', logined_element)
        
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
    name = title(file_path)
    await page1.frame_locator("div.iframe-comp-container iframe").locator("textarea").fill(name)
    
    # content
    cont = content(file_path)
    await page1.frame_locator("div.iframe-comp-container iframe").locator("div.ql-editor.ql-blank").fill(cont)

    await page1.frame_locator("div.iframe-comp-container iframe").get_by_text("更多设置").click()
    await page1.frame_locator("div.iframe-comp-container iframe").get_by_role("checkbox", name="我声明此文章为原创").click()
    await page1.frame_locator("div.iframe-comp-container iframe").locator(".bre-modal__close").click()
    await page1.frame_locator("div.iframe-comp-container iframe").get_by_role("button", name="提交文章").click()
    await page1.frame_locator("div.iframe-comp-container iframe").locator(".success-image").wait_for()
    await page1.wait_for_timeout(1000)
    await browser.close()
    
async def bilibili(file_path,cover_path) -> None:
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = os.getenv('FILE_PATH')
    cover_path=os.getenv('COVER_PATH')
    asyncio.run(bilibili(file_path,cover_path))
