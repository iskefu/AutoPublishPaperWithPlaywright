import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect
import pyperclip
from func.get_cover import get_random_image
from func.md_to_doc import md_to_doc
from func.md_to_html import md_to_html
from func.title_content import content, title

async def run(playwright: Playwright, filepath: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/jianshu-mp-auth.json'
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
    url='https://www.jianshu.com'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = 'div.user'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.locator("#sign_in").click()
            async with page.expect_popup() as p1_info:
                await page.locator("a.weixin").click()
            page1 = await p1_info.value
            await page1.wait_for_selector(logined_element)
            print('wait for user img locator:', logined_element)
        
        except Exception as e:
            print('login failed, try again \n error:', e)
            await page.close()
            return
    
    # 保存登陆状态
    await page.wait_for_load_state('load')
    await context.storage_state(path=ss_file)
    print('save state to', ss_file)

    # 打开新建文章
    async with page.expect_popup() as p1_info:
        await page.locator("a.btn.write-btn").click()
    page2 = await p1_info.value
    # await page2.wait_for_load_state('load')
    await page2.wait_for_timeout(1000)
    print('wait for load state')
    
    await page2.locator("div._1GsW5").click()
    await page2.wait_for_timeout(1000)

    name= title(file_path)
    await page2.wait_for_selector('div > input[type="text"]')
    await page2.locator('div > input[type="text"]').clear()
    await page2.locator('div > input[type="text"]').fill(name)
    await page2.wait_for_timeout(1000)

    md_content = content(file_path)
    pyperclip.copy(md_content)
    await page2.locator("div.kalamu-area").click()
    await page2.locator("div.kalamu-area").press('Control+v')
    await page2.wait_for_timeout(1000)
    await page2.locator('a[data-action="publicize"]').click()
    await page2.wait_for_selectorr('a:has-text("发布成功")')
    print('publish success')
    await browser.close()




    # await browser.close()

async def wxgzh(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = 'Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(wxgzh(file_path,cover_path))
