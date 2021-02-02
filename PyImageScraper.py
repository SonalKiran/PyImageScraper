# imports
from selenium import webdriver
import time, requests
import pandas as pd
import os
import concurrent.futures
import base64
import ast
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

# function to fetch urls
def fetch_url(search_query, url_count = 20):
    browser = webdriver.Chrome()
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # open browser and begin search
    browser.get(search_url)
    try:
        elements = browser.find_elements_by_class_name('rg_i')
    except TimeoutException:
        print("Loading took too much time!")

    count = 0
    for e in elements:
        # fetch image urls
        try:
            e.click()
            time.sleep(1.5)
            element = browser.find_elements_by_class_name('v4dQwb')
            # Google Chrome logic
            if count == 0:
                big_img = element[0].find_element_by_class_name('n3VNCb')
                count += 1
            else:
                big_img = element[1].find_element_by_class_name('n3VNCb')
                count += 1
            images_url.append(big_img.get_attribute("src"))
        except WebDriverException as e:
            print(f"Web Driver Exception Occurred: {e.__str__()}")
            continue

        # save urls for the given search query in a dictionary
        if len(images_url) == url_count:
            global master_urls
            master_urls[search_query] = images_url
            browser.quit()
            break

# function to fetch images
def fetch_img(sess, url, filename):
    if 'base64' in url:
        try:
            b64 = url[url.index('base64')+6:]
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(b64))
        except Exception as e:
            print(f"Base64 to Image - Exception Occurred: {e.__str__()}")
    else:
        try:
            r = sess.get(url, stream = True, timeout=3)
            if r.status_code == 200:
                # Open a local file with wb ( write binary ) permission.
                with open(filename, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                print(f'Image successfully downloaded: {filename}')
            else:
                print(f'Unable to downloaded image: {filename}')
        except Exception as e:
            print(f"Exception Occurred: {e.__str__()}")

# retrieve master_urls dict from keyword_urls.txt
# with open('./keyword_urls.txt', 'r') as file:
#     new_dict = file.read()
# master_urls = ast.literal_eval(new_dict)

# define the path of csv containing keywords
csv_path = './queries.csv'

# set destination directory to store images
dest_dir = './images'

# initialize dict
master_urls = {}

def main():
    # load search queries from csv
    data = pd.read_csv(csv_path, header=None)
    data.columns = ["Query"]

    # save queries to a list
    keywords = [data["Query"][i] for i in range(len(data))]

    # fetch urls using multithreading and save to master_urls dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
        future = [exec.submit(fetch_url, search_query=val, url_count=10) for
                  val in keywords]

    #  ensure dest_dir exists
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # save master_urls in text file for future reference
    with open(os.path.join(dest_dir,'keyword_urls.txt'), 'w') as file:
        file.write(str(master_urls))

    for key, values in master_urls.items():
        # create directory for every keyword for which image is to be downloaded
        if not os.path.exists(os.path.join(dest_dir, key)):
            os.mkdir(os.path.join(dest_dir, key))
        # download images
        with requests.Session() as sess:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
                future = [exec.submit(fetch_img, sess=sess, url=val, filename=os.path.join(dest_dir, key, str(i) + '.jpg')) for i, val in enumerate(
                    values)]

main()