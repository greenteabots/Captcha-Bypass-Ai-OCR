from io import BytesIO
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from ocrspaceapi import *
import json
import uuid
import os
import random

def get_views(apikey, link):
    proxy_list = 'proxies.txt'

    with open(proxy_list, 'r') as f:
        proxies = f.readlines()
    while True:
        try:
            proxy = random.choice(proxies)
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server={}'.format(proxy))
            options.headless = False
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(chrome_options=options)
            driver.maximize_window()
            driver.get('https://zefoy.com/')

            #wait timer
            time.sleep(8)

            # Take a screenshot of the entire page
            screenshot = driver.get_screenshot_as_png()

            # Convert the screenshot to a Pillow image
            screenshot_image = Image.open(BytesIO(screenshot))

            # Find the element that contains the captcha image
            captcha_element = driver.find_element(By.CSS_SELECTOR, 'img.img-thumbnail.card-img-top')

            # Get the bounding box of the captcha element
            captcha_rect = captcha_element.rect

            # Crop the screenshot image to the bounding box of the captcha element
            captcha_image = screenshot_image.crop((captcha_rect['x'], captcha_rect['y'], captcha_rect['x'] + captcha_rect['width'], captcha_rect['y'] + captcha_rect['height']))

            # Save the captcha image with random number in the name
            #captcha_image.save(random.randint(1, 1000) + 'captcha.png')
            randomuuid = str(uuid.uuid4())
            captcha_image.save(randomuuid + '.png')

            print('Captcha image saved to "captcha.png"')

            # READ THE IMAGE TO TEXT USING OCR

            text = ocr_space_file(filename=randomuuid + '.png', language='eng', api_key=apikey)

            data = json.loads(text)

            line_text = data['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText']

            print(line_text)
            text = line_text

            time.sleep(1)

            # Find the input field
            captcha_input_element = driver.find_element(By.NAME, 'captcha_secure')

            # Type the text into the input field
            try:
                captcha_input_element.send_keys(str(text))
            except StaleElementReferenceException:
                # Re-locate the input field
                captcha_input_element = driver.find_element(By.NAME, 'captcha_secure')

                # Type the text into the input field
                captcha_input_element.send_keys(str(text))

            # Press the "Enter" key to submit the form
            captcha_input_element.send_keys(Keys.RETURN)

            time.sleep(2)

            # Find the button element
            buttons = driver.find_elements(By.CSS_SELECTOR, '.btn.menu4')
            button_index = 0  # change this to the index of the button you want to press
            desired_button = buttons[button_index]
            desired_button.click()
            time.sleep(2)

            input_element = driver.find_element(By.XPATH,
                                                '/html/body[@class="text-center arka-plan-color"]/div[@class="container"]/div[@id="sid4"]/div[@class="card m-b-20 card-ortlax"]/form/div[@class="input-group mb-3"]/input[@class="form-control text-center font-weight-bold rounded-0"]')
            input_element.send_keys(link)
            time.sleep(3)
            driver.execute_script("document.elementFromPoint(1320, 167).click();")
            time.sleep(3)
            driver.execute_script("document.elementFromPoint(964, 217).click();")
            time.sleep(3)

            # close driver
            driver.close()
            os.remove(captcha_image.filename)
            print('Views Sent to link: ' + link)
        except Exception as e:
            # If there was an exception, print the error message and try again with a new proxy
            print(e)
            continue