from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import pandas as pd

# Automatically install or update ChromeDriver
chromedriver_autoinstaller.install()

# Setup Chrome WebDriver with options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for performance
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Open the target webpage
url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement?company=0193"
driver.get(url)

# Wait to ensure the page fully loads
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-announcements tbody tr")))

# Data storage
data = []

try:
    while True:
        # Locate table rows inside tbody for extraction
        table_rows = driver.find_elements(By.CSS_SELECTOR, "#table-announcements tbody tr")

        # Iterate over rows to capture structured data
        for row in table_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                try:
                    # Extract the date, company name, and links
                    announcement_date = cells[1].find_element(By.CSS_SELECTOR, "div.d-lg-inline-block.d-none").text.strip()
                    company_name = cells[2].text.strip()
                    company_link = cells[2].find_element(By.TAG_NAME, "a").get_attribute("href")
                    announcement_title = cells[3].text.strip()
                    title_link = cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    data.append({
                        "Announcement Date": announcement_date,
                        "Company Name": company_name,
                        "Company Link": company_link,
                        "Announcement Title": announcement_title,
                        "Title Link": title_link,
                    })
                except Exception as e:
                    print(f"Error processing row: {e}")

        # Handle pagination
        try:
            # Locate and click the next button if not disabled
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.paginate_button.next')
            if 'disabled' in next_button.get_attribute('class'):
                print("Reached the last page.")
                break

            # Scroll the next button into view and click it
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the page to load
            time.sleep(2)  # Small delay to avoid overwhelming the server
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-announcements tbody tr")))

        except Exception as e:
            print(f"Pagination error: {e}")
            break

finally:
    # Close the browser
    driver.quit()

# Save to CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv("bursa_announcements.csv", index=False)
    print(f"Successfully scraped {len(data)} announcements.")
else:
    print("No announcements found.")
	
	
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import pandas as pd

# Automatically install or update ChromeDriver
chromedriver_autoinstaller.install()

# Setup Chrome WebDriver with options
options = webdriver.ChromeOptions()
# Removed --headless to allow the browser to open
# options.add_argument("--headless")  # Run in headless mode for performance (removed this line)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Read stock codes from CSV
try:
    stock_codes = pd.read_csv('stock_codes.csv')['Stock Code'].tolist()
except Exception as e:
    print(f"Error reading stock codes CSV: {e}")
    stock_codes = []

# Data storage
data = []

for stock_code in stock_codes:
    try:
        # Open the target webpage for current stock code
        url = f"https://www.bursamalaysia.com/market_information/announcements/company_announcement?company={stock_code}"
        driver.get(url)

        # Wait for the page to load completely by waiting for a specific element (the table rows)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-announcements tbody tr")))
        
        # Add a small wait to ensure the page fully loads after opening the URL
        time.sleep(2)  # Wait for 2 seconds (adjust as needed)

        # Process pagination for current stock code
        while True:
            # Locate table rows inside tbody for extraction
            table_rows = driver.find_elements(By.CSS_SELECTOR, "#table-announcements tbody tr")

            # Iterate over rows to capture structured data
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    try:
                        # Extract the date, company name, and links
                        announcement_date = cells[1].find_element(By.CSS_SELECTOR, "div.d-lg-none").text.strip()
                        company_name = cells[2].text.strip()
                        company_link = cells[2].find_element(By.TAG_NAME, "a").get_attribute("href")
                        announcement_title = cells[3].text.strip()
                        title_link = cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        data.append({
                            "Announcement Date": announcement_date,
                            "Company Name": company_name,
                            "Company Link": company_link,
                            "Announcement Title/Announcement Category": announcement_title,
                            "Title Link": title_link,
                        })
                        print("Announcement Date:", announcement_date,
                            "Company Name:", company_name,
                            "Company Link:", company_link,
                            "Announcement Title/Announcement Category:", announcement_title,
                            "Title Link:", title_link)
                    except Exception as e:
                        print(f"Error processing row for {stock_code}: {e}")

            # Handle pagination
            try:
                # Locate and click the next button if not disabled
                next_button = driver.find_element(By.CSS_SELECTOR, 'li.paginate_button.next')
                if 'disabled' in next_button.get_attribute('class'):
                    print(f"Reached the last page for stock code {stock_code}.")
                    break

                # Scroll the next button into view and click it
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)

                # Wait for the page to load
                time.sleep(2)  # Small delay to avoid overwhelming the server
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-announcements tbody tr")))

            except Exception as e:
                print(f"Pagination error for stock code {stock_code}: {e}")
                break

    except Exception as e:
        print(f"Error processing stock code {stock_code}: {e}")
        continue  # Continue with next stock code

# Close the browser after all stock codes are processed
driver.quit()

# Save to Excel with renamed column
if data:
    df = pd.DataFrame(data)
    df.to_excel("bursa_announcements.xlsx", index=False, engine='openpyxl')
    print(f"Successfully scraped {len(data)} announcements.")
else:
    print("No announcements found.")