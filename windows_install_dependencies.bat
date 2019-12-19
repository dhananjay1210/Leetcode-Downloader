:start
cls
echo ********** Installing Dependancies **********
set INPUT= "dependency.txt"
echo INPUT
pip install -r %INPUT%
 
pause