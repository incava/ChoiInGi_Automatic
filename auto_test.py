from selenium import webdriver

# Start a new instance of the Firefox driver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

# Navigate to the Google homepage
driver.get("https://www.google.com")

# Find the search box element and enter a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium with Python")
search_box.send_keys(Keys.ENTER)

# Close the browser window
# driver.quit()
