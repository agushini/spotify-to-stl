from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import os
import errno


def get_svg_code(url):
    track_name = url[14:]
    file_name = f"spcode-{track_name}.svg"
    print(file_name)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path2 = fr"{dir_path}\output"

    try:
        os.mkdir(dir_path2)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": dir_path2,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument("--window-size=1920,1080")
    #options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.77 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.spotifycodes.com/")
    spotify_url = driver.find_element_by_id('playlist-code')
    spotify_url.clear()
    spotify_url.send_keys(url)


    get_code_btn = driver.find_element_by_css_selector('.l-btn.uri-button') 
    get_code_btn.send_keys(Keys.ENTER)
    time.sleep(2)

    # dismiss the acknowledgements modal 
    # scroll to bottom of modal and wait to give it time to catch up
    #link_in_modal = driver.find_element_by_partial_link_text('Terms and Conditions')
    #link_in_modal.send_keys(Keys.SHIFT)
    #link_in_modal.send_keys(Keys.END)
    modal_accept = driver.find_element_by_class_name('accept-button')

    frame = driver.find_element_by_id('modal-content')
    driver.switch_to.frame(frame)
    driver.execute_script("arguments[0].scrollIntoView()", modal_accept)
    time.sleep(2)
   
    # click accept
    modal_accept.click()

    #switch out of frame mode
    driver.switch_to.default_content()

    bg_color_input = driver.find_element_by_name('back-color')
    bg_color_input.clear()
    bg_color_input.send_keys('#FFFFFF')
    bg_color_input.send_keys(Keys.ENTER)

    bar_col = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/div[2]/input')
    bar_col.click()
    time.sleep(0.1)

    bar_black = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/div[2]/div/div[2]')
    bar_black.click()

    choose_format = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/div[4]/input')
    choose_format.click()
    time.sleep(0.1)

    format_png = driver.find_element_by_xpath('//html/body/div[2]/div[4]/div[1]/div/div[2]/div[4]/div/div[1]')
    format_png.click()

    download = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]/div/div[1]/a')
    download_btn = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/div/div[1]/a/button")

    while True:
        href = str(download.get_attribute('href'))
        print(href)
        if href is not None and href != 'https://www.spotifycodes.com/#create' \
                and href != 'https://www.spotifycodes.com/' \
                and href != 'https://www.spotifycodes.com/#':
            break
    download_btn.click()
    print('click')
    time.sleep(10)
    return file_name
