# web-scraping-challenge - Mission to Mars

## Homework submission:

All files and folders that contain codes and correspondent input/output data & images are stored under the folder called _Missions_to_Mars_, except this ReadMe and gitignore files.

The folder structure of _Missions_to_Mars_ is as followed: </br>
1. Folder "css" contains: local styling css codes, including bootswatch
2. Folder "images" contains: several screen snapshots of the final application with date & time stamp; and a background image of the page.
3. Folder "output" contains: program output json file with the images of the hemispheres and their titles, called: _image_url.json_
4. Folder "templates" contains: application main page _index.html_ and program output file (from pandas jupyter notebook and python) that stored Mars Facts, called: _mars_facts.html_
5. Data scrapping files: _scrape_mars.py_ and jupyter notebook _mission_to_mars.ipynb_
6. The main Mission to Mars program file is called: _app.py_

**_Notes:_** </br>
  - Execute the main program by run the following command in the terminal: _python app.py_
  - _App.py_ will call function _scrape()_ in the file _scrape_mars.py_ and execute all the scrapping functions when the button _Scrape New Data_ is pressed. 
  - There will be no data to display on the page when the first time _index.html_ is load as nothing has been scrapped or stored in the local machine's MongoDB server.
