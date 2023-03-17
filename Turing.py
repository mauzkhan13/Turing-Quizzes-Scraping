# Importing necessary libraries

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

#Setting Chrome options and opening the URL

chrome_options = webdriver.ChromeOptions()
url = 'https://developers.turing.com/dashboard/takechallenge'
driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', options=chrome_options)
driver.get(url)
driver.maximize_window()

#Finding the Username and Password elements, entering the credentials and logging in

userName = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/div/input')
userName.send_keys('username')
sleep(3)
password = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[2]/div/input')
password.send_keys('password')
sleep(2)
login= driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/form/div[3]/div/button').click()
sleep(2)

#Clicking on the Quizzes option and selecting the first quiz on the page
quizzes_options = driver.find_element(By.XPATH,'//a[@class="icon navigation-icon"][2]').click()

quiz_name = driver.find_element(By.XPATH,'//span[@class="turing-ui-v2-mcq-tests-item-title"]')
print(quiz_name)

quiz_time = driver.find_element(By.XPATH,'//span[@class="turing-ui-v2-mcq-tests-item-time-estimate"]')
print(quiz_time)

#Starting the quiz by clicking on the 'Start' button
start_quiz = driver.find_element(By.XPATH,'//button[@class="ant-btn turing-ui-v2-action-item turing-ui-v2-action-item-start ant-btn-link"]').click()


# Setting the path to the Tesseract executable and initializing variables to store questions and answer options

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

questions = []
answer_options = []

#Setting up a folder path to store screenshots

folder_path = r'C:'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

#Initializing a flag to determine if all questions have been answered

finished = False

#Looping through the questions until all have been answered

while not finished:
    ## Finding and scrolling to all images on the page, taking a screenshot, and performing OCR on the top-left portion of the screenshot to extract the question text
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
        questions.append(text)

        sleep(3)
        # Save the screenshot with a unique filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        driver.save_screenshot(os.path.join(folder_path, f'screenshot_{timestamp}.png'))
            
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
path = r'C:Turing.csv'
df.to_csv(path, index=False)
