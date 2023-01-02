from io import BytesIO
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from ocrspaceapi import *
import json


apikey = input("Enter your API key from https://ocr.space/ (its free): ")
driver = webdriver.Chrome()
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

# Save the captcha image
captcha_image.save('captcha.png')
print('Captcha image saved to "captcha.png"')

# READ THE IMAGE TO TEXT USING OCR

text = ocr_space_file(filename='captcha.png', language='eng', api_key=apikey)

data = json.loads(text)

line_text = data['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText']

print(line_text)
text = line_text


time.sleep(20)

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
