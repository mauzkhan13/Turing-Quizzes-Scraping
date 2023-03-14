# Turing-Quizzes-Scraping
This code is a Python script that uses Selenium WebDriver to automate the process of taking a quiz on the Turing developers' website. The quiz contains multiple-choice questions, and the code navigates through each question, selects an answer, and records both the question and the answer option in a CSV file.

To achieve this, the script imports several libraries, including Selenium, Pandas, and Pytesseract. It also sets Chrome options, such as maximizing the browser window and setting the executable path for the Chrome browser.

The script then navigates to the quiz login page and logs in by entering the username and password. It clicks on the Quizzes option to open the quiz section, selects the first quiz on the page, and clicks on the Start button to begin the quiz.

Next, the script initializes variables to store the questions and answer options and sets up a folder path to store screenshots. It also sets a flag to determine if all questions have been answered.

The script then loops through each question until all questions have been answered. For each question, it first finds and scrolls to all images on the page, takes a screenshot, and performs OCR on the top-left portion of the screenshot to extract the question text. It saves the screenshot with a unique filename in the specified folder path.

It then waits for the answer options to load, retrieves the answer options, and saves them to the answer_options list. The script selects the first answer option by clicking on it using ActionChains.

If this is the final question, the script sets the finished flag to True and breaks out of the inner loop. Otherwise, it clicks on the next button to move to the next question and waits for the page to load.

After all questions have been answered, the script creates a Pandas DataFrame with the questions and answer options and saves it to a CSV file in the specified path.

Overall, this code demonstrates how Selenium WebDriver can be used to automate the process of taking quizzes and performing other repetitive tasks on websites.
