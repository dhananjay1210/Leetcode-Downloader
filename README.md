# Leetcode-Downloader

This is web scraping program to download all your Leetcode submission.<br />
<br />
**How to use?** <br />
You just need 3 things. <br />
- Check your Chrome browser version and download suitable chromedriver from here(8-10 MB file) - https://chromedriver.chromium.org/downloads <br />
- Download download_submission_links.ipynb (provided above)
- Download download_codes.ipynb (provided above)
<br />
Put chromedriver, above two ipython notebook file in same folder and provide this as root directory in both the codes. You do not need to create any directory or file except these 3. Required directory/files will be created during runtime. If you are not a python user, go through the comments. <br />
Provide your leetcode username and password in both the codes. <br />
- Run download_submission_links.ipynb to extract your all submision link. This will be saved in "code_links" folder. <br />
- Run download_codes.ipynb to download your all codes. They will be saved categotywise(i.e. accepted, wrong answer, TLE etc.) in "codes" folder. Filename is question name of Leetcode problem + your leetcode submission id. <br /> 
- Watch automation on browser, it is fun :) <br />

<br />
Share this with your friends! Happy Leetcoding!! <br />
Put a star, if you like this project.
