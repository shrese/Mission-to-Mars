# import splinter, beautiful soup, and other dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
from os import name

def generatebrowser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)
    return browser

# set up splinter & initiate headless driver for deployment
def scrape_all():
    browser = generatebrowser()
    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemi_image(browser) 
    }
# Deliverable 2 #2 - In the def scrape_all() function in your scraping.py file, create a new dictionary in the data dictionary 
        # to hold a list of dictionaries with the URL string and title of each hemisphere image.
    
    # Stop webdriver and return data
    browser.quit()
    return data

#######################################################################################
# LOCATE THE TITLE
#######################################################################################
# define function so it can be called
def mars_news(browser):    
    # scrape mars news
    # visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    # set up the parser/Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

######################################################################################
#LOCATE THE IMAGE
######################################################################################
#define function so it can be called
def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')   
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url
    

######################################################################################
#LOCATE THE FUN FACTS
######################################################################################
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-stripped")

    #if running as script, print scraped data
    # print(scrape_all())


###############################
# Start of Challenge
###############################

###################################################################################
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres
###################################################################################

# 1. Use browser to visit the URL 
# Deliverable 2 - #3 create a function that will scrape the hemisphere data by using your code from the 
              #   Mission_to_Mars_Challenge.py file. At the end of the function, return the scraped data as a list of 
              #   dictionaries with the URL string and title of each hemisphere image.

def hemi_image(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []  

# 3. Write code to retrieve the image urls and titles for each hemisphere.   
    try:
        for i in range(4):
            hemisphere = {}
            browser.find_by_css('a.product-item h3')[i].click()
            element = browser.find_link_by_text('Sample').first
            img_url = element['href']
            title = browser.find_by_css("h2.title").text
            hemisphere["img_url"] = img_url
            ##hemisphere["title"] = title
            hemisphere_image_urls.append(hemisphere)
            browser.back()
    except AttributeError:
        return None

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls