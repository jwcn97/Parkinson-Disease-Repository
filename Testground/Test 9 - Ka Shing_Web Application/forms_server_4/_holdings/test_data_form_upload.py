# === Import ===
import time 
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# === Get test cases ===
test_cases_directory = '/'.join([os.getcwd(), 'upload_test_cases'])
test_cases_directory = [
    '/'.join([test_cases_directory, t]) for t in list(filter(lambda x: '.' not in x, os.listdir(test_cases_directory)))
]

# Select only Case 7
test_cases_directory = list(filter(lambda x: "7" in x, test_cases_directory))
test_cases_directory = {t: os.listdir(t) for t in test_cases_directory}

# === Boot up webdriver ===
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)

driver.get('http://127.0.0.1:5000/')

# === Test ===
# --- Test for the notifications based on the 7 test cases ---
for test_dir, test_file in test_cases_directory.items():
    upload_test = driver.find_element_by_id("files")

    uploads = []
    for f in test_file:
        uploads.append('/'.join([test_dir, f]))
    uploads = ' \n '.join(uploads)

    # print(uploads)
        # upload_test.send_keys('/'.join([test_dir, f]))
    upload_test.send_keys(uploads)
    upload_test.submit()

    time.sleep(1)
    
# # --- Test for data request form submission --- 
submit_form = driver.find_element_by_id("submit-data-request-form")
submit_form.submit()

# === Close testing ===
# For debugging this script
time.sleep(2)

driver.quit()