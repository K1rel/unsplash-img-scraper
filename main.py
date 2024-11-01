from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests 
import os

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

        return [srcset.split(", ")[-1].split(" ")[0]] if filter_imgs(srcset.split(", ")[-1], ['plus', 'profile', 'premium']) else None

        
       



def save_imgs(img_urls, dest_dir="images", tag=""):
    for url in img_urls: 
        response = requests.get(url)
        file_name = url.split("?")[0].split("/")[-1]
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)


        with open(f"{dest_dir}/{tag}{file_name}.jpeg","wb") as f:
            f.write(response.content)
        
   


if __name__ == "__main__":
   
    result = get_img_tags_for("ski mountains")
    high_res_images = []

    imgs, driver = result["img_nodes"], result["driver"]

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
    
    high_res_images = [url for sublist in high_res_images for url in sublist]
    
    save_imgs(high_res_images)
    driver.quit()

 
