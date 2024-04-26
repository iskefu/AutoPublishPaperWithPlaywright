import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess
from func.check_port import check_port
from func.find_click import find_and_click, find_input, find_upload, get_herf, markdownhere, wait_login_success
from func.title_content import title, content

def swich_new_window(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

def JIANSHU(platform="jianshu"):
    driver.get(config[platform]["url"])
    sleep(1)
    swich_new_window(driver)
    def login(driver):
        find_and_click(driver, config[platform]["login"])
        
        find_and_click(driver, config[platform]["weixin"])
        swich_new_window(driver)
        
        
        wait_login_success(driver, config[platform]["wright_paper"])
        
    login=driver.find_elements(By.XPATH,config[platform]["login"])
    if login:       
        login(driver)

    find_and_click(driver,config[platform]["wright_paper"])
    swich_new_window(driver)
    
    
    find_and_click(driver,config[platform]["new_paper"])
    
    # driver.get('https://www.jianshu.com/writer#/notebooks/54772126/notes/119657316')
    # sleep(2)
    
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
    islogin=driver.find_elements(By.XPATH,config[platform]["write_paper"])
    if not islogin:
        find_and_click(driver,config[platform]["weixin"])
        wait_login_success(driver,config[platform]["write_paper"])
    find_and_click(driver,config[platform]["write_paper"])
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
    # driver.get(config[platform]["url"])
    # swich_new_window(driver)
    # login=driver.find_elements(By.XPATH,config[platform]["login"])
    # if login:
    #     find_and_click(driver,config[platform]["login"])
    #     find_and_click(driver,config[platform]["weixin"])
    #     wait_login_success(driver,config[platform]["upload_entry"])
    # find_and_click(driver,config[platform]["upload_entry"])
    # driver.get(config[platform]["url"]+get_herf(driver,config[platform]["zhuanlan"]))
    # find_and_click(driver,config[platform]["zhuanlan"])
    
    
    driver.get(config[platform]["zhuanlan_url"])
    swich_new_window(driver)
    sleep(5)
    el=driver.find_element(By.XPATH,config[platform]["title"])
    print(el)
    find_input(driver,config[platform]["title"],title)
    find_input(driver,config[platform]["content"],content)
    find_and_click(driver,config[platform]["publish"])
    
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
    # ZHIHU(platform="zhihu")
    # BLBL(platform="bilibili")
    CSDN(platform="csdn")