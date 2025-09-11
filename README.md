# Easy-Payload
belows is explained how Easy Payload works and how to use it or run it for some changes you wuold make

#1 Dependencies
Easy Payload use a bunch of python library to work like:
- PyQt6 for the GUI
- Pandas for reading files and extract values
- numpy for the 3d maths
- plotly for the 3D bin packing design in the web page

#2 How it works
divided in different points is explained the workflow of the software

#2.1 Set the .csv path
the first thing you have to do is type the path of the csv file or browse the file system to find the file

#2.2 Set the bin type
next you to select the real dimension of your bin (width, height, depth, max weight supported):
- container= 2.30, 2.36, 12.03, 30480
- tractor-trailer= 2.40, 2.36, 8.00, 10000
- tumbler truck= 2.40, 2.36, 13.60,24000

#2.3 Set your .csv fields
Easy Payload extract the data of the object in your payload from a .csv packing list (data like weight, lenght, height, ID, ecc...) and use it for fitting the your payload items in the container in the best way. When you open the software you have to insert in the designed space the exact names of your .csv file fields (example: if the fields with the name of the items is called "ID", you have to insert "ID" in the software".). This is important because they will be saved in a txt file and they will be used by pandas to access and extract data from the .csv file (like a database query). ATTENTION you need to set the fields only the first time you use the software

#3 Pyinstaller bundle compiling
the 3 main file will be compiled into a pyinstaller bundle (with all the dependencies) in one folder by this command:
pyinstaller --onedir --windowed --add-data icon.ico:. --icon=icon.ico --hidden-import pandas --hidden-import plotly --hidden-import numpy --hidden-import PyQt6 --name="Easy Payload" --exclude PyQt5 main.py

this folder will be copied in the users pc by the "Easy Payload setup.py" file that will be compiled into a .exe file with this command:
pyinstaller --onefile --windowed --icon="icon.ico" --hidden-import=PyQt6 --add-data "Easy Payload;Easy Payload" --add-data "icon.ico;." --exclude PyQt5 "Easy Payload setup.py"

#4 Reccomendations 
-The folder with first Pyinstaller bundel (the folder) will be insert into the .exe installer by the "--add-data" property and the installer can access and manipolate the into the folder by the  sys.MEIPASS property and the global variable in the in the first 40 line fo the code (line 0 to 40 in "Easy Payload setup.py")
-The file "main.py" is the heart of the application and it decide the workflow of the application and all of the cases, every function in the other file is initiated in the "main.py" file.
