from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os
import dotenv
import datetime
from dateutil import relativedelta

# Create your views here.
def index(request):
    num_jobs = {
        "current": [], 
        "next": []
    }
    # Load credentials
    dotenv.load_dotenv()
    admin_email = os.getenv('EMAIL')
    admin_password = os.getenv('PASSWORD')
    # Log into Jobber and find elements
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    wait = WebDriverWait(driver, 10)
    driver.get("https://www.getjobber.com/login")
    wait.until(EC.presence_of_element_located(("id", "email")))
    email = driver.find_element("id", 'email')
    email.send_keys(admin_email)
    password = driver.find_element("id", 'user_session_password')
    password.send_keys(admin_password)
    driver.find_element("xpath", '/html/body/div[1]/div/div[2]/div/div/div/div[1]/form/input[4]').click()
    wait.until(EC.presence_of_element_located(("xpath", '/html/body/div[2]/div/div[2]/div[1]/div[1]/nav/div[3]/a[2]')))
    driver.find_element("xpath", '/html/body/div[2]/div/div[2]/div[1]/div[1]/nav/div[3]/a[2]').click()
    wait.until(EC.presence_of_element_located(("xpath", '//*[@id="right-header-row"]/div[1]/div/button')))
    driver.find_element("xpath", '//*[@id="right-header-row"]/div[1]/div/button').click()
    wait.until(EC.presence_of_element_located(("xpath", '//*[@id="right-header-row"]/div[1]/div/div[1]/nav/a[4]')))
    driver.find_element("xpath", '//*[@id="right-header-row"]/div[1]/div/div[1]/nav/a[4]').click()
    time.sleep(1)
    # Current Month
    while driver.find_element("id", "current_date").text.split(" ")[1].lower() == datetime.datetime.strptime(str(datetime.date.today().month), "%m").strftime("%b").lower():
        wait.until(EC.presence_of_element_located(("class name", 'js-userRowList')))
        users = driver.find_element("class name", 'js-userRowList').find_elements("class name", 'user')
        if (driver.find_element("class name", 'js-tasksLabel').text.strip().split(" ")[0] != "0"):            
            # Populate number of jobs
            data = []
            for i in range(len(users)):
                data.append(users[i].text.replace("\n", " ").replace(" ", " - "))
            num_jobs["current"].append(data)
        else:
            # Populate number of jobs
            data = []
            for i in range(len(users)):
                text = "0 - " + "".join(users[i].text.replace('\n', ' ').split(" ")[1:])
                data.append(text)
            num_jobs["current"].append(data)
        driver.find_element("class name", "js-nextArrow").click();
        time.sleep(1)
    # Next Month
    while driver.find_element("id", "current_date").text.split(" ")[1].lower() == datetime.datetime.strptime(str(datetime.date.today() + relativedelta.relativedelta(months=1)).split("-")[1], "%m").strftime("%b").lower():
        wait.until(EC.presence_of_element_located(("class name", 'js-userRowList')))
        users = driver.find_element("class name", 'js-userRowList').find_elements("class name", 'user')
        if (driver.find_element("class name", 'js-tasksLabel').text.strip().split(" ")[0] != "0"):            
            # Populate number of jobs
            data = []
            for i in range(len(users)):
                data.append(users[i].text.replace("\n", " ").replace(" ", " - "))
            num_jobs["next"].append(data)
        else:
            # Populate number of jobs
            data = []
            for i in range(len(users)):
                text = "0 - " + "".join(users[i].text.replace('\n', ' ').split(" ")[1:])
                data.append(text)
            num_jobs["next"].append(data)
        driver.find_element("class name", "js-nextArrow").click();
        time.sleep(1)
    return render(request, "index.html", {"data": json.dumps(num_jobs)})
