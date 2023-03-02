from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import datetime
import random
import pytesseract
from PIL import Image
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import os
import re
import time
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException, TimeoutException)

chrome_options = webdriver.ChromeOptions()
url = 'https://developers.turing.com/dashboard/takechallenge'
driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', options=chrome_options)
driver.get(url)
driver.maximize_window()


login = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/div/input')
login.send_keys('@gmail.com')
sleep(3)
pswd = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[2]/div/input')
pswd.send_keys('password')
sleep(2)
okay = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[3]/div/button').click()
sleep(2)


# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

questions = []
answer_options = []


finished = False
while not finished:
    while True:
        try:
            image_elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="html-question"]/img')))
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        try:    
            for image_element in image_elements:
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass  
               
        driver.save_screenshot('screenshot.png')

        screenshot = Image.open('screenshot.png')
        screenshot_width, screenshot_height = screenshot.size
        cut_width = screenshot_width // 2
        cut_height = screenshot_height // 2
        left_top_cut = screenshot.crop((0, 0, cut_width, cut_height))

        text = pytesseract.image_to_string(left_top_cut).strip()
        text = re.sub(r'(Question \d+ of \d+)|(Something wrong with the question or blank content?.*?Report a problem\.)', '', text).strip()

        text = text.replace('7 Turing', '').replace('Data Engineer', '').replace('\n', '').strip()
        questions.append(text)
    
            
        try:
            options = WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="ql-editor"]/p')))
            option1 = [option.text for option in options]
            answer_options.append(option1)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
                
        
        try:
            selected_option = driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-default border-default option-card"][1]')
            actions = ActionChains(driver)
            actions.move_to_element(selected_option).click().perform()
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Finish')]")))
            finished = True
            break  # break out of the inner loop if this is the final question
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        # Click on the next button
        try:
            next_question = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class=" button-next"]')))
            next_question.click()
            time.sleep(random.uniform(2.1, 3))

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            #
            break
        
    if finished:
        break

# Create the DataFrame
df = pd.DataFrame(zip(questions,answer_options), columns=['Questions','Answers'])
path = r'C:\Users\Mauz Khan\Desktop\My Scrapy\Google Cloud Platform.csv'
df.to_csv(path, index=False)