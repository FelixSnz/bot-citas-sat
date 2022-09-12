from typing import List
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException    

import time
import sys

from proxy_rotation import get_proxies, filter_valid_proxy

chrome_driver_path = r'chromedriver'


class myChromeDriver(webdriver.Chrome):

    

    def __init__(driver, executable_path, proxy):
        options = ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--proxy-server={}'.format(proxy))
        super().__init__(executable_path=executable_path, options=options)
        driver.wait:WebDriverWait = WebDriverWait(driver, 10)
    
        
    def element_exists(driver, by_type:str, element_ref:str) -> bool:
        try:
            driver.wait_and_get_element(by_type, element_ref)
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        else:
            return True

    def wait_and_get_element(driver, by_type:str, element_ref:str) -> WebElement:
        driver.wait.until(EC.visibility_of_all_elements_located((by_type, element_ref)))
        return driver.find_element(by_type, element_ref)
    
    def wait_and_get_elements(driver, by_type:str, element_ref:str) -> List[WebElement]:
        driver.wait.until(EC.visibility_of_all_elements_located((by_type, element_ref)))
        return driver.find_elements(by_type, element_ref)       

    def click_element(driver, by_type:str, element_ref:str):
        element = driver.wait_and_get_element(by_type, element_ref)
        element.click()


    def fill_input(driver, by_type:str, element_ref:str, data):
        field = driver.wait_and_get_element(by_type, element_ref)
        field.send_keys(data)

    def close_current_tab_and_return_to_main_tab(driver):
        driver.close()
        parent = driver.window_handles[0]
        driver.switch_to.window(parent)

    def wait_and_get_next_window(driver, timeout:int=1000) -> str:
        print(driver.window_handles)
        elapsed_time = 0
        while elapsed_time < timeout:
            if len(driver.window_handles) > 1:
                return driver.window_handles[1]
            elapsed_time += 1
        return None

    def switch_to_next_window(driver):
        next_window = driver.wait_and_get_next_window()
        driver.switch_to.window(next_window)


