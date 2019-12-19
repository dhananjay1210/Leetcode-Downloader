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

print()
print()
print("************************************************************************")
print("************************************************************************")
print("*******                                                          *******")
print("*******              Welcome to Leetcode Downloader              *******")
print("*******                                                          *******")
print("************************************************************************")
print("************************************************************************")
print()
print()

# Input user's root path
print("Root directory is a path where this code file along with chromedriver is present")
print("e.g. For windows system     : G:\\Leetcode\\Mycodes")
print("e.g. For linux/mac system   : /home/Leetcode/Mycodes")
print("Enter your root directory : ",end = "")
root_path = input().strip()
print()

# Input OS
user_os = ""
retry = 0
while (user_os not in ["windows","linux"]) and retry < 5:
	print("Enter your operating syatem (windows/linux) : ",end = "")
	user_os = input().strip().lower()
	retry += 1
if retry == 5:
	print()
	print("Maximum attempt reached.")
	print("You entered invalid OS name...")
	print("Exiting...")
	sys.exit()
print()

# Create directories
print("Creating necessary directories/files... ")
os_dir_appender = {"windows" : '\\', "linux" : '/', "mac" : "/"}
if root_path[-1] not in os_dir_appender.values():
	root_path += os_dir_appender[user_os]
code = root_path + "codes" + os_dir_appender[user_os]                                            # Directory where your leetcode submission will be saved
code_links = root_path + "code_links" + os_dir_appender[user_os]                                 # Directory where your leetcode submission links will be saved
download_default_directory = root_path + "chrome_download" + os_dir_appender[user_os]            # Default Directory for chrome downloads
accepted_file = "accepted_code_link.txt"
wrong_answer_file = "wrong_answer_code_link.txt"
tle_file = "tle_code_link.txt"
runtime_error_file = "runtime_error_code_link.txt"
compile_error_file = "compile_error_code_link.txt"
all_file_list = [accepted_file, wrong_answer_file, tle_file, runtime_error_file, compile_error_file]

accepted_dir = code + "accepted_codes" + os_dir_appender[user_os]
wrong_answer_dir = code + "wrong_answer_codes" + os_dir_appender[user_os]
tle_dir = code + "tle_codes" + os_dir_appender[user_os]
runtime_error_dir = code + "runtime_error_codes" + os_dir_appender[user_os]
compile_error_dir = code + "compile_error_codes" + os_dir_appender[user_os]
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
      
print("Created necessary directories/files.")
print()


# Leetcode acc_type,username, password
print("Leetcode account details. Username,passward are case/whitespace sensitive.")
acc_type = ""
retry = 0
while retry < 5:
	print("Logging using which of the following accounts? Choose one of them : leetcode/linkedin/google/github/facebook")
	print()
	print("Enter account type : ",end = "")
	acc_type = input().strip().lower()
	if (acc_type not in ["leetcode","linkedin","google","github","facebook"]):
		print("Invalid account type")
		print()
		retry += 1
	else:
		print()
		print("Enter " + acc_type + " username : ",end = "")
		username = input()
		print("Enter " + acc_type + " password : ",end = "")
		pwd = input()
		break
if retry == 5:
	print()
	print("Maximum attempt reached.")
	print("You entered invalid account type...")
	print("Exiting...")
	sys.exit()
print()

#selenium configurations
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_default_directory,"safebrowsing.enabled": "false"}
chromeOptions.add_experimental_option("prefs",prefs)
if user_os == "windows":
	chromedriver = root_path + "chromedriver.exe"
else:
	chromedriver = root_path + "chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)


#user agent configurations
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'
print()

# Load website
driver.get("https://leetcode.com/accounts/login/")
time.sleep(3)
print("Website loaded")
print()


# Login to leetcode
if acc_type == "leetcode":
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
	
	try:
		err_msg = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p").text
		if "CAPTCHA" in err_msg:
			print("If captcha issue persist then connect to the VPN and rerun the code")
			print("                              OR                                   ")
			print("ENTER THE CAPTCHA AND THEN PRESS 'y' KEY FOLLOWED BY ENTER TO PROCEED : ",end = "")
			input()
			print()
			driver.find_element_by_xpath("//button[@class='btn__2FMG fancy-btn__CYhs primary__3S2m light__3zR9 btn__1eiM btn-md__3VAX ']").click()
			# You may increase below timer to 10 if you have slow internet connection.
			time.sleep(5)
			err_msg = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p").text
		if "username" in err_msg:
			print()
			print("Wrong username and/or password")
			print("Exiting...")
			print()
			sys.exit()
	except Exception as e:
		print("Login Successful")
		print()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
		
			
elif acc_type == "linkedin":
	driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/a[1]").click()
	time.sleep(5)
	linkedin_username_xpath = "/html/body/div/main/div/form/div[1]/input"
	
	already_present = driver.find_element_by_xpath(linkedin_username_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(linkedin_username_xpath).send_keys(Keys.BACKSPACE);
	# user name will be entered
	driver.find_element_by_xpath(linkedin_username_xpath).send_keys(username)
	time.sleep(1)
	
	linkedin_password_xpath = "/html/body/div/main/div/form/div[2]/input"
	already_present = driver.find_element_by_xpath(linkedin_password_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(linkedin_password_xpath).send_keys(Keys.BACKSPACE);
	# password will be entered
	driver.find_element_by_xpath(linkedin_password_xpath).send_keys(pwd)
	time.sleep(1)
	
	linkedin_sign_in_xpath = "/html/body/div/main/div/form/div[3]/button"
	driver.find_element_by_xpath(linkedin_sign_in_xpath).click()
	# You may increase below timer to 10 if you have slow internet connection.
	time.sleep(5)
	
	try:
		# If error occurs, then exit
		err_linkedin_username = "/html/body/div/main/div/form/div[1]/div" # Please enter a valid username
		err_mes_username = driver.find_element_by_xpath(err_linkedin_username).text
		if(len(err_mes_username) > 0):
			print("You entered wrong username.")
			print("Exiting...")
			sys.exit()
	except Exception as e:
		# correct username, check password
		pass
		
	try:
		err_linkedin_password = "/html/body/div/main/div/form/div[2]/div" # Hmm, that's not the right password   or    The password you provided must have at least 6 characters.
		err_mes_password = driver.find_element_by_xpath(err_linkedin_password).text
		if(len(err_mes_password) > 0):
			print("You entered wrong password.")
			print("Exiting...")
			sys.exit()
	
	except Exception as e:
		# If password is correct then check for captcha.	
		try:
			linkedin_captcha = "/html/body/div/main/div"
			linkedin_captcha_msg = driver.find_element_by_xpath(linkedin_captcha).text
			if len(linkedin_captcha_msg) > 0:
				print("If captcha issue persist then connect to the VPN and rerun the code")
				print("                              OR                                   ")
				print("ENTER THE CAPTCHA AND THEN PRESS 'y' KEY FOLLOWED BY ENTER TO PROCEED : ",end = "")
				input()
				print()
		except Exception as e:
			# Catptcha page did not appear.
			pass
			
		# Check for allow button
		try:
			linkedin_allow = "/html/body/div/div[2]/form/button"
			linkedin_allow_text = driver.find_element_by_xpath(linkedin_allow).text
			if linkedin_allow_text.lower() == "Allow":
				driver.find_element_by_xpath(linkedin_allow).click()
		except Exception as e:
			# Allow button Linked in page does not appeared.. Signed in successfully.
			pass
		print("Login Successful")
		print()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
		
	
elif acc_type == "google":
	driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/a[2]").click()
	time.sleep(5)
	google_username_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
	
	already_present = driver.find_element_by_xpath(google_username_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(google_username_xpath).send_keys(Keys.BACKSPACE);
	# user name will be entered
	driver.find_element_by_xpath(google_username_xpath).send_keys(username)
	time.sleep(1)
	google_username_next_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div"
	driver.find_element_by_xpath(google_username_next_xpath).click()
	time.sleep(5)
	try:
		# If error occurs, then exit
		goole_uname_err_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[2]/div[2]/div/span"
		err_mes = driver.find_element_by_xpath(goole_uname_err_xpath).text
		if "Couldn't find" in err_mes:
			print("You entered wrong username.")
		else:
			print("Some error occured. Try after some time.")
		print("Exiting...")
		sys.exit()
	except Exception as e:
		# If username is correct then only proceed
		google_password_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
		already_present = driver.find_element_by_xpath(google_password_xpath).get_attribute('value')
		for i in range(len(already_present)+1):
			driver.find_element_by_xpath(google_password_xpath).send_keys(Keys.BACKSPACE);
		# password will be entered
		driver.find_element_by_xpath(google_password_xpath).send_keys(pwd)
		time.sleep(1)
		google_password_next_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div"
		driver.find_element_by_xpath(google_password_next_xpath).click()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
		
		try:
			# If error occurs, then exit
			goole_err_xpath = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[2]/div[2]/span"
			err_mes = driver.find_element_by_xpath(goole_err_xpath).text
			if "Wrong password" in err_mes:
				print("You entered wrong password")
			else:
				print("Some error occured. Try after some time.")
			print("Exiting...")
			sys.exit()
		except Exception as e:
			# If password is correct then only proceed.
			print("Login Successful")
			print()
			# You may increase below timer to 10 if you have slow internet connection.
			time.sleep(5)
			
	
elif acc_type == "github":
	driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/a[3]").click()
	time.sleep(5)
	
	github_username_xpath = "/html/body/div[3]/main/div/form/div[2]/input[1]"
	
	already_present = driver.find_element_by_xpath(github_username_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(github_username_xpath).send_keys(Keys.BACKSPACE);
	# user name will be entered
	driver.find_element_by_xpath(github_username_xpath).send_keys(username)
	time.sleep(1)
	
	github_password_xpath = "/html/body/div[3]/main/div/form/div[2]/input[2]"
	already_present = driver.find_element_by_xpath(github_password_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(github_password_xpath).send_keys(Keys.BACKSPACE);
	# password will be entered
	driver.find_element_by_xpath(github_password_xpath).send_keys(pwd)
	time.sleep(1)
	
	github_sign_in_xpath = "/html/body/div[3]/main/div/form/div[2]/input[8]"
	driver.find_element_by_xpath(github_sign_in_xpath).click()
	# You may increase below timer to 10 if you have slow internet connection.
	time.sleep(5)
	
	
	try:
		# If error occurs, then exit
		err_github_username_or_password = "/html/body/div[3]/main/div/form/div[2]/div/div" # Incorrect username or password.
		err_mes_username = driver.find_element_by_xpath(err_github_username_or_password).text
		if(len(err_mes_username) > 0):
			print("You entered wrong username or password.")
			print("Exiting...")
			sys.exit()
	except Exception as e:
		'''
		# If password is correct then check for captcha.	
		linkedin_captcha = "/html/body/div/main/div"
		try:
			linkedin_captcha_msg = driver.find_element_by_xpath(linkedin_captcha).text
			if len(linkedin_captcha_msg) > 0:
				print("If captcha issue persist then connect to the VPN and rerun the code")
				print("                              OR                                   ")
				print("ENTER THE CAPTCHA AND THEN PRESS 'y' KEY FOLLOWED BY ENTER TO PROCEED : ",end = "")
				input()
				print()
		except Exception as e:
		'''
		print("Login Successful")
		print()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
	
elif acc_type == "facebook":
	driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/a[4]").click()
	time.sleep(5)
	
	try:
		fb_username_xpath = "/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input"
	
		already_present = driver.find_element_by_xpath(fb_username_xpath).get_attribute('value')
		for i in range(len(already_present)+1):
			driver.find_element_by_xpath(fb_username_xpath).send_keys(Keys.BACKSPACE);
		# user name will be entered
		driver.find_element_by_xpath(fb_username_xpath).send_keys(username)
		time.sleep(1)
		
		fb_password_xpath = "/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input"
		already_present = driver.find_element_by_xpath(fb_password_xpath).get_attribute('value')
		for i in range(len(already_present)+1):
			driver.find_element_by_xpath(fb_password_xpath).send_keys(Keys.BACKSPACE);
		# password will be entered
		driver.find_element_by_xpath(fb_password_xpath).send_keys(pwd)
		time.sleep(1)
		
		fb_sign_in_xpath = "/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button"
		driver.find_element_by_xpath(fb_sign_in_xpath).click()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
		
	except Exception as e:
		# Maybe already logged in to facebook
		pass
		
	try:
		# after above login
		fb_cont_sign_in_xpath = "/html/body/div[3]/div[2]/div/div/form/div/div[1]/div[2]/div[1]/div[1]/button"
		driver.find_element_by_xpath(fb_cont_sign_in_xpath).click()
		time.sleep(5)
	except Exception as e:
		try:
			fb_cont_sign_in_xpath = "/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button"
			driver.find_element_by_xpath(fb_cont_sign_in_xpath).click()
			time.sleep(5)
		except Exception as e:
			pass
			#print("Some error occured. Try after some time.")
			#print("Exiting...")
			#sys.exit()
	
	print("Login Successful")
	print()
	# You may increase below timer to 10 if you have slow internet connection.
	time.sleep(5)

leetcode_submission_link = "https://leetcode.com/submissions/" 
driver.get(leetcode_submission_link)
time.sleep(3)
print("Webpage for all submission loaded.")
print()

try:
	if driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/h4").text:
		print("Submission links loaded successfully...")
		print()
except Exception as e:
	print("Login attempt failed. Please try again.")
	print("Exiting...")
	sys.exit()


print("Downloading links of submission...")
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
print("All submission link saved in folder : ",code_links)
print()



def remove_invalid(que_name,invd):
    return que_name.replace(invd, "")

print("Downloading your codes...")
for i in range(len(all_file_list)):
    file_name = all_file_list[i]
    file_dir = all_file_dir[i]
    
    with open(code_links + file_name) as f:
        cnt = 0
        for submission_link in f:
            sub_id = submission_link.split("/")[-2]
            #print(sub_id)
            driver.get(submission_link)
            
            # Increase this timer to 8 if you have slow internet connection
            time.sleep(6)
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

print()
print("All codes downloaded in folder : ",code)	 
driver.close()