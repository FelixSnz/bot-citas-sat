
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from typing import List
import time
import sys

from proxy_rotation import get_proxies, filter_valid_proxy
from audiotools import audio_file_to_text, download_mp3_url, mp3_to_wav


from chromedriver import myChromeDriver




data_table_css_classname = ".panel>.table-responsive "




chrome_driver_path = r'chromedriver'


urls = {
    "regularizacion-autos":r"https://www.regularizaauto.sspc.gob.mx/",
    "firma-electronica":""
}



class SatAppointmentsDriver(myChromeDriver):

    

    def __init__(driver, driver_path, proxy):
        super().__init__(executable_path=driver_path, proxy=proxy)



    def select_my_module(driver, city:str):
        module_selector_xpath = "/html/body/div[3]/main/div/div[1]/div[2]/form/select"
        module_selector = Select(driver.wait_and_get_element(By.XPATH, module_selector_xpath))
        all_options:List[WebElement] = [o for o in module_selector.options]
        for option in all_options:
            if city in option.text:
                module_selector.select_by_value(option.get_attribute('value'))
                driver.click_submit()
                return
        
    
    def user_info_table_exists(driver) -> bool:
        user_info_table_xpath = r'/html/body/div[4]/main/div/div[2]/div[2]/div'
        return driver.element_exists(By.XPATH, user_info_table_xpath)
    
    def validate_vin(driver, vin:str) -> bool:
        vin_td_xpath = r'/html/body/div[4]/main/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td[2]'

        


    def click_submit(driver):
        submit_curp_btn_id = "envia"
        submit_curp_btn = driver.wait_and_get_element(By.ID, submit_curp_btn_id)
        submit_curp_btn.click()

    def wait_for_recaptcha_status(driver, recaptcha_click_btn:WebElement, timeout:int=1000) -> bool:
        elapsed_time = 0
        recaptcha_status = eval(recaptcha_click_btn.get_attribute("aria-checked").capitalize())
        while not recaptcha_status and elapsed_time < timeout:
            recaptcha_status = eval(recaptcha_click_btn.get_attribute("aria-checked").capitalize())
            elapsed_time += 1
        return recaptcha_status

    def click_and_get_recaptcha(driver, recaptcha_frame_xpath):
        recaptcha_frame = driver.wait_and_get_element(By.XPATH, recaptcha_frame_xpath)
        driver.switch_to.frame(recaptcha_frame)
        recaptcha_id = "recaptcha-anchor"
        recaptcha_element = driver.find_element(By.ID, recaptcha_id)
        recaptcha_element.click()
        return recaptcha_element
    
    def bypass_recaptcha(driver):
        #driver.switch_to.default_content()
        #recaptcha_question_frame_xpath = r'/html/body/div[6]/div[4]/iframe'
        #recaptcha_frame = driver.wait_and_get_element(By.XPATH, recaptcha_question_frame_xpath)
        #time.sleep(0.5)
        #driver.switch_to.frame(recaptcha_frame)
        
        sound_btn_xpath = "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button"
        sound_btn = driver.wait_and_get_element(By.XPATH, sound_btn_xpath)
        time.sleep(0.5)
        sound_btn.click()

        dwnload_audio_btn_xpath = r'/html/body/div/div/div[7]/a'
        dwnload_audio_btn = driver.wait_and_get_element(By.XPATH, dwnload_audio_btn_xpath)
        dwnload_audio_btn.click()
        new_window = driver.wait_and_get_next_window(timeout=4000)
        driver.switch_to.window(new_window)
        print(f"this is the new window url: {driver.current_url}")

        
        driver.close_current_tab_and_return_to_main_tab()

        temp_mp3_path = download_mp3_url(driver.current_url)
        text_from_sound = audio_file_to_text(mp3_to_wav(temp_mp3_path))
        text_from_sound_field_xpath = r'/html/body/div/div/div[6]/input'
        

        driver.fill_input(By.XPATH, text_from_sound_field_xpath, text_from_sound)
        verify_recaptcha_btn_xpath = r'/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button'
        driver.click_element(By.XPATH, verify_recaptcha_btn_xpath)
        time.sleep(1)
        

    def pass_recaptcha(driver):
        recaptcha_frame_xpath = "/html/body/div[4]/main/div/div[2]/div[2]/div/div/form/div[2]/div[1]/div/div/div/iframe"
        recaptcha_element = driver.click_and_get_recaptcha(recaptcha_frame_xpath)
        recaptcha_passed = driver.wait_for_recaptcha_status(recaptcha_element, timeout=1000)
        time.sleep(1)

        if recaptcha_passed:
            driver.switch_to.default_content()
            driver.click_submit()
        else:
            driver.bypass_recaptcha()
            


    def fill_curp_field(driver, curp_str):
        curp_entry_xpath = r'/html/body/div[4]/main/div/div[2]/div[2]/div/div/form/div[1]/input'
        driver.fill_input(By.XPATH, curp_entry_xpath, curp_str)


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


def main(args):
    print(args)
    curp = args[1]
    vin = args[2]

    valid_proxy = filter_valid_proxy(get_proxies())

    while not valid_proxy:
        print("nigun proxy fue valido, intentando otra vez")
        valid_proxy = filter_valid_proxy(get_proxies())



    my_driver = SatAppointmentsDriver(driver_path=chrome_driver_path, proxy=valid_proxy)
    my_driver.maximize_window()
    my_driver.get(urls["regularizacion-autos"])
    my_driver.fill_curp_field(curp)
    time.sleep(1)

    my_driver.pass_recaptcha()
    
    my_driver.select_my_module("Rio Bravo")
    my_driver.check_calendar()


if __name__=="__main__":
    main(sys.argv)
