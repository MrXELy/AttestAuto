from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, \
    WebDriverException, ElementNotInteractableException, ElementClickInterceptedException, \
    TimeoutException
from adresses import adresses
from time import sleep
import os

ATTESTATIONS_PATH = './Attestations'
CHROME_PROFILE_PATH = './CustomProfile'

def download_wait(path_to_downloads): # From https://stackoverflow.com/a/51949811
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 10:
        sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds

def set_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=' + CHROME_PROFILE_PATH)
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--disable-extensions')
    prefs = {"download.default_directory": ATTESTATIONS_PATH, # ! Does not seem to work
             "download.prompt_for_download": False,
             "directory_upgrade": True,
             "safebrowsing_for_trusted_sources_enabled": False,
             "safebrowsing.enabled": False
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    return options


def open_chrome(options: webdriver.ChromeOptions):
    print('[LOG] Opening Chrome...')
    driver = webdriver.Chrome(options=options)
    print('[SUCCESS] Chrome opened')
    return driver


def open_page(driver: webdriver.Chrome, URL):
    print('[LOG] Opening page...')
    driver.get(URL)
    try:
        element_tmp = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-profile"]')))
        print('[LOG] Page loaded')
    except TimeoutException:
        print('[FAIL] Can not open page : Timeout')
        driver.quit()
        exit()
        

def fill(driver: webdriver.Chrome, personne):
    print('[LOG] Filling...')
    
    driver.find_element_by_xpath('//*[@id="field-firstname"]').click()
    driver.find_element_by_xpath('//*[@id="field-firstname"]').send_keys(adresses[personne]['prenom'])
    
    driver.find_element_by_xpath('//*[@id="field-lastname"]').click()
    driver.find_element_by_xpath('//*[@id="field-lastname"]').send_keys(adresses[personne]['nom'])
    
    driver.find_element_by_xpath('//*[@id="field-birthday"]').click()
    driver.find_element_by_xpath('//*[@id="field-birthday"]').send_keys(adresses[personne]['date_de_naissance'])
    
    driver.find_element_by_xpath('//*[@id="field-lieunaissance"]').click()
    driver.find_element_by_xpath('//*[@id="field-lieunaissance"]').send_keys(adresses[personne]['lieu_de_naissance'])
    
    driver.find_element_by_xpath('//*[@id="field-address"]').click()
    driver.find_element_by_xpath('//*[@id="field-address"]').send_keys(adresses[personne]['adresse'])
    
    driver.find_element_by_xpath('//*[@id="field-town"]').click()
    driver.find_element_by_xpath('//*[@id="field-town"]').send_keys(adresses[personne]['ville'])
    
    driver.find_element_by_xpath('//*[@id="field-zipcode"]').click()
    driver.find_element_by_xpath('//*[@id="field-zipcode"]').send_keys(adresses[personne]['code_postal'])
    
    driver.find_element_by_xpath('//*[@id="checkbox-courses"]').click()
    
    print('[SUCCESS] Filled!')
    
    driver.find_element_by_xpath('//*[@id="generate-btn"]').click()

    print('[LOG] Downloading...')
    
    if download_wait(r"C:\Users\Robin\Downloads") >= 10:
        print('[FAIL] Download failed : Timeout')
        driver.quit()
        exit()

    print('[SUCESS] File downloaded in', r"C:\Users\Robin\Downloads")