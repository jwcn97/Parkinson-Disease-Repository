# Distinguishing Severity in Parkinson Disease

## About
This documentation on Chin Yang's Playground will guide you through the use of each folder and file. It shall also display benchmarks required to be achieved and their progress.

## Folder Breakdown
### Motion Data, Motion Data2 & Motion Data3

----
The folders containing data simulated for training, test and validation.

### PD_redo & PD_test

----
These two folders will have self-simulated data. This is to achieve the following:
- [X] Check for upper limit of clipping effect in gyroscope data. # It was found to be at approx. 500 deg/s
- [X] Check on the need for reorientation of data
- [X] Check using activation of sensors that measures linear acceleration, pressure, temperature, quaternion and euler angles.

### Sara_Experiment

----
The folders contain simple motion test data where video recording has been taken and stored in Google Drive

### Parkinsonian Analysis

----
This file comprises of all the code used for analyses that has been done up to date. It will also include some comments to explain the methodology of the code and its relevance to the data retrieved. Certain form of testing works are carried out to validate the functions' output.

#### - Importing Libraries

----
- [X] Implementation of itertool: combinations
- [ ] Implementation of scipy.signal: find_peaks and peak prominences
- [X] Fixed mpld3 to allow plugins and widgets to work for scatter plots and colorbars
- [ ] Fixed tqdm to display running time of code

#### - Directory Check

----
- [X] Navigates successfully to different data folders or specific .csv files from current working directory

#### - Configuration Testing

----
- [ ] Check that every data set has adhere to the nomenclature accurately

#### - Orientation Testing

----
- [X] Comparison on results dominantly using linear acceleration, quaternion and euler angles.
- [X] Testing difference in accelerometer and gyroscope results with deployment of sensors on front and back of wrist

#### - Retrieving Raw Data

----
- [X] Displays raw motion data from designated folder path correctly

#### - Truncating Data

----
- [X] Functionality of manual truncation with exhaustive elsif statements
- [ ] Automatic truncation with key features analysed from time series waveforms. #Still undergoing testing

#### - Time Series Data

----
- [X] Plots truncated accelerometer and gyroscope data succesfully

#### - Time-domain Statistics

----
####  _Descriptive Statistics_
- [ ] Central Tendency Measures
    - [X] Arithmetic Mean
    - [ ] Median 
    - [ ] Mode
- [ ] Variability/Spread Measures
    - [ ] Standard Deviation
    - [ ] Interquartile Range
    - [ ] Covariance
- [ ] Shape Measures # Have not looked into this
- [ ] Positional Measures
    - [ ] Percentile # Have not looked into this
- [ ] Impurity Measures
    - [ ] Entropy # Have not looked into this
#### _Inferential Statistics_
- [X] Zero-crossing rate
- [X] Mean-crossing rate # Find explanation on this
- [X] Pearson's correlation coefficient
- [ ] Spearman's correlation coefficient #for non-gaussian distribution

#### _Exploratory Data Analysis_
#Done by Jing
- [ ] Count of dominant peaks and troughs 
- [ ] Count of subsidiary peaks and troughs
- [ ] Height and width of dominant peaks and troughs 
- [ ] Height and width of subsidiary peaks and troughs

#### - Frequency Spectrum

----
- [X] Fast Fourier Transform
- [ ] Frequency Analysis
    - [ ] Amplitude vs Frequency
    - [ ] Energy Spectral Density vs Frequency
    - [ ] Power vs Frequency
    - [ ] Power Spectral Density vs Frequency

#### - Frequency-domain Statistics

----
#### _Descriptive Statistics_
#Done by Ken
- [ ] Central Tendency Measures
    - [X] Arithmetic Mean
    - [ ] Median 
    - [ ] Mode
- [ ] Variability Measures
    - [X] Standard Deviation
    - [ ] Interquartile Range 
- [ ] Shape Measures 
    - [ ] Skewness
    - [ ] Kurtosis 
- [ ] Positional Measures
    - [ ] Percentile
- [ ] Impurity Measures
    - [ ] Entropy #Have not looked into this

#### _Exploratory Data Analysis_
- [ ] Spectrogram. #A 3D measure the change in frequency along with its intensity with variation of time. Though, a mismatch in values with colorbar is still a concern here.

#### - Feature Selection

----
This section of the code will serve as evaluation purposes for all the statistics or indicators used for classification. The features will then be tentatively ranked according to the metric of evaluations.
- [ ] Accuracy.  #The accuracy achieved will be representative of the uni-directional trend shown across severity levels.
    - [ ] Gini impurity # To be reconsidered. This is the measure for the misclassification data set, based on the features finalised for classification.
- [ ] Distinguishability. #Measure the extent of significance of the feature, across severity levels. Metrics for this could be absolute difference or ratio.
- [ ] Precision. #This will be use to measure the consistency of the features' accuracy and distinguishability, across data sets.

#### - Smoothen Data

----
- [ ] Filter works. #Check with Ken

#### - Noise

----
- [ ] Background noise check for sensors. #Still need checks
- [ ] 

#### - Archive

----
- [] Notes prior for data pre-processing
    - [] Error checks
    - [] Identifying patterns and observations
    - [] Insights for automatic truncation
    - [] Additional notes for feature extraction
- [] Manual truncation timestamps for new data sets
- [] Cross check on 
- [] Debugging issues in frequency domain


### Insights on Experiment & Insights on Motion Tests

Draft record of some observations made in a textfile.

### Jing_Test1

Reference ipynb file for time domain analysis

### CY_Testing

Older version of ipynb file for truncation purposes and time domain analysis

### Ken_Test1

Older version of ipynb file for truncation purposes, frequency domain analysis and display of some descriptive statistics

### Archive

Folder for files that are now considered redundant or irrelevant