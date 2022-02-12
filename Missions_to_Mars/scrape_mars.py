#################################################
# Import/ call dependencies and Setup
#################################################
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import json

#################################################
# Visit the page by browser and scrape data for the latest news
#################################################
def news(browser):

    # Set url and browser visit the site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html

    # Convert the browser html to a soup object
    news_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        print(news_soup.title.text)
        page_element = news_soup.find('div', class_='list_text')

        # Use the parent element to find the first tag and save it as `contents_title`
        news_1st_title = page_element.find(class_='content_title').text

        print(news_1st_title)

        # Use the parent element to find the paragraph text
        news_1st_par = page_element.find(class_="article_teaser_body").text
        print(news_1st_par)
    
    except AttributeError:
        return None, None
    
    return news_1st_title, news_1st_par
#################################################


#################################################
# Visit the page by browser and scrape the link of the featured image of the day
#################################################
def featured_image(browser):

    # Set url and browser visit the site
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    img_html = browser.html

    # Convert the browser html to a soup object
    img_soup = bs(img_html, 'html.parser')

    # Add try/except for error handling
    try:
        # Navigate to the image's file name
        image_1st = img_soup.find('img',class_='headerimage').get('src')
        print(img_soup.title.text)

        # Capture URL for the featured image
        featured_image_url = img_url + image_1st

        print(featured_image_url)
    
    except AttributeError:
        return None, None
    
    return featured_image_url
#################################################

#################################################
# Visit the page by browser and scrape data for mars_facts
#################################################
def mars_facts():

    # Add try/except for error handling
    try:
        # Using pandas to capture the data of the second table on the page with index [0] (i.e. comaprison bertween mars and earth) 
        mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]

        # Work on pandas dataframe, rename columns, set index column, remove index column name and 
        # drop the first row of dataframe that contains duplicated columns names
        mars_df.columns = ["Description","Mars", "Earth"]
        mars_df.set_index('Description', inplace=True)
        mars_df.drop(index=mars_df.index[0], axis=0, inplace=True)
        mars_df.index.name = None

        # Print Mars Facts to terminal
        print(f"Mars Facts")

        # Convert pandas dataframe into html string and save to output folder
        mars_df.to_html("templates/mars_facts.html")
    
    except AttributeError:
        return None, None
    
    # Set styling attributes for mars_facts table html
    table_style = '<table style="background-color:#66ccff;" class="table table-hover table-bordered";>'
    th_style = '<th style="color:black; text-align: left; font-size:15px; padding: 5px;">'
    td_style = '<td style="color:#2F4F4F; text-align: left; font-size:15px; padding: 5px;">'

    # Convert pandas dataframe to html file, replace all the default tags with styling tags
    mars_facts = str(mars_df.to_html()).replace('<table border="1" class="dataframe">', table_style).replace('<td>', td_style).replace('<th>', th_style)

    return mars_facts

#################################################

#################################################
# Visit the page by browser and scrape data links for the full size image of the hemispheres
#################################################
def hemispheres(browser):

    # Set url and browser visit the site
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemispheres_html = browser.html

    # Convert the browser html to a soup object
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    # Add try/except for error handling
    try:
        # Initialise a new list to hold the hemisphere titles and images
        hemisphere_image_urls = []

        # Look into all divs elements of item class
        items = hemispheres_soup.find_all('div', class_='item')

        # Loop through all sub elements under 'div' class 'item', to capture the title & image url as a pair of dictionary.
        # First visit the page (i.e. 1s layer), then navigate to find the link of the image that leads to the next page (i.e. 2nd layer).
        # On 2nd page/ layer, navigate to the full size image's name and title, capture them as a pair of dictionary and append to the list.
        # Returns back to the 1st page/layer to work on the next item on the page. 
        # Keep repeating until no more items to be read on 1st page/layer.

        for i in items:
            
            # Initliase the dictionary
            hem_dict = {}
            
            # Navigate to find the full size image url, through the intermediate link (i.e. 1st layer for user to click button)
            img_title = i.find('h3').text
            link_ref = i.find('a', class_='itemLink')['href']
            
            # Create a URL and browser visit (i.e. browser opens 2nd layer, after user's clicked page)
            browser.visit(url + link_ref)
            
            # Parse the data
            image_html = browser.html
            image_soup = bs(image_html, 'html.parser')
            
            # Navigate to find the image in the element div with downloads class
            download = image_soup.find('div', class_= 'downloads')
            
            # Capture the full size image url
            img_url = url + download.find('a')['href']
            
            # Display on screen the titles and image url
            print(img_title)
            print(img_url)
            
            # Append the dictionary to the himisphere image url list
            hem_dict['title'] = img_title
            hem_dict['img_url'] = img_url
            hemisphere_image_urls.append(hem_dict)
            
            # Go back to the previous page (i.e. 1st page/layer to work on the next item on the page)
            browser.back()

        print(hemisphere_image_urls)
    
        # Save the image url list to json file
        with open('output/image_url.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(hemisphere_image_urls,ensure_ascii=False,indent=1))

    except AttributeError:
        return None, None
    
    return hemisphere_image_urls
#################################################


#################################################
# Perform all scrapping functions and store the data into a dictionary to be loaded on MongoDB
#################################################
def scrape():
   
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = news(browser)

    # Run all the scraping functions and store results in the dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Close the browser after finished scraping
    browser.quit()
    return data

