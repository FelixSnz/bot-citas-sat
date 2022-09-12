from typing import List
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import requests
import time
import os

import speech_recognition as sr
from pydub import AudioSegment


from proxy_rotation import get_proxies, filter_valid_proxy
chrome_driver_path = r'chromedriver.exe'
curp = "ROXE800409MTSDXR05"
vin = "2FMZA5144YBA21362"
url_bef_check = ""
check_mark_class_name = ".recaptcha-checkbox-checkmark"
asd = ".recaptcha-checkbox-borderAnimation"
test_file_mp3 = "audio.wav"

urls = {
    "regularizacion-autos":r"https://www.regularizaauto.sspc.gob.mx/",
    "firma-electronica":""
}

def audio_file_to_text(audio_file_path:str):

    wav_save_name = "temp.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(audio_file_path)
    sound.export(wav_save_name, format="wav")


    r = sr.Recognizer()
    with sr.AudioFile(wav_save_name) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text

class myChromeDriver(webdriver.Chrome):
    """_summary_

    Args:
        webdriver (_type_): _description_
    """

    

    

    def __init__(driver, proxy):
        options = ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--proxy-server={}'.format(proxy))
        super().__init__(executable_path=chrome_driver_path, options=options)
        driver.wait:WebDriverWait = WebDriverWait(driver, 10)

    

    def wait_and_get_element(driver, by_type:str, xpath:str) -> WebElement:
        driver.wait.until(EC.visibility_of_all_elements_located((by_type, xpath)))
        return driver.find_element(by_type, xpath)
    
    def wait_and_get_elements(driver, by_type:str, xpath:str) -> List[WebElement]:
        driver.wait.until(EC.visibility_of_all_elements_located((by_type, xpath)))
        return driver.find_elements(by_type, xpath)


    def select_my_module(driver, city:str):
        module_selector_xpath = "/html/body/div[3]/main/div/div[1]/div[2]/form/select"
        module_selector = Select(driver.wait_and_get_element(By.XPATH, module_selector_xpath))
        all_options = [o for o in module_selector.options]
        for option in all_options:
            if city in option.text:
                module_selector.select_by_value(option.get_attribute('value'))
                driver.click_submit()
                return
        
    def download_mp3_url(driver, mp3_url):
        doc = requests.get(mp3_url)
        mp3_file_savename = 'myfile.mp3'
        with open(mp3_file_savename, 'wb') as f:
            f.write(doc.content)
        return mp3_file_savename
        

    def click_submit(driver):
        submit_curp_btn_id = "envia"
        submit_curp_btn = driver.wait_and_get_element(By.ID, submit_curp_btn_id)
        submit_curp_btn.click()

    def wait_for_recaptcha_status(driver, recaptcha_click_btn:WebElement, timeout:int) -> bool:
        elapsed_time = 0
        recaptcha_status = eval(recaptcha_click_btn.get_attribute("aria-checked").capitalize())
        while not recaptcha_status and elapsed_time < timeout:
            recaptcha_status = eval(recaptcha_click_btn.get_attribute("aria-checked").capitalize())
            elapsed_time += 1
        return recaptcha_status

    
        


    def enter_curp(driver, curp_str):
        curp_entry_xpath = r'/html/body/div[4]/main/div/div[2]/div[2]/div/div/form/div[1]/input'

        driver.get(urls["regularizacion-autos"])
        

        curp_entry = driver.wait_and_get_element(By.XPATH, curp_entry_xpath)
        curp_entry.send_keys(curp_str)


    def check_calendar(driver):
        
        div_calendar_xpath = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr/td/div/div/*'
        # test_asdasda_pathj = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[1]'
        # asdadasdsadasdadad = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[3]'
        # sasdaddsadadadadss = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[1]/table/tbody/tr/td[2]'

        rows_amount = len(driver.wait_and_get_elements(By.XPATH, div_calendar_xpath))


        print("row amount: ", rows_amount)


        pass
    
    
        



    def change_calendar_month(driver, forward:bool = True):
        prev_month_btn_xpath = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/button'
        next_month_btn_xpath = r'/html/body/div[4]/main/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/button'

        # if forward:
        #     chague_month_btn = driver.





def main():


    # proxy = filter_valid_proxy(get_proxies())

    # if not proxy:
    #     print("nigun proxy fue valido, intentando otra vez")
    #     proxy = filter_valid_proxy(get_proxies())
        




    # my_driver = myChromeDriver(proxy=proxy)

    # my_driver.enter_curp(curp)
    # time.sleep(1)
    # my_driver.bypass_recaptcha()
    
    # my_driver.select_my_module("Rio Bravo")
    # my_driver.check_calendar()


    print(audio_file_to_text("myfile.mp3"))


    
    pass

if __name__=="__main__":
    main()