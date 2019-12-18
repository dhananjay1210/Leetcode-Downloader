# Imports
from bs4 import BeautifulSoup
import re
import os
from time import sleep
import urllib.request 
import requests
import errno
import shutil
import sys
import traceback
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
import time


## Edit below root_path - It is a path where this code file along with chromedriver, download_codes.py are present.
## e.g. For windows system : root_path = "G:\\Leetcode\\Mycodes\\"
## e.g. For linux system   : root_path = "/home/Leetcode/Mycodes/"
root_path = "your_root_path"


# If you are windows user do not touch the below directory names.
# For linux user - Just replace "\\" at the end of each DIRECTORY (not .txt file) with '/'. DO NOT CHANGE THE DIRECTORY NAMES AND TEXT FILE NAME!!
# e.g. code = root_path + "codes/"
code = root_path + "codes\\"                                            # Directory where your leetcode submission will be saved
code_links = root_path + "code_links\\"                                 # Directory where your leetcode submission links will be saved
download_default_directory = root_path + "chrome_download\\"            # Default Directory for chrome downloads
accepted_file = "accepted_code_link.txt"
wrong_answer_file = "wrong_answer_code_link.txt"
tle_file = "tle_code_link.txt"
runtime_error_file = "runtime_error_code_link.txt"
compile_error_file = "compile_error_code_link.txt"

# Creates the above directory and files if not present already
try:
    os.makedirs(code)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs(download_default_directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
try:
    os.makedirs(code_links)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


with open(code_links + accepted_file,'w') as f:
    pass
with open(code_links + wrong_answer_file,'w') as f:
    pass
with open(code_links + tle_file,'w') as f:
    pass
with open(code_links + runtime_error_file,'w') as f:
    pass
with open(code_links + compile_error_file,'w') as f:
    pass



#selenium configurations
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_default_directory,"safebrowsing.enabled": "false"}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = root_path + "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)


#user agent configurations
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'



## Provide your leetcode username and password within a string.
# Load login page
username = "leetcode username"
pwd = "leetcode password"

driver.get("https://leetcode.com/accounts/login/")
time.sleep(3)
print("Website loaded")


#Login

# To Clear username field
already_present = driver.find_element_by_name("login").get_attribute('value')
for i in range(len(already_present)+1):
    driver.find_element_by_name("login").send_keys(Keys.BACKSPACE);

# user name will be entered
driver.find_element_by_name("login").send_keys(username)
time.sleep(1)

# To Clear password field
already_present = driver.find_element_by_name("password").get_attribute('value')
for i in range(len(already_present)+1):
    driver.find_element_by_name("password").send_keys(Keys.BACKSPACE);

# password will be entered
driver.find_element_by_name("password").send_keys(pwd)
time.sleep(1)


driver.find_element_by_xpath("//button[@class='btn__2FMG fancy-btn__CYhs primary__3S2m light__3zR9 btn__1eiM btn-md__3VAX ']").click()
# You may increase below timer to 10 if you have slow internet connection.
time.sleep(5)

if len(driver.find_elements_by_xpath("//ul[@class='nav navbar-nav']/li")):
    print("Login Successful")
else:
    print("Unable to login")
    print("Rerun this file...If captcha issue persist then the connect to VPN and rerun this file.")
    
    
leetcode_submission_link = "https://leetcode.com/submissions/" 
driver.get(leetcode_submission_link)
time.sleep(1)
print("Webpage for all submission loaded.")



while(True):
    for row in driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div/table/tbody/tr"):
        third_row_value = row.find_elements(By.TAG_NAME, "td")[2]               # get status column value from table
        status = third_row_value.find_elements(By.TAG_NAME, "strong")[0].text   # extract status from strong field
        submission_link = third_row_value.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')

        if status == "Accepted":
            with open(code_links + accepted_file,'a') as f:
                f.writelines(submission_link)
                f.writelines("\n")
        elif status == "Wrong Answer":
            with open(code_links + wrong_answer_file,'a') as f:
                f.writelines(submission_link)
                f.writelines("\n")
        elif status == "Time Limit Exceeded":
            with open(code_links + tle_file,'a') as f:
                f.writelines(submission_link)
                f.writelines("\n")
        elif status == "Runtime Error":
            with open(code_links + runtime_error_file,'a') as f:
                f.writelines(submission_link)
                f.writelines("\n")
        elif status == "Compile Error":
            with open(code_links + compile_error_file,'a') as f:
                f.writelines(submission_link)
                f.writelines("\n")
            
    try:
        # Load next submission page
        next_page = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div/nav/ul/li[2]")[0].find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
        print("Loading next page...",next_page)
        driver.get(next_page)
        # You may increase below timer to 6 if you have slow internet connection.
        time.sleep(3)
    except Exception as e:
        # If this is last submission page, then exit
        print("Next page not available.")
        print()
        break
print("All submission link saved.")



driver.close()
    
