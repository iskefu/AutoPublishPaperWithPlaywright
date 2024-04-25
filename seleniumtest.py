import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess
from func.check_port import check_port
from func.find_click import find_and_click, find_input, markdownhere, wait_login_success
from func.title_content import title, content

def swich_new_window(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
def login(driver):
    find_and_click(driver, config[platform]["login_element"])
    
    find_and_click(driver, config[platform]["weixin_element"])
    swich_new_window(driver)
    
    
    wait_login_success(driver, config[platform]["wright_paper_element"])
    
def jian_shu():

    driver.get(config[platform]["domain"])
    sleep(1)
    swich_new_window(driver)
    
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
if __name__ ==  '__main__':
    if not check_port(9222):
        subprocess.Popen(["/usr/bin/google-chrome-stable" ,"--remote-debugging-port=9222"])
        sleep(3)

    options = Options()
    options.debugger_address="127.0.0.1:9222"
    driver = webdriver.Chrome(options = options)
    driver.maximize_window()
    driver.implicitly_wait(10) # seconds
    
    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'
    title = title(filepath)
    content = content(filepath)
    
    with open('xpath_config.json', 'r') as f:
        config = json.load(f)
    
    platform="jianshu"
    jian_shu()