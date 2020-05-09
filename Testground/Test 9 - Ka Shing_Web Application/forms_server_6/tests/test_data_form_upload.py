# === Import ===
import time 
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# === Get test cases ===
test_cases_directory = '\\'.join([os.getcwd(), 'csv_files'])
test_cases = os.listdir(test_cases_directory)

# === Boot up webdriver ===
options = Options()
# options.add_argument('--headless')
options.add_argument("--window-size=960,1080")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)

driver.get('http://127.0.0.1:5000/')

# === Test ===
# --- Test for the notifications based on the 7 test cases ---
upload_test = driver.find_element_by_id("files")

uploads = []
for f in test_cases:
    uploads.append('/'.join([test_cases_directory, f]))
uploads = ' \n '.join(uploads)

#     # print(uploads)
#         # upload_test.send_keys('/'.join([test_dir, f]))
upload_test.send_keys(uploads)
upload_test.submit()

time.sleep(1)
    
# --- Test for data request form submission --- 
submit_form = driver.find_element_by_id("submit-parameter-request-form")
submit_form.submit()

# === Close testing ===
# For debugging this script
# time.sleep(4)

# driver.quit()