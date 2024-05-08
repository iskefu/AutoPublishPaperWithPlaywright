import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect

from publish.func.get_cover import get_random_image
from publish.func.md_to_doc import md_to_doc

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/baijiahao-mp-auth.json'
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
    url='https://baijiahao.baidu.com/'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = '.author'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.locator("div.btnlogin--bI826").click()
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

    await page.locator("div.nav-switch-btn").first.click()
    await page.get_by_role("button",  name= "发布" ).hover()
    await page.locator("li.edit-news").click()
    await page.wait_for_load_state("load")
    
    await page.locator("#edui43_body div").first.click()
    doc=md_to_doc(file_path)
    await page.locator("span input[type='file']").set_input_files(doc)

    cover=get_random_image(cover_path)
    await page.locator("#edui33_body div").first.click()
    await page.locator("span.uploader input").set_input_files(cover)
    await page.wait_for_timeout(3 * 1000)
    await page.get_by_role("button",  name= "确 认" ).click()

    await page.locator("div.edit-cover-container  input").last.click()
    await page.locator(".coverUploaderView > .container").first.click()
    await page.locator("div.cheetah-ui-pro-image-modal-choose-cover > div").click()
    await page.get_by_role("button",  name= "确 认" ).click()
    await page.wait_for_timeout(5 * 1000)
    await page.locator("div.setting-item input").first.click()
    await page.wait_for_timeout(5 * 1000)
    await page.locator("div.op-btn-outter-content button").nth(1).click()
    await page.wait_for_selector('a.btn.write-another')
    await browser.close()

async def baijiahao(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = 'Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"
    asyncio.run(baijiahao(file_path,cover_path))