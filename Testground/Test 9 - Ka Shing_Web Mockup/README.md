# Parkinson's Data Web Mockup 
## About
The web mockup serves to display Parkinson's data. The aim is to build a web-based frontend GUI (a.k.a. the GUI) which communicates with a Python script hosted on Firebase (a.k.a. the server). The GUI is targeted towards researchers and its purpose is to display any metrics/statistics that have been determined throughout the Parkinson's Disease Sensors research project conducted by Team Marvel during the UCL academic year of 2019/2020. 

## How It Works
1. On the webpage hosting the GUI, the researcher logs in with their credentials. 
1. The researcher uploads a pair of CSV files collected from the Metabase application on iOS/Android.
1. The GUI sends the CSV files to the server, which returns a dataframe of statistics.
    1. The server runs a series of functions (as determined by the developers) on the given CSV files. 
    1. Each function results in a single, or a group of, statistics. Each statistic will be added to a row in a dataframe.
    1. This dataframe is sent back to the GUI.
    1. At the same time, the CSV files are saved in a cloud folder online. 
    1. \[Optional]: The statistic dataframe can be saved in a cloud folder online. This is optional as the addition or removal of statistics in the future may likely necessitate re-running the series of functions (rather than just the set of additional functions) to ensure all statistics are consistent across CSV files. x
1. The researcher can view the statistics in the GUI.

## Problems
<b><i>Currently, there seems to be a CORS problem with the communication between Python Flask and the Angular webserver hosted. The same issue occurred when using Java Springboot with Angular back in the summer but a server-side (Java) fix seemed to remedy the issue. As of now, I can't find a similar solution for Flask yet. </i></b>

## To-Do
 - [ ] Offline server:
     The purpose of this offline server is to test out communication between server and GUI APIs.
     - [x] Laptop-hosted Python script with Flask 
     - [x] Laptop-hosted Angular 7 webpage
     - [] Successful communication between server and GUI
 - [ ] Online server:
     Hosting the above server and GUI online.
     - [ ] Successful communication between server and GUI
 - [ ] Implementation of actual functions:
     Implementation of actual functions rather than dummy ones. 
     - [ ] Server API equipped with a function returning a single dataframe. Does not need to contain all information as the intention is to make it scalable and generalisable to addition of future statistics.
     - [ ] GUI capable of uploading a CSV file and displaying a HTML table. 
     - [ ] Successful saving of CSV files on server. 
     - [ ] Ability to manually delete CSV files on server. \[Optional: Ability to 'exclude' files rather than deleting them outright using a property in the file's metadata. Overwriting files overwrites the exclusion metadata, causing them to be included by defaeult. ] 
     - [ ] Somehow, we need to let the researchers input the severity of the file. One method is by enforcing the naming conventions already used as they will name the files after they finish the test. Otherwise, a team meeting may be required to overcome the recording of the severity level. We would, preferably, wish to avoid a one-by-one inputting of the severity level as that essentially reintroduces the manual task of an extra click or two/extra typing per pair of CSV files. 
 - [ ] Implementation of multiple users:
     Ensure the server can be used by multiple users at the same time. 
     - [ ] Asynchronous execution of server API. 
     - [ ] Hosting of multiple sessions. Potentially require investigation into the number of writes called to Firebase per upload to extrapolate the number of uploads permissible (remaining) for the day. 
     - [ ] Ability to upload an entire set of files (as the researchers may be uninterested in uploading a single file one by one if the dataframe itself isn't going to give an objective understanding of the patient's condition yet).