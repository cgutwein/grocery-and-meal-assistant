If you are running Chrome, you need to first run this command to enable the browser to read local files:
<chrome install path>/chrome.exe --allow-file-access-from-files
  
Steps to run:
0. Make sure you have installed all the necessary libraries included in the python script
1. Run $python recipe.py to stand up the web service
2. On your browser, go to URL: http://localhost:5000/home
3. You should see the welcome page. This gets rendered from the index.html file stored in the /templates folder
4. Enter selections and upload the sample file sample_list.csv
5. The program uploads the list, makes a copy of it, and then builds a html table from the copied csv
