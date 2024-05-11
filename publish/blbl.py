import asyncio
import os
import re
from playwright.async_api import Playwright, async_playwright, expect
import pyautogui
import pyperclip

from publish.func.title_content import content, title

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/bilibili-mp-auth.json'
    if os.path.exists(ss_file):
        print('Loading state from', ss_file, '\n')
        context =await browser.new_context(storage_state=ss_file)
    else:
        print('No state file found, creating new context', '\n')
        context = await browser.new_context()

    # create new page
    page=await context.new_page()
    page.set_default_timeout(600*1000)

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
    
    # 保存登陆状态
    await page.wait_for_load_state('load')
    await context.storage_state(path=ss_file)
    print('save state to', ss_file)
    
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
    file_path = '/run/media/kf/data/obsidian/4-Archives/自动化发布文章脚本/Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(bilibili(file_path,cover_path))
