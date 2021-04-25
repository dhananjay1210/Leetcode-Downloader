:start
cls
echo ********** Installing Dependancies **********
set INPUT= "dependency.txt"
echo INPUT
pip install -r %INPUT%
python leetcode_downloader.py
pause