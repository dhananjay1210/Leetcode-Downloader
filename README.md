# Leetcode-Downloader

This is web scraping program to download all your Leetcode submission.<br />
<br />
**How to use?** <br />
You just need 3 things. <br />
- Check your Chrome browser version and download suitable chromedriver.Just download this driver, do not run this file. Download from here(8-10 MB file) - https://chromedriver.chromium.org/downloads <br />  

- Download download_submission_links.py (provided above)
- Download download_codes.py (provided above)
<br />
Put chromedriver, above two code files in same folder and provide this as root directory in both the codes. You do not need to create any directory or file except these 3. Required directory/files will be created during runtime.<br /> 
Go through the comments in the codes. You need to initialte following 3 variables as they are user dependent:<br />
Provide root_code, your leetcode username, password in both the codes. <br />
- Run download_submission_links.py to extract your all submision link. This will be saved in "code_links" folder. <br />
- Run download_codes.py to download your all codes. They will be saved categotywise(i.e. accepted, wrong answer, TLE etc.) in "codes" folder. Filename is question name of Leetcode problem + your leetcode submission id. <br /> 
- Watch automation on browser, it is fun :) <br />

<br />
Share this with your friends! Happy Leetcoding!! <br />
Put a star, if you like this project.
