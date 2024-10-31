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

       
        return {"img_urls": img_urls, "img_nodes": imgs, "driver": driver}

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit() 

def filter_imgs(url: str, keywords: list) -> bool:
    return not any(x in url for x in keywords)

def get_high_res(img_node):
    srcset = img_node.get_attribute("srcset")
    if srcset:
        return [i.split(" ") for i in srcset.split(", ") if filter_imgs(i,['plus', 'profile', 'premium'])]



if __name__ == "__main__":
   
    result = get_img_tags_for("ski mountains")
    high_res_images = []

   
    imgs, driver = result["img_nodes"], result["driver"]

    print("nodes:")
    for i, img_node in enumerate(imgs):
        if img_node is None:
            print(f"Image node {i} is None.")
            continue
        try:
            urls = get_high_res(img_node)
            if urls: 
                high_res_images.append(urls)
        except Exception as e:
            print(f"Error processing img_node {i}: {e}")

    highest_res_images = [urls[-1][0] for urls in high_res_images if urls]
    [print(f"{i}: {imgs}") for i, imgs in enumerate(highest_res_images)]
    driver.quit()

 
