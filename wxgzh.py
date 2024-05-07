import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect
from func.get_cover import get_random_image
from func.md_to_doc import md_to_doc
from func.title_content import content

async def run(playwright: Playwright, filepath: str, cover_path: str) -> None:
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
    
    # 填写文章title
    # title=os.path.splitext(os.path.basename(filepath))[0]
    # await page1.get_by_placeholder("请在这里输入标题").fill(title)
    # print('fill title:', title)


    # upload docx file
    await page1.get_by_role("listitem", name="文档导入").click()
    docx_file = md_to_doc(filepath)
    await page1.locator(".weui-desktop-upload input").set_input_files(docx_file)
    
    author="kefu1252"
    await page1.get_by_placeholder("请输入作者").fill(author)
    print('fill author:', author)
    
    await page1.wait_for_selector(".select-cover__btn")
    await page1.locator(".select-cover__btn").hover()
    await page1.get_by_role("link", name="从图片库选择").click()
    cover_file = get_random_image(cover_path)
    await page1.locator('input[multiple="multiple"]').set_input_files(cover_file)
    await page1.wait_for_timeout(3000)
    await page1.get_by_role("button", name="下一步").click()
    await page1.wait_for_timeout(1000)
    await page1.get_by_role("button", name="完成").click()
    print("封面")
        
    await page1.locator(".weui-desktop-switch__box").first.click()
    await page1.locator("label").filter(has_text="我已阅读并同意遵守《微信公众平台原创声明及相关功能使用协议》").locator("i").click()
    await page1.get_by_role("button", name="下一步").click()
    await page1.get_by_role("term").click()
    await page1.get_by_text("科技").first.click()
    await page1.get_by_text("互联网+").first.click()
    await page1.wait_for_timeout(1000)
    await page1.get_by_role("button", name="确定").click()
    print("原创声明")

    await page1.locator("#js_reward_setting_area > .setting-group__content > .setting-group__switch > .weui-desktop-switch > .weui-desktop-switch__box").click()
    await page1.locator(".reward-reply-switch__wrp > .weui-desktop-switch > .weui-desktop-switch__box").click()
    await page1.wait_for_timeout(1000)
    await page1.get_by_role("button", name="确定").click()
    print("赞赏")
    
    await page1.locator("#js_comment_area i").first.set_checked(True)

    await page1.wait_for_timeout(1000)
    await page1.get_by_role("button", name="发表").click()
    print("发表")
    
    await page1.locator("#vue_app").get_by_role("button", name="发表").click()
    await page1.get_by_role("button", name="继续发表").click()
    print("继续发表")
    print("扫码验证")
    await page1.wait_for_selector(".weui-desktop-qrcode__img")
    print("发布成功")
    await page1.wait_for_timeout(1000)
    await browser.close()

async def wxgzh(file_path,cover_path) -> None:
    
    async with async_playwright() as playwright:
        await run(playwright, file_path, cover_path)

if __name__ == '__main__':
    file_path = 'Dataview JavaScript速查表.md'
    cover_path="/run/media/kf/data/cover"

    asyncio.run(wxgzh(file_path,cover_path))
