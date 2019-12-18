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

## Edit below root_path - It is a path where this code file along with chromedriver, download_submission_links.py are present.
## e.g. For windows system : root_path = "G:\\Leetcode\\Mycodes\\"
## e.g. For linux system   : root_path = "/home/Leetcode/Mycodes/"
root_path = "your_root_path"


# If you are windows user do not touch the below directory names.
# For linux user - Just replace "\\" at the end of each DIRECTORY (not .txt file) with '/'. DO NOT CHANGE THE DIRECTORY NAMES AND TEXT FILE NAME!!
# e.g. code = root_path + "codes/"
download_default_directory = root_path + "chrome_download\\"               # Default Directory for chrome downloads
code = root_path + "codes\\"                                               # Directory where your leetcode submission will be saved
code_links = root_path + "code_links\\"                                    # Directory where your leetcode submission links will be saved
accepted_file = "accepted_code_link.txt"
wrong_answer_file = "wrong_answer_code_link.txt"
tle_file = "tle_code_link.txt"
runtime_error_file = "runtime_error_code_link.txt"
compile_error_file = "compile_error_code_link.txt"
all_file_list = [accepted_file, wrong_answer_file, tle_file, runtime_error_file, compile_error_file]

accepted_dir = code + "accepted_codes\\"
wrong_answer_dir = code + "wrong_answer_codes\\"
tle_dir = code + "tle_codes\\"
runtime_error_dir = code + "runtime_error_codes\\"
compile_error_dir = code + "compile_error_codes\\"
all_file_dir = [accepted_dir, wrong_answer_dir, tle_dir, runtime_error_dir, compile_error_dir]
extention_of = {"cpp" : ".cpp",
                "java" : ".java",
                "python" : ".py",
                "python3" : ".py",
                "c" : ".c",
                "csharp" : ".cs",
                "javascript" : ".js",
                "ruby" : ".ruby",
                "swift" : ".swift",
                "golang" : ".go",
                "scala" : ".scala",
                "kotlin" : ".kt",
                "rust" : ".rs",
                "mysql" : ".sql"}


# Create all above directory and files if not present already
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
        
try:
    os.makedirs(accepted_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs(wrong_answer_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
try:
    os.makedirs(tle_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
try:
    os.makedirs(runtime_error_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs(compile_error_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
        
        
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
time.sleep(1)
print("Website loaded")



#Login
# Clear username field
already_present = driver.find_element_by_name("login").get_attribute('value')
for i in range(len(already_present)+1):
    driver.find_element_by_name("login").send_keys(Keys.BACKSPACE);

# enter user name
driver.find_element_by_name("login").send_keys(username)
time.sleep(1)

# Clear password field
already_present = driver.find_element_by_name("password").get_attribute('value')
for i in range(len(already_present)+1):
    driver.find_element_by_name("password").send_keys(Keys.BACKSPACE);

# enter password
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
    
    
    
def remove_invalid(que_name,invd):
    return que_name.replace(invd, "")


for i in range(len(all_file_list)):
    file_name = all_file_list[i]
    file_dir = all_file_dir[i]
    
    with open(code_links + file_name) as f:
        cnt = 0
        for submission_link in f:
            sub_id = submission_link.split("/")[-2]
            #print(sub_id)
            driver.get(submission_link)
            
            # Increase this timer to 6 if you have slow internet connection
            time.sleep(3)
            que_name = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/h4/a")[0].text
            
            for invd in ['?','/','\\',':','*','<','>','|','"']:
                if invd in que_name:
                    que_name = remove_invalid(que_name,invd)
            code_in_list = []
            code_lines = driver.find_elements_by_class_name("ace_line")
            prog_lang = driver.find_elements_by_id("result_language")[0].text.strip()

            # create file
            with open(file_dir + que_name + "_" + str(sub_id) + extention_of[prog_lang] , 'w') as f2:
                pass

            # write code
            #print("Downloading ", que_name + extention_of[prog_lang])
            with open(file_dir + que_name + "_" + str(sub_id) + extention_of[prog_lang], 'a') as f2:
                for line in code_lines:#.find_elements(By.TAG_NAME, "div"):
                    f2.writelines(line.text)
                    f2.writelines("\n")
            cnt += 1
    print(str(cnt) + " " + file_name.split('.')[0] + " downloaded." )
    
    
driver.close()