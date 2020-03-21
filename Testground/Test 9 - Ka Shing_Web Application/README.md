# Parkinson's Data Web Application
## About
The web application serves to display Parkinson's data. The aim is build a web-based frontend GUI with HTML and CSS, as well as a backend server, both in Python. The GUI is targeted towarads researchers and its purpose is to display any metrics/statistics that have been determined throughout the Parkinson's Disease Sensors research project conducted by Team Marvel during the UCL academic year of 2019/2020. 

## How It Works
1. On the webpage hosting the GUI, the researcher logs in with their credentials. 
1. The researcher uploads a pair of CSV files (or a collection of CSV files) collected from the Metabase application on iOS/Android.
1. The GUI sends the CSV files to the server, which returns a dataframe of statistics.
    1. The server runs a series of functions (as determined by the developers) on the given CSV files. 
    1. Each function results in a single, or a group of, statistics. Each statistic will be added to a row in a dataframe.
    1. This dataframe is sent back to the GUI.
    1. At the same time, the CSV files are saved in a cloud folder online. 
    1. \[Optional]: The statistic dataframe can be saved in a cloud folder online. This is optional as the addition or removal of statistics in the future may likely necessitate re-running the series of functions (rather than just the set of additional functions) to ensure all statistics are consistent across CSV files. 
1. The researcher can view the statistics in the GUI.

## Notes
1. Based on the information found on [AWS Free](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc), the AWS service remains free even after a year. 

## Problems
1. Currently, there is a question of which online storage will be appropriate to use for the storage of sensitive medical data. Read [here](https://aws.amazon.com/blogs/architecture/store-protect-optimize-your-healthcare-data-with-aws/) for better understanding of whether it's appropriate. 
1. Currently, our access key is from the Root account. According to AWS best practices, it is best to use the root account to generate an IAM user; we then use the IAM user's credentials for the script. 

## Resources
 - https://www.youtube.com/watch?v=6WruncSoCdI

## To-Do
### Main Branch
 - [x] <b>offline_server</b> - Offline server: 
     Hosting the server and GUI on a local server. 
     - [x] Successful frontend and backend communication. 
 - [x] <b>aws_bucket_call</b> - AWS API Test:
     Testing if a Python script can GET from and POST to an S3 bucket; if only POST works, we can proceed
     - [x] GET successful
     - [x] POST successful
 - [x] <b>mock_server</b> - Online server:
     Hosting the server and GUI online.
     - [x] Hosting a random Python script with Flask.
     - [x] Saving arbitrary text files on the server. 
 - [ ] Implementation of actual functions:
     Implementation of actual functions rather than dummy ones. 
     - [ ] Server API equipped with a function returning a single dataframe. Does not need to contain all information as the intention is to make it scalable and generalisable to addition of future statistics.
     - [ ] GUI capable of uploading a CSV file and displaying a HTML table. 
     - [x] Successful saving of CSV files on server. 
     - [x] Ability to manually delete CSV files on server. \[(Unimplemented) Optional: Ability to 'exclude' files rather than deleting them outright using a property in the file's metadata. Overwriting files overwrites the exclusion metadata, causing them to be included by default.] 
     - [ ] Somehow, we need to let the researchers input the severity of the file. One method is by enforcing the naming conventions already used as they will name the files after they finish the test. Otherwise, a team meeting may be required to overcome the recording of the severity level. We would, preferably, wish to avoid a one-by-one inputting of the severity level as that essentially reintroduces the manual task of an extra click or two/extra typing per pair of CSV files. 
 - [ ] Implementation of multiple users:
     Ensure the server can be used by multiple users at the same time. 
     - [ ] Asynchronous execution of server API. 
     - [ ] Hosting of multiple sessions. Potentially require investigation into the number of writes called to Firebase per upload to extrapolate the number of uploads permissible (remaining) for the day. 
     - [ ] Ability to upload an entire set of files (as the researchers may be uninterested in uploading a single file one by one if the dataframe itself isn't going to give an objective understanding of the patient's condition yet).
     
### Branch 1: Strict Questionnaire
 - [ ] Generate a table of questionnaires for each uploaded file. Some sections should automatically be filled based on the required nomenclature. However, <b>all</b> fields should be filled up before they can be sent. 
 
### Branch 1-1: Lenient Questionnaire
 - [ ] Instead of asserting that all fields must be filled up before they can be sent, the fields that pass regulation can be sent; those that do not remain. 