If you are running Chrome, you need to first run this command to enable the browser to read local files:
<chrome install path>/chrome.exe --allow-file-access-from-files

Steps to run:  
0. Make sure you have installed all the necessary libraries included in the python scripts
1. For Mac enter the command `export FLASK_APP=recepticon.py`  
   For Windows enter the command `$env:FLASK_APP = 'recepticon.py'`
2. Navigate to the 'flask' folder and run the command `flask run`
3. On your browser, go to URL: `http://localhost:5000`
4. You will need to either login or register for a new account (Note: Keep in mind that at the moment username and login credentials are written to a static SQLite database.)
5. You should now see the welcome page. This gets rendered from the index.html file stored in the /templates folder
6. Enter selections and upload the sample file sample_list.csv
7. The program uploads the list, makes a copy of it, and then builds a html table from the copied csv

Users in db as of the latest push:

chet, nerothecat   
napoleon, iheartfood
