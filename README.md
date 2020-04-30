# Leetcode-Downloader

This is web scraping program to download all your Leetcode submission.<br />
For more details, must read - https://medium.com/@dhananjaysonawane01/leetcode-downloader-9fefd1575c72 and follow the instructions.<br />
<br />
**How to use?** <br />
You just need 2 things. <br />
- Check your Chrome browser version and download suitable chromedriver.Just download this driver, do not run this file. Download from here(8-10 MB file) - https://chromedriver.chromium.org/downloads. Unzip the folder. <br />  

- All above code files
<br />

Put chromedriver.exe(windows user) / chromedriver(linux user), code file in same folder. You do not need to create any directory or file. Required directory/files will be created during runtime. Go through the comments in the codes.<br /> 
<br />

Run linux_install_dependencies.sh or windows_install_dependencies.bat code file <br />
<br />

Run leetcode_downloader.py and follow the on screen instruction. You will be asked your login credentials.<br />
(You might face warning/error after running "leetcode_downloader.py" :<br />
ERROR:ssl_client_socket_impl.cc(941)] handshake failed; returned -1, SSL error code 1, net_error -200<br />
You can **ignore** this warning/error )<br />
<br />

After successful execution : <br />
Your submision link will be saved in "code_links" folder. <br />
All your codes will be saved categotywise(i.e. accepted, wrong answer, TLE etc.) in "codes" folder. Filename is question name of Leetcode problem + your leetcode submission id. <br /> 
<br />

Watch automation on browser, it is fun :) <br />
<br />

Share this with your friends! Happy Leetcoding!! <br />
Put a star, if you like this project.
