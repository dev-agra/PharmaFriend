from Screenshot import Screenshot
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')

# op.add_argument = {'user-data-dir': r"C:\Users\Devansh\AppData\Local\Google\Chrome\User Data\Profile 5"}

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

driver.maximize_window()

ob = Screenshot.Screenshot()
url = "https://nesoacademy.org/"
driver.get(url)

time.sleep(10)

# click login button
driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div/div[6]/div[3]/button/span[1]").click()

# login
time.sleep(10)

loginuser = driver.find_element(By.XPATH, '//*[@id="loginEmail"]')
loginuser.send_keys("agraradev2218@gmail.com")

loginpass = driver.find_element(By.CSS_SELECTOR, '.MuiInputBase-inputAdornedEnd')
loginpass.send_keys("IknowDevansh@2822")

time.sleep(4)
driver.find_element(By.CSS_SELECTOR, 'button.MuiButton-contained:nth-child(2) > span:nth-child(1)').click()

time.sleep(5)
driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div[6]/a/div/div[1]").click()

time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section[2]/section/div[2]/header/div/div/div/button[3]/span[1]').click()

time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section[2]/section/div[2]/div[3]/section/section/div/a[1]/section/div[1]/div[2]/p').click()
time.sleep(3)

#obtain window handle of browser in focus
p = driver.current_window_handle
print(p)

#obtain parent window handle
parent = driver.window_handles[0]

#obtain browser tab window
child = driver.window_handles[1]

#switch to browser tab
driver.switch_to.window(child)
time.sleep(25)

original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
# driver.set_window_size(required_width, required_height)
driver.set_window_size(required_width, min(6000, required_height))
# driver.save_screenshot(path)  # has scrollbar
driver.find_element(By.CLASS_NAME, 'outer-container').screenshot('CN_Network_IMG/PPT.png')
driver.set_window_size(original_size['width'], original_size['height'])


driver.close()
driver.quit()
