import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect
from func.get_cover import get_random_image
from func.md_to_doc import md_to_doc
from func.title_content import content, title

async def run(playwright: Playwright, filepath: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/zhihu-mp-auth.json'
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
    url='https://www.zhihu.com'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = "button.GlobalWriteV2-topItem"
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.locatorr(".Login-socialButtonGroup > button").first.click()
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
    
    async with page.expect_popup() as popup_info:
        await page.get_by_role("button",name='写文章').click()
    page2 = await popup_info.value
    await page2.wait_for_load_state('load')
    
    name=title(file_path)
    await page2.locator('textarea').fill(name)
    
    await page2.get_by_label("文档").click()
    await page2.locator("#Popover5-content").get_by_label("文档").click()
    
    await page2.locator('form input').set_input_files(file_path)
    
    cover = get_random_image(cover_path)
    await page2.locator("label input[type='file']").set_input_files(cover)
    
    await page2.wait_for_timeout(10*1000)
    await page2.get_by_role("button", name="发布").click()
    
    await page2.get_by_role("button", name="写文章").wait_for()
    await browser.close()
        
async def zhihu(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = '/run/media/kf/data/obsidian/4-Archives/自动化发布文章脚本/Dataview JavaScript速查表.docx'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(zhihu(file_path,cover_path))
