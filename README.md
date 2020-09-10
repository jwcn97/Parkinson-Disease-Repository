# Feature Engineering for Detection of Parkinson Disease Severity with Motion Sensor Arrays

This is the repository for the final year project undertaken by the following individuals: 
1. [Chan Jing Wei](https://github.com/jwcn97)
3. [Joseph Piong Ken Yew](https://github.com/KenYew)
2. [Liong Ka Shing](https://github.com/KaShing96)
4. [Tan Chin Yang](https://github.com/CYTan2209)

This project aims to explore potential metrics for the quantification of Parkinson's Disease severity. These metrics are intended to ultimately be fed into a machine learning algorithm, which ideally predicts and assigns a severity level for the disease.

This repository has been cleaned up where possible to facilitate browsing and is meant to be used in conjunction with the project report.

---

## Data
This folder holds the mock data used for the purposes of this project. 

## Testground
This folder holds the list of code that the team has developed, whether failed, a work-in-progress, or completed. 

1. Tapping `Discontinued`<br>An early-stage attempt to visualise the tapping motions. 
2. Ken Yew Testground<br>Ken Yew's test codes.
3. Chin Yang Playground<br>Chin Yang's test codes.
4. Ka Shing_Data Truncation `Discontinued`<br>An attempt to automatically truncate a CSV's data into its constituent signals. Discontinued due to complexity and preference for manual truncation for the purposes of the project.
5. Jing Testground<br>Jing Wei's test codes.
6. Ka Shing_Sensor bluetooth `Discontinued`<br>An attempt to automate bluetooth connectivity to the sensors. Discontinued due to extremely unintuitive and potentially costly API and setup. 
7. Ka Shing_Inertial navigation `Discontinued`<br>An attempt to transform sensor data to the global reference frame. 
8. Ka Shing_Data Analysis `Discontinued`<br>An attempt to run methodical data analysis on acquired data. Discontinued due to redistribution of task responsibilities. 
9. Ka Shing_Web Application `Complete`<br>Proof-of-concept regarding a Create-Read-Update-Delete web app for acquired data.
10. Ken Yew_Feature_Extraction<br>Feature extraction code. 

---

# Notes for the Team
1. We will be removing all non-data files and folders from `Data`. 
2. We will not be including the `Data (Archived)` folder in the final version. 
3. We will not be including `Images` in the final version.
4. As most of our notebooks and code of note are found in `Testground`, we will not be including `Notebooks` in the final version.
5. Can the author of `Pulse Analysis` move it into `Testground` for consistency, unless there's a reason not to? 

---

# Explanations of .gitignore for the Team
1. All `.ipynb_checkpoints` and `__pycache__` folders are ignored.
2. Everything within the `Data (Archived)` folder.
3. `.csv` files are ignored. The exceptions to this are those in `Data` and those used for interactive testing, like the Web App. Let me know if you need any to be included. 
4. `Images`, and all files ending in `.gif`, `.jpg`, and `.png` are ignored.
5. Everything in `Notebooks` is ignored. 
6. Copies of Ken's `resources` folder in Chin Yang's testgrounds are ignored.
7. The old web app folder is ignored.
8. The `Archives` folder is a locally stored folder of a copy of everything previously in the repository. 