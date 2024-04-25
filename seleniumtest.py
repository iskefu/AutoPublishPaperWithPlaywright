import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess
from func.check_port import check_port
from func.find_click import find_and_click, find_input, find_upload, markdownhere, wait_login_success
from func.title_content import title, content

def swich_new_window(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

def JIANSHU(platform="jianshu"):
    driver.get(config[platform]["url"])
    sleep(1)
    swich_new_window(driver)
    def login(driver):
        find_and_click(driver, config[platform]["login_element"])
        
        find_and_click(driver, config[platform]["weixin_element"])
        swich_new_window(driver)
        
        
        wait_login_success(driver, config[platform]["wright_paper_element"])
        
    login_element=driver.find_elements(By.XPATH,config[platform]["login_element"])
    if login_element:       
        login(driver)

    find_and_click(driver,config[platform]["wright_paper_element"])
    swich_new_window(driver)
    
    
    find_and_click(driver,config[platform]["new_paper_element"])
    
    # driver.get('https://www.jianshu.com/writer#/notebooks/54772126/notes/119657316')
    # sleep(2)
    
    find_input(driver,config[platform]["title_element"],title)
    find_input(driver,config[platform]["content_element"],content)
    
    markdownhere(driver,config[platform]["content_element"])
    
    sleep(2)
    
    find_and_click(driver,config[platform]["publish_element"])
    sleep(2)
    
    if driver.find_elements(By.XPATH,config[platform]["publish_element"]):
        find_and_click(driver,config[platform]["publish_element"])
    else:
        print("发布成功")
    driver.quit()

def ZHIHU(platform="zhihu"):
    driver.get(config[platform]["url"])
    swich_new_window(driver)
    islogin=driver.find_elements(By.XPATH,config[platform]["write_paper_element"])
    if not islogin:
        find_and_click(driver,config[platform]["weixin_element"])
        wait_login_success(driver,config[platform]["write_paper_element"])
    find_and_click(driver,config[platform]["write_paper_element"])
    swich_new_window(driver)
    find_and_click(driver,config[platform]["doc_element"])
    find_and_click(driver,config[platform]["doc_element2"])
    find_upload(driver,config[platform]["upload_doc_element"],filepath)
    find_input(driver,config[platform]["title_element"],title)
    find_and_click(driver,config[platform]["publish_setting_element"])
    find_and_click(driver,config[platform]["add_topic_element"])
    find_input(driver,config[platform]["search_topic_element"],title)
    find_and_click(driver,config[platform]["publish_element"])
    
    if driver.find_elements(By.XPATH,config[platform]["publish_element"]):
        find_and_click(driver,config[platform]["publish_element"])
    else:
        print("发布成功")    
    
if __name__ ==  '__main__':
    if not check_port(9222):
        subprocess.Popen(["/usr/bin/google-chrome-stable" ,"--remote-debugging-port=9222"])
        sleep(3)

    options = Options()
    options.add_argument("--disable-gpu")
    options.debugger_address="127.0.0.1:9222"
    driver = webdriver.Chrome(options = options)
    # driver.maximize_window()
    driver.implicitly_wait(10) # seconds
    
    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'
    title = title(filepath)
    content = content(filepath)
    
    with open('xpath_config.json', 'r') as f:
        config = json.load(f)
    
    # JIANSHU(platform="jianshu")
    ZHIHU(platform="zhihu")
    