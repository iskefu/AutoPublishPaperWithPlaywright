import json
import os
import subprocess
from time import sleep
from selenium.webdriver.common.by import By
from func.find_click import find_and_click, find_input, find_upload, get_herf, markdownhere, wait_login_success
from func.md_to_doc import md_to_docx
from func.title_content import content, md_content, title
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def swich_new_window(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

def JIANSHU(platform="jianshu"):
    # 登录后 跳转到发布页
    driver.get(config[platform]["url"])

    swich_new_window(driver)
    find_and_click(driver,config[platform]["new_paper"])

    find_input(driver,config[platform]["title"],title)
    find_input(driver,config[platform]["content"],content)
    
    markdownhere(driver,config[platform]["content"])
    
    sleep(2)
    
    find_and_click(driver,config[platform]["publish"])
    sleep(2)
    
    if driver.find_elements(By.XPATH,config[platform]["publish"]):
        find_and_click(driver,config[platform]["publish"])
    else:
        print("发布成功")
    driver.quit()

def ZHIHU(platform="zhihu"):
    driver.get(config[platform]["url"]) 
    swich_new_window(driver)
    find_and_click(driver,config[platform]["doc"])
    find_and_click(driver,config[platform]["doc2"])
    find_upload(driver,config[platform]["upload_doc"],filepath)
    find_input(driver,config[platform]["title"],title)
    find_and_click(driver,config[platform]["publish_setting"])
    find_and_click(driver,config[platform]["add_topic"])
    find_input(driver,config[platform]["search_topic"],title)
    find_and_click(driver,config[platform]["publish"])
    
    if driver.find_elements(By.XPATH,config[platform]["publish"]):
        find_and_click(driver,config[platform]["publish"])
    else:
        print("发布成功")    
    
def BLBL(platform="bilibili"):
    
    driver.get(config[platform]["url"])
    swich_new_window(driver)
    sleep(3)
    
    iframe= driver.find_element(By.XPATH,"//div[@id='edit-article-box']//iframe")
    driver.switch_to.frame(iframe)
    print("switch to iframe")
    sleep(1)
    
    driver.find_element(By.XPATH,"//textarea").send_keys(title)
    print("title")
    sleep(1)


    driver.find_element(By.XPATH,"//div[@data-placeholder='请输入正文']").send_keys(content)
    print("content")
    sleep(5)

    e=driver.find_element(By.XPATH,"//button[contains(text(),'提交文章')]")
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});',e)
    e.click()
    print("submit")
    sleep(1)
    
def CSDN(platform="csdn"):
    driver.get(config[platform]["url"])
    swich_new_window(driver)
    find_and_click(driver,config[platform]["write_paper"])
    find_and_click(driver,config[platform]["MD_editor"])
    swich_new_window(driver)
    # find_upload(driver,config[platform]["upload_doc"],filepath)
    driver.find_element(By.XPATH,config[platform]["upload_doc"]).send_keys(filepath)
    driver.find_element(By.XPATH,config[platform]["publish"]).click()
    driver.find_element(By.XPATH,config[platform]["add_tag"]).click()
    driver.find_element(By.XPATH,config[platform]["add_tag1"]).click()
    driver.find_element(By.XPATH,config[platform]["close"]).click()
    driver.find_element(By.XPATH,config[platform]["publish2"]).click()
    if driver.find_elements(By.XPATH,config[platform]["publish2"]):
        find_and_click(driver,config[platform]["publish"])
    else:
        print("发布成功")
        
# def BAIJIAHAO(platform="baijiahao"):
def WXGZH(platform="wxgzh"):
    
    driver.get(config[platform]["url"])
    
    swich_new_window(driver)
    
    wait_login_success(driver,config[platform]["pic_paper_news"])
    
    find_and_click(driver,config[platform]["pic_paper_news"])
    
    swich_new_window(driver)
    
    find_input(driver,config[platform]["title"],config[platform]["title"])
    find_input(driver,config[platform]["author"],config[platform]["author"])
    
    driver.switch_to.frame(config[platform]["iframe"])
    find_input(driver,config[platform]["content"],content)
    markdownhere(driver,config[platform]["content"])
    driver.switch_to.default_content()
def js_click(driver,xpath):
    e=driver.find_element(By.XPATH,xpath)
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});',e)
    driver.execute_script("arguments[0].click();", e)

def TOUTIAO(platform='toutiao'):
    
    driver.get(config[platform]["url"])
    swich_new_window(driver)
    sleep(1)
    
    driver.find_elements(By.XPATH,"//div[@class='syl-toolbar']//button")[-1].click()
    print('文档导入')
    sleep(1)
    
    doc_filepath = md_to_docx(filepath)
    driver.find_element(By.XPATH,"//input[@type='file']").send_keys(doc_filepath)
    os.remove(doc_filepath)
    sleep(1)
    print('上传文件')
    
    driver.find_element(By.XPATH,config[platform]["title"]).clear()
    driver.find_element(By.XPATH,config[platform]["title"]).send_keys(title)
    sleep(1)
    print('标题')

    js_click(driver,"//span[contains(text(),'单标题')]/..")
    sleep(1)
    print('单标题')
    
    js_click(driver,"//span[contains(text(),'无封面')]/..")
    sleep(1)
    print('无封面')
    
    driver.execute_script('arguments[0].scrollIntoView();',driver.find_element(By.XPATH,config[platform]["declare_original"]))
    driver.find_element(By.XPATH,config[platform]["declare_original"]).click()
    sleep(1)
    print('声明原创')
    
    driver.find_element(By.XPATH,config[platform]["preview_publish"]).click()    
    sleep(1)
    print('预览发布')
    
    # 确认发布
    driver.find_element(By.XPATH,config[platform]["confirm_publish"]).click()
    print('确认发布')
    sleep(1)
    
    # 手机验证码
    driver.find_element(By.XPATH,config[platform]["phone_code"]).click()
    print('手机验证码')
    sleep(1)
    
    
if __name__ ==  '__main__':
    
    port=9222
    
    # 打开浏览器
    # subprocess.Popen(["/usr/bin/google-chrome-stable" ,f"--remote-debugging-port={port}"])
    # sleep(3)
    
    options = Options()
    # options.add_argument("--disable-gpu")
    options.debugger_address=f"127.0.0.1:{port}"
    driver = webdriver.Chrome(options = options)
    # driver.maximize_window()
    driver.implicitly_wait(10) # secondst)

    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'
    title = title(filepath)
    content = content(filepath)
    with open('xpath_config.json', 'r') as f:
        config = json.load(f)
    
    # JIANSHU(platform="jianshu")
    # ZHIHU(platform="zhihu")
    BLBL(platform="blbl")
    # CSDN(platform="csdn")
    # WXGZH(platform="wxgzh")
    # TOUTIAO(platform="toutiao")
    