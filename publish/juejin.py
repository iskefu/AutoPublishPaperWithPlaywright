import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect

from publish.func.title_content import title

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/juejin-mp-auth.json'
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
    url='https://www.juejin.cn'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = 'div.avatar-wrapper'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.locator("button.login-button").click()
            await page.locator("div.oauth-bg").nth(1).click()
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
    
    await page.get_by_role('button', name='创作者中心').click()
    await page.wait_for_load_state('load')

    async with page.expect_popup() as p1_info:
        await page.get_by_role('button', name='写文章').click()
    page1 = await p1_info.value
    await page1.wait_for_load_state('load')
    await page1.locator('div.bytemd-toolbar-icon.bytemd-tippy.bytemd-tippy-right[bytemd-tippy-path="6"]').click()

    await page1.locator('div.upload-area > input[type="file"]').set_input_files(file_path)

    name = title(file_path)
    await page1.locator("input.title-input").fill(name)
    await page1.get_by_role("button",  name= "发布" ).click()
    await page1.locator("div.item").nth(4).click()
    await page1.locator("div.byte-select__wrap").first.click()
    await page1.get_by_role("button",  name= "GitHub" ).click()
    await page1.locator("div.summary-textarea > textarea").fill("A"*100)
    await page1.get_by_role("button",  name= "确定并发布" ).click()
    await page1.wait_for_timeout(1000)
    await page1.get_by_text("回到首页").click()
    await browser.close()

async def juejin(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = 'Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(juejin(file_path,cover_path))
