from dotenv import load_dotenv
from httpx import get 
import os

load_dotenv()
access_key = os.environ["UNSPLASH_ACCESS_KEY"]

def get_response_for(keyword,results_per_page, page = 1):
    url = f"https://api.unsplash.com/search/photos/?page={page}&per_page={results_per_page}&query={keyword}&client_id={access_key}"
   
    print(access_key)
 
    resp = get(url)
    if resp.status_code == 200:
        return resp.json()
    print(resp.status_code)

def get_img(data):
    results = data["results"]

    imgs_urls = [i["urls"]["full"] for i in results]

    return imgs_urls

def download_images(img_urls, max_download, dest_dir = "images", tag=""):
    successfully_downloaded = 0

    for url in img_urls: 
        if successfully_downloaded < max_download:
            resp = get(url)
            file_name = url.split("/")[-1].split("?")[0]

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(f"{dest_dir}/{tag}{file_name}.jpeg", "wb") as f: 
                f.write(resp.content)
                successfully_downloaded += 1
        else:
            break

    return successfully_downloaded

def scrape(keyword, num_of_results):
    start_page = 1
    success_count = 0

    while success_count < num_of_results:
        data = get_response_for(keyword,results_per_page=20,page=start_page)    
        max_downloads = num_of_results - success_count

        if data: 
            img_urls = get_img(data)
            successfully_downloads = download_images(img_urls, max_downloads, tag = keyword)
            success_count += successfully_downloads
            start_page +=1
        else: 
            print("Error: no data returned")
            break



if __name__ == "__main__":

    scrape("beer", 10)

  

