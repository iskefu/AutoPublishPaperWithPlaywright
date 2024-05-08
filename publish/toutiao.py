import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect

from publish.func.get_cover import get_random_image
from publish.func.title_content import title

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/toutiao-mp-auth.json'
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
    url='https://www.toutiao.com/'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = 'div.user-icon span'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:
            await page.locator(".show-monitor a.login-button").click()
            await page.get_by_label("协议勾选框").click()
            async with page.expect_popup() as popup_info:
                await page.get_by_role("button", name="微信登录").click()
            page1= await popup_info.value
            await page1.wait_for_selector(logined_element)
            print('wait for user img locator:', logined_element)
        
        except Exception as e:
            print('login failed, try again \n error:', e)
            await page.close()
            return
    else:
        page1=page
    # 保存登陆状态
    await page1.wait_for_load_state('load')
    await context.storage_state(path=ss_file)
    print('save state to', ss_file)
    
    async with page1.expect_popup() as popup_info:
        await page1.locator("a.publish-item").first.click()
    page2 = await popup_info.value
    await page2.wait_for_load_state('load')
    await (await page2.wait_for_selector("span.icon-wrap")).click()

    await page2.locator('div.doc-import button').click()
    await page2.locator(' div.upload-handler input').set_input_files(file_path)

    await page2.wait_for_timeout(1000)
    name = title(file_path)
    await page2.locator("div.editor-title textarea").fill(name)
    await page2.wait_for_timeout(1000)
    # if 

    await page2.locator("label").filter(has_text="单标题").locator("div").click()
    
    await page2.locator(".article-cover-add").click()
    cover =get_random_image(cover_path)
    await page2.locator('button input').set_input_files(cover)
    await page2.wait_for_timeout(1000)
    await page2.get_by_role("button", name="确定").click()
    
    await page2.locator("label").filter(has_text="声明原创").locator("div").click()
    
    await page2.get_by_role("button", name="预览并发布").click()
    await page2.wait_for_timeout(3000)
    await page2.locator('div.publish-footer  button').last.click()
    
    await page2.locator("button").filter(has_text="获取验证码").click()
    
    
async def toutiao(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = '/run/media/kf/data/obsidian/4-Archives/自动化发布文章脚本/Dataview JavaScript速查表.docx'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(toutiao(file_path,cover_path))
