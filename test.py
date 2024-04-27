import asyncio
import os
import re
from playwright.async_api import Playwright, async_playwright, expect
from func.get_chrome_user_data_dir import get_chrome_user_data_dir
from func.title_content import content

async def run(playwright: Playwright) -> None:
    chrome_data_dir = get_chrome_user_data_dir()

    ss_file = 'wechat_ss.json'
    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'

    browser = await playwright.chromium.launch(headless=False)
    
    if os.path.exists(ss_file):
            print('Loading state from', ss_file)
            context =await browser.new_context(storage_state=ss_file)
    else:
        context = await browser.new_context()

    page = await context.new_page()
    await page.goto("https://mp.weixin.qq.com/")
    
    user_img_locator = '.weui-desktop-account__img'
    await page.wait_for_selector(user_img_locator, timeout=120*1000)
    
    
    async with page.expect_popup() as page1_info:
        await page.locator(".new-creation__menu-content").first.click()
    page1 = await page1_info.value
    
    title=os.path.splitext(os.path.basename(filepath))[0]
    await page1.get_by_placeholder("请在这里输入标题").fill(title)
    
    author="kefu1252"
    await page1.get_by_placeholder("请输入作者").fill(author)
    
    cont =  content(filepath)
    await page1.frame_locator("#ueditor_0").locator("body").fill(cont)
    
    await page1.locator(".weui-desktop-switch__box").first.click()
    await page1.locator("label").filter(has_text="我已阅读并同意遵守《微信公众平台原创声明及相关功能使用协议》").locator("i").click()
    await page1.get_by_role("button", name="下一步").click()
    await page1.get_by_role("term").click()
    await page1.get_by_text("科技").first.click()
    await page1.get_by_text("互联网+").first.click()
    await page1.get_by_role("button", name="确定").click()
    print("原创声明")
    
    await page1.locator("#js_reward_setting_area > .setting-group__content > .setting-group__switch > .weui-desktop-switch > .weui-desktop-switch__box").click()
    await page1.get_by_text("感谢我主").first.click()
    await page1.get_by_role("button", name="确定").click()
    print("赞赏")
    
    await page1.locator(".select-cover__btn").hover()
    await page1.get_by_role("link", name="从图片库选择").click()
    await page1.get_by_role("img", name="图片描述").first.click()
    await page1.get_by_role("button", name="下一步").click()
    await page1.get_by_role("button", name="完成").click()
    print("封面")
    
    await page1.pause() # 断点
    await page1.locator(".mass_send").first.click()
    
    await page1.wait_for_timeout(10000)

async def main() -> None:
    
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
