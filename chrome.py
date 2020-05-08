from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, \
    WebDriverException, ElementNotInteractableException, ElementClickInterceptedException, \
    TimeoutException, NoAlertPresentException
from adresses import adresses
import time
import os

DEFAULT_DL_PATH = r"path\to\default\download\folder\\" # ! Last slash is important
ATTESTATIONS_PATH = './Attestations'
CHROME_PROFILE_PATH = './CustomProfile'


def find_file(dir: str, name: str) -> bool:
    """Return True if name is in dir

    :param dir: Path of a directory
    :type dir: str
    :param name: File name
    :type name: str
    :return: True or False
    :rtype: bool
    """ 
    for fname in os.listdir(dir):
        if fname == name:
            return True
    return False


def get_attestation_name(current_time=time.localtime()) -> str:
    """Returns name of attestation file created at current_time

    :param current_time: Time attestation is created, defaults to time.localtime()
    :type current_time: struct_time, optional
    :return: Name of attestion file as a String
    :rtype: str
    """
    return 'attestation-' + time.strftime("%Y-%m-%d_%H-%M", current_time) + '.pdf'


def download_wait(path_to_downloads): # From https://stackoverflow.com/a/51949811
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 30:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 0.5
    return seconds


def set_options():
    """Return chrome options

    :return: Chrome options
    :rtype: ChromeOptions
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    prefs = {"download.default_directory": ATTESTATIONS_PATH, # ! Does not seem to work
             "download.prompt_for_download": False,
             "directory_upgrade": True,
             "safebrowsing_for_trusted_sources_enabled": False,
             "safebrowsing.enabled": False
    }
    options.add_experimental_option('prefs', prefs)
    
    # DevTools logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Headless arguments
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=45449')
    
    return options


def enable_download_in_headless_chrome(driver, download_dir): # From https://stackoverflow.com/a/47366981
    # add missing support for chrome "send_command" to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


def open_chrome(options: webdriver.ChromeOptions):
    """Open a Google Chrome session, using options

    :param options: Chrome options
    :type options: webdriver.ChromeOptions
    :return: Driver
    :rtype: webdriver
    """
    print('[LOG] Opening Chrome...')
    driver = webdriver.Chrome(options=options)
    print('[SUCCESS] Chrome opened')
    
    enable_download_in_headless_chrome(driver, DEFAULT_DL_PATH)
    
    return driver


def open_page(driver: webdriver.Chrome, URL):
    """Open a page in a chrome driver

    :param driver: Chrome driver
    :type driver: webdriver.Chrome
    :param URL: Page URL
    :type URL: str
    """
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
    """Fill the attestation form and download it

    :param driver: Chrome driver
    :type driver: webdriver.Chrome
    :param personne: Person name
    :type personne: str
    :return: Attestation file name
    :rtype: str
    """
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

    # If there is an alert popup
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    
    attestation_name = get_attestation_name()
    current_time = time.time()
    
    print('[LOG] Downloading...')

    time.sleep(3)

    if download_wait(DEFAULT_DL_PATH) >= 30:
        print('[FAIL] Download failed : Timeout')
        driver.quit()
        exit()

    if find_file(DEFAULT_DL_PATH, attestation_name) is False:
        current_time -= 60
        attestation_name = get_attestation_name(time.localtime(current_time))
        if find_file(DEFAULT_DL_PATH, attestation_name) is False:
            print('[FAIL] Download failed: no file')
            driver.quit()
            exit()

    print('[SUCCESS] File downloaded in your default download folder')

    return attestation_name