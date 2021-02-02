# PyImageScraper

### About
This script helps you download images from Google Chrome for a set of keywords pre-defined in a csv file.

### Pre-requisites
1. MacOS Catalina (tested on this OS version, probably will work on others as well)
2. Python 3
3. Chrome driver 
```brew install chromedriver```

### How To Use
1. Make sure pre-requisites are installed.
2. Populate keywords for which images are to be downloaded in 'queries.csv', each keyword in a new row.
3. Either keep 'queries.csv' in the root folder or change 'csv_path' in the script.
4. Define the number of urls to fetch per search query by updating 'url_count' in the main function. Please note that the number of images
 downloaded will be less than or equal to 'url_count'.
3. run ```python PyImageScraper.py``` 
4. All images will be stored in the 'images' folder inside the root folder.
5. The dictionary containing keyword-url pairs will be stored as 'keyword_urls.txt' in the 'images' folder inside the root folder.
