from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_img_tags_for(term=None):
    if term is None:
        raise ValueError("Term needs to be specified")

    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

   
    service = Service(r'C:\Program Files\Google\chromedriver-win64\chromedriver.exe')  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"https://unsplash.com/s/photos/{term}"
        driver.get(url)

       
        time.sleep(3)

       
        imgs = driver.find_elements(By.CSS_SELECTOR, "figure img")

      
        img_urls = [img.get_attribute("src") for img in imgs if img.get_attribute("src")]
        return img_urls

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  

def img_filter(url : str, keywords: list) -> bool:
    return not any(x in url for x in keywords)



if __name__ == "__main__":
    imgs = get_img_tags_for("python")
  
    relevant_imgs = [i for i in imgs if img_filter(i, ["profile", "plus", "premium"])]
    [print(i) for i in imgs]
 
