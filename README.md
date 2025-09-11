# Easy-Payload
belows is explained how Easy Payload works and how to use it or run it for some changes you wuold make

#1 Dependencies
Easy Payload use a bunch of python library to work like:
- PyQt6 for the GUI
- Pandas for reading files and extract values
- numpy for the 3d maths
- plotly for the 3D bin packing design in the web page

#2 How it works

#2.1 Set the .csv path

#2.2 Set the bin type

#2.3 Set your .csv fields
Easy Payload extract the data of the object in your payload from a .csv packing list (data like weight, lenght, height, ID, ecc...) and use it for fitting the your payload items in the container in the best way. When you open the software you have to insert in the designed space the exact names of your .csv file fields (example: if the fields with the name of the items is called "ID", you have to insert "ID" in the software".). This is important because they will be saved in a txt file and they will be used by pandas to access and extract data from the .csv file (like a database query).
