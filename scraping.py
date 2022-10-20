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

    # Setting our hemispheres dictionary
    hemisphere_image_urls = hemis(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data
    
    
    
# ### The Article

def mars_news(browser):
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    # Or this: 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page: wait 1 second before searching for components
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Return first matching elt. (last elt. as per CSS) with the <div /> tag and class list_text 
        slide_elem = news_soup.select_one('div.list_text')

        # Scrape the title of the most recent article published: use the parent element to find the first `a` tag
        news_title = slide_elem.find('div', class_='content_title').get_text()
      
        # Scrape the summary for the most recent article: use the parent element to find the paragraph text
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
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    ##### Or this: f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url



# ### Table of Facts

def mars_facts():
    
    # Add try/except for error handling
    try:
        # Converting HTML-coded table into a DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        ##### Or this: 'https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html'
        
    except BaseException:
        return None
        
    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Converting the DataFrame we created into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemis(browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    ## Create an HTML object, assigned to the html variable:
    html = browser.html
    ## Use BeautifulSoup (as soup) to parse the html object:
    hemi_soup = soup(html, 'html.parser')

    try: 
        # Create a list with all relevant elements (4 elements for 4 hemispheres) in it:
        divs = hemi_soup.find_all('div', class_='description')
        for div in divs:
            a = div.find_all('a', class_='itemLink product-item')
            # From each specific element, get the href (to go to a specific hemisphere's own page):
            for ana in a:
                href = ana.get('href')
                
                # Create dictionary:
                hemispheres = {}
                
                # From the specific href, string together a complete URL (to be able to visit the specific hemisphere's own page):
                next_pg_url = url + href
                browser.visit(next_pg_url)

                # Parse the new (a specific hemisphere's) page:    
                html = browser.html
                # Use BeautifulSoup (as soup) to parse the html object:
                sphere_soup = soup(html, 'html.parser')

                # Get the title for that hemisphere:
                title = sphere_soup.find('h2', class_='title').get_text()

                # Get the (complete) image URL for that hemisphere (and visit the full image thereby):
                img_rel_url = sphere_soup.find('img', class_='wide-image').get('src')
                img_url = url + img_rel_url
                browser.visit(img_url)

                # Add the image URL and title to the dictioanry:
                hemispheres['img_url'] = img_url
                hemispheres['title'] = title
                hemisphere_image_urls.append(hemispheres)

    except AttributeError:
        return None

    return hemisphere_image_urls



# Tell Flask that the script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    