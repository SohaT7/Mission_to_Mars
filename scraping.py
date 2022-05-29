# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Setting our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data
    
    
    
# ### The Article

def mars_news(browser):
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    ##### Or this: 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    ## In the line above, we are:
    ## Searching for elt.s with a sp. combination of tag (div) and attribute (list_text);
    ## (Eg: 'div.list_text' exists as <div class="list_text"> in HTML)
    ## and, we are telling the browser to wait 1 second before searching for components -
    ## this gives dynmaic pages a little while to load, esp if they are image-heavy.

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        ## NOTE: Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent 
        ## (the other tags within the <div /> element)? This is our parent element. This means that this element holds 
        ## all of the other elements within it, and we'll reference it when we want to filter search results even further. 
        ## The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag 
        ## with the class of list_text. CSS works from right to left, such as returning the last item on the list instead 
        ## of the first. Because of this, when using select_one, the first matching element returned will be a <li /> 
        ## element with a class of slide and all nested elements within it.

        # Scrape the title of the most recent article published
        # slide_elem.find('div', class_='content_title')
        ## This, however, prints the title Along with the extra HTML stuff.
        ## We only require the text.

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        ## This returns only the text of the elt.,
        ## which in our case is the title of the news article. 
        # NOTE: 
        ## .find() is used when we want only the first class and attribute we've specified.
        ## .find_all() is used when we want to retrieve all of the tags and attributes.

        # Scrape the summary text for the most recent article published
        ## Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p
    
    
    
# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    ##### Or this: 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    ## The index [1] stipulates that the second button be clicked (which is our required button).

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        ## An img tag is nested within this HTML, so we've included it.
        ## .get('src') pulls the link to the image.
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    ##### Or this: f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    ## A NOTE on f-strings: 
    ## We're using an f-string for this print statement because it's a cleaner way to create print statements; 
    ## they're also evaluated at run-time. This means that it, and the variable it holds, doesn't exist until the 
    ## code is executed and the values are not constant. This works well for our scraping app because the data 
    ## we're scraping is live and will be updated frequently.

    return img_url



# ### Table of Facts

def mars_facts():
    
    # Add try/except for error handling
    try:
        # Converting HTML-coded table into a DataFrame
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        ##### Or this: 'https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html'
        
    except BaseException:
        return None
        
    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # The above mentioned steps do the following:
    ## 1st line: The Pandas function read_html() specifically searches for and returns a list of tables found in the 
    ## HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first
    ## item in the list. Then, it turns the table into a DataFrame.
    ## 2nd line: Here, we assign columns to the new DataFrame for additional clarity.
    ## 3rd line: By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
    ## inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a 
    ## new variable.

    # Converting the DataFrame we created into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



# Tell Flask that the script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    