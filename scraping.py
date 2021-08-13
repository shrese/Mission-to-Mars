# import splinter, beautiful soup, and other dependencies
from os import name
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# for jupyter only
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

# set up splinter & initiate headless driver for deployment
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in a dictionary
    data = { 
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        "last_motified": dt.datetime.now()
    }

    #stop webdriver and return data
    browser.quit()

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
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the parser/Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find the paragraph text
        news_p = slide_elem.fid('div', class_='article_teaswer_body').get_text()
        
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
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('scr')

    except AttributeError:
        return None    

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

if __name__ == '__main__':
    #if running as script, print scraped data
    print(scrape_all())

browser.quit()