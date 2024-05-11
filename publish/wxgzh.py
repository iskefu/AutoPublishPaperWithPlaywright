import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect

from publish.func.get_cover import get_random_image
from publish.func.md_to_doc import md_to_doc

async def run(playwright: Playwright, file_path: str, cover_path: str) -> None:
    # launch browser
    browser = await playwright.chromium.launch(headless=False)
    
    # create new context
    ss_file = f'playwright/.auth/weixin-mp-auth.json'
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
    url='https://mp.weixin.qq.com/'
    await page.goto(url)
    await page.wait_for_load_state('load')

    #  if login
    logined_element = '.weui-desktop-account__img'
    is_login = await page.is_visible(logined_element)
    if not is_login:
        try:

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

    # 打开新建文章
    async with page.expect_popup() as p1_info:
        await page.locator(".new-creation__menu-content").first.click()
    page1 = await p1_info.value
    await page1.wait_for_load_state('load')
    print('wait for load state')
    
    # upload docx file
    await page1.get_by_role("listitem", name="文档导入").click()
    doc = md_to_doc(file_path)
    await page1.locator(".weui-desktop-upload input").set_input_files(doc)
    
    author="kefu1252"
    await page1.get_by_placeholder("请输入作者").fill(author)
    print('fill author:', author)
    
    # upload cover image
    await page1.wait_for_selector(".select-cover__btn")
    await page1.locator(".select-cover__btn").hover()
    await page1.get_by_role("link", name="从图片库选择").click()
    cover_file = get_random_image(cover_path)
    await page1.locator('input[multiple="multiple"]').set_input_files(cover_file)
    await page1.wait_for_timeout(10*1000)
    await page1.locator('div.selected.weui-desktop-img-picker__item').wait_for()
    await page1.get_by_role("button", name="下一步").click()
    await page1.wait_for_timeout(10000)
    await page1.get_by_role("button", name="完成").wait_for()
    await page1.get_by_role("button", name="完成").click()
    print("封面")
    
    # 原创声明
    await page1.locator("#js_original").click()
    await page1.locator("i.weui-desktop-icon-checkbox").click()
    await page1.get_by_role("button", name="确定").click()
    print("原创声明")

    await page1.locator("#js_reward_setting_area").click()
    await page1.wait_for_timeout(3000)
    await page1.get_by_role("button", name="确定").click()
    print("赞赏")
    
    await page1.wait_for_timeout(1000)
    await page1.get_by_role("button", name="发表").click()
    print("发表")
    
    await page1.locator("#vue_app").get_by_role("button", name="发表").wait_for()
    await page1.locator("#vue_app").get_by_role("button", name="发表").click()
    await page1.get_by_role("button", name="继续发表").click()
    print("继续发表")
    print("扫码验证")
    await page1.wait_for_selector(".weui-desktop-qrcode__img", timeout=129*1000)
    print("发布成功")
    await browser.close()
    os.remove(doc)
    
async def wxgzh(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = 'Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(wxgzh(file_path,cover_path))