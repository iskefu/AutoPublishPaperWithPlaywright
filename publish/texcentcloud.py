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
    ss_file = f'playwright/.auth/tencentcloud-mp-auth.json'
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
    url='https://cloud.tencent.com/developer'
    await page.goto(url)
    await page.wait_for_load_state('load')

    istips= await page.is_visible("button.cdc-btn.mod-activity__btn.cdc-btn--hole")
    if istips:
        await page.get_by_role("button",  name= "不再提示" ).click()
        
    #  if login
    logined_element = 'i.cdc-header__account-avatar'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.get_by_role('button', name='登录/注册').click()
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
    
    await page.get_by_text('发布').click()
    await page.get_by_role('link', name= '写文章' ).click()
    await page.wait_for_timeout(2000)
    # await page.locator('div.col-editor-switch a').click()
    name = title(file_path)
    await page.locator('div.article-title-wrap  textarea').fill(name)

    await page.locator(".qa-r-editor-btn-wrap input[accept='.docx']").set_input_files(file_path)
    

    await page.get_by_role('button', name= '发布' ).click()
    await page.get_by_label('原创').click()
    await page.locator('.com-2-tag-input').first.fill("github")
    await page.locator('.com-2-tagsinput-dropdown-menu li').first.click()
    await page.wait_for_timeout(2000)
    await page.get_by_role('button', name= '确认发布' ).click()
    await page.wait_for_selector('.col-editor-feedback-icon')
    await browser.close()
    
async def tencentcloud(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = '/run/media/kf/data/obsidian/4-Archives/自动化发布文章脚本/Dataview JavaScript速查表.docx'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(tencentcloud(file_path,cover_path))
