import asyncio
import os
from playwright.async_api import Playwright, async_playwright, expect
from func.get_chrome_user_data_dir import get_chrome_user_data_dir
from func.title_content import content




async def run(playwright: Playwright) -> None:
    
    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'
    
    browser = await playwright.chromium.launch(headless=False)
    
    ss_file = f'data/wechat_ss.json'
    if os.path.exists(ss_file):
        print('Loading state from', ss_file)
        context =await browser.new_context(storage_state=ss_file)
    else:
        print('No state file found, creating new context')
        context = await browser.new_context()
    p=await context.new_page()
    
    url='https://mp.weixin.qq.com/'
    await p.goto(url)
    print('p goto:', url)
    
    p.wait_for_load_state('load')
    print('wait for load state')
    
    try:
        logined_element = '.weui-desktop-account__img'
        await p.wait_for_selector(logined_element, timeout=120*1000)
        print('wait for user img locator:', logined_element)
    except Exception as e:
        print('login failed, try again \n error:', e)
        await p.close()
        return
    
    async with p.expect_popup() as p1_info:
        await p.locator(".new-creation__menu-content").first.click()
    p1 = await p1_info.value
    print('new creation popup:', p1)
    
    await p1.wait_for_load_state('load')
    print('wait for load state')
    
    title=os.path.splitext(os.path.basename(filepath))[0]
    await p1.get_by_placeholder("请在这里输入标题").fill(title)
    print('fill title:', title)
    
    author="kefu1252"
    await p1.get_by_placeholder("请输入作者").fill(author)
    print('fill author:', author)
    
    cont =  content(filepath)
    await p1.frame_locator("#ueditor_0").locator("body").fill(cont)
    print('fill content:', cont)

    await p1.locator(".select-cover__btn").hover()
    await p1.get_by_role("link", name="从图片库选择").click()
    await p1.get_by_role("img", name="图片描述").first.click()
    await p1.get_by_role("button", name="下一步").click()
    await p1.wait_for_timeout(1000)
    await p1.get_by_role("button", name="完成").click()
    print("封面")
        
    await p1.locator(".weui-desktop-switch__box").first.click()
    await p1.locator("label").filter(has_text="我已阅读并同意遵守《微信公众平台原创声明及相关功能使用协议》").locator("i").click()
    await p1.get_by_role("button", name="下一步").click()
    await p1.get_by_role("term").click()
    await p1.get_by_text("科技").first.click()
    await p1.get_by_text("互联网+").first.click()
    await p1.wait_for_timeout(1000)
    await p1.get_by_role("button", name="确定").click()
    print("原创声明")
    
    await p1.locator("#js_reward_setting_area > .setting-group__content > .setting-group__switch > .weui-desktop-switch > .weui-desktop-switch__box").click()
    await p1.locator(".reward-reply-switch__wrp > .weui-desktop-switch > .weui-desktop-switch__box").click()
    await p1.wait_for_timeout(1000)
    await p1.get_by_role("button", name="确定").click()
    print("赞赏")
    
    await p1.wait_for_timeout(1000)
    await p1.get_by_role("button", name="发表").click()
    print("发表")
    
    await p1.locator("#vue_app").get_by_role("button", name="发表").click()
    await p1.get_by_role("button", name="继续发表").click()
    print("继续发表")
    
    print("扫码验证")
    await p.pause() # 断点


async def main() -> None:
    
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
