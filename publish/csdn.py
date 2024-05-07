import asyncio
import os
import re
from playwright.async_api import Playwright, async_playwright, expect
import pyautogui
import pyperclip
from func.get_cover import get_random_image
from func.md_to_doc import md_to_doc
from func.title_content import content, title

async def run(playwright: Playwright, filepath: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/csdn-mp-auth.json'
    if os.path.exists(ss_file):
        print('Loading state from', ss_file, '\n')
        context =await browser.new_context(storage_state=ss_file)
    else:
        print('No state file found, creating new context', '\n')
        context = await browser.new_context()

    # create new page
    page=await context.new_page()
    # page.set_default_timeout(600*1000)

    # go to url
    url='https://www.csdn.net'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = 'a.hasAvatar'
    is_login = await page.is_visible(logined_element)
    
    if not is_login:
        try:
            await page.get_by_text("登录", exact=True).click()
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
    
    await page.get_by_role('link', name='发布', exact=True).click()
    await page.wait_for_load_state('load')
    
    async with page.expect_popup() as p1_info:
        await page.get_by_label("使用 MD 编辑器").click()
    page1 = await p1_info.value
    await page1.wait_for_load_state('load')
    await page1.locator("#import-markdown-file-input").set_input_files(file_path)
    
    await page1.get_by_role('button', name='发布文章').click()
    await page1.get_by_role('button', name='添加文章标签').hover()
    await page1.wait_for_timeout(1000)
    await page1.locator(".el-tag.el-tag--light").first.click()
    await page1.locator('.mark_selection_box_body button').click()
    await page1.locator('.modal__button-bar button').last.click()
    
    await page1.wait_for_selector('a.success-modal-btn')
    await browser.close()
    
    
    
    
    
    
async def csdn(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = '/run/media/kf/data/obsidian/4-Archives/自动化发布文章脚本/Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(csdn(file_path,cover_path))
