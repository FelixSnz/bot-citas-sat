from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time


def get_proxies():


    options = webdriver.ChromeOptions()
    
    options.add_argument("headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver')
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div/div[2]/div/table"))))
                                                                                                                                    
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, r"/html/body/section[1]/div/div[2]/div/table/tbody/tr[*]/td[1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, r"/html/body/section[1]/div/div[2]/div/table/tbody/tr[*]/td[2]")))]


    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])
    driver.quit()
    return proxies

def filter_valid_proxy(proxies):
    for proxy in proxies:
        try:
            print("Proxy selected: {}".format(proxy))
            options = ChromeOptions()
            options.add_argument("headless")
            options.add_argument('--proxy-server={}'.format(proxy))
            driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver')
            ip_check_url = r'https://whatismyipaddress.com/es/mi-ip'
            ip_check_url = r'https://www.regularizaauto.sspc.gob.mx/'
            #ip_check_url = r'https://www.whatismyip.com/proxy-check/?iref=home'
            driver.get(ip_check_url)
            curp_entry_xpath = r'/html/body/div[4]/main/div/div[2]/div[2]/div/div/form/div[1]/input'
            WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.XPATH, curp_entry_xpath)))
            return proxy
        except TimeoutException:
            continue
        except WebDriverException:
            continue
        finally:
            driver.quit()