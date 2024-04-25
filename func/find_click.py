from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys  # 导入Keys类

def find_and_click(driver, xpath):

        try:
            for i in range(3):
                actions = ActionChains(driver)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                actions.move_to_element(driver.find_element(By.XPATH,xpath)).perform()
                driver.find_element(By.XPATH, xpath).click()
                print(f"成功找到元素:{xpath}并点击")
                break

        except NoSuchElementException:
            print(f"未找到路径为{xpath}的元素")
        except ElementNotInteractableException:
            print(f"路径为{xpath}的元素不可交互")
        except Exception as e:
            print(f"试图点击元素时发生错误: {e}")
        sleep(1)
        
def wait_login_success(driver,xpath):
    success_element = (By.XPATH, xpath)
    try:
        # WebDriverWait 会每隔一小段时间就判断一次指定的元素是否已经出现，这里设置最多等待300秒
        WebDriverWait(driver, 300).until(EC.presence_of_element_located(success_element))
        print("成功登录！")
    except Exception as e:
        print(f"登录超时: {e}")
        
def find_upload(driver, xpath, filepath):
    try:
        for i in range(3):
            actions = ActionChains(driver)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.find_element(By.XPATH, xpath).send_keys(filepath)
            print(f"成功找到元素:{xpath}并点击")
            break

    except NoSuchElementException:
        print(f"未找到路径为{xpath}的元素")
    except ElementNotInteractableException:
        print(f"路径为{xpath}的元素不可交互")
    except Exception as e:
        print(f"试图点击元素 {xpath} 发生错误: {e}")
    sleep(1)       
def find_input(driver, xpath, text):
    try:
        for i in range(3):
            actions = ActionChains(driver)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            actions.move_to_element(driver.find_element(By.XPATH,xpath)).perform()
            driver.find_element(By.XPATH, xpath).click()
            driver.find_element(By.XPATH, xpath).clear()
            driver.find_element(By.XPATH, xpath).send_keys(text)
            print(f"成功找到元素:{xpath}并点击")
            break

    except NoSuchElementException:
        print(f"未找到路径为{xpath}的元素")
    except ElementNotInteractableException:
        print(f"路径为{xpath}的元素不可交互")
    except Exception as e:
        print(f"试图点击元素 {xpath} 发生错误: {e}")
    sleep(1)
def markdownhere(driver,xpath):
    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL + Keys.ALT + 'm')