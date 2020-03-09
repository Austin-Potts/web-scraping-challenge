from bs4 import BeautifulSoup as bs 
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    return Browser("firefox", executable_path = "/Users/Austin Potts/Downloads/geckodriver", headless=True)

def scrape():
    browser = init_browser()


    #############################################################################################################################################################
    #working
    #Grab title and paragraph from the first post on the mars news page
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Make a GET request to fetch the raw HTML content
    news_html_content = requests.get(news_url).text

    # Parse the html content & print the parsed data of html
    soup = bs(news_html_content, "lxml")

    #using beautiful soup to grab the first title of the content on the news page
    articles = soup.find("div", attrs={"class": "content_title"})
    news_title = articles.find_all("a")
    news_title = news_title[0].text.strip()

    #grabbing the intro paragraph associated with the title
    body_text = soup.find("div", attrs={"class":"rollover_description_inner"})
    news_p = body_text.text.replace("\n","").strip()
    print(f"Title: {news_title} \n Body: {news_p}")

###################################################################################################################################################
    #working
    #creates a browser controlled by splinter which doesnt open because headless is true
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    
    #clicks the link we need from the page to pull the image from
    target = '#full_image'
    browser.find_by_css(target).click()

    #clicking more info button to get path to full jpeg
    target_2 = '#fancybox-lock > div > div.fancybox-title.fancybox-title-outside-wrap > div > div.buttons > a.button'
    browser.find_by_css(target_2).click()

    #parses the pages html and allows us to use beautiful soup, the image we need is help in the figure with class lede
    html = browser.html
    soup = bs(html, 'lxml')
    featured_image_url = soup.find('figure', class_='lede').a['href']

    #places the specific image tag into the url string to make the link
    featured_image_url = (f"https://www.jpl.nasa.gov{featured_image_url}")

    #closes the browser after grabbing the necessary image url we need
    browser.quit()

    #printing image to make sure this works
    print(featured_image_url)

#######################################################################################################################################################
    #working
    #url to twitter page for mars weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    tweet_html_content = requests.get(tweet_url).text
    soup = bs(tweet_html_content, "lxml")

    #<div class="js-tweet-text-container"> --> <p> has tweet body
    #list of tweets on page
    tweet_list = soup.find_all('div', class_="js-tweet-text-container")

    #empty list to hold tweet we are going to keep, used to strip useless content from string
    holds_tweet = []

    # Loop that scans every tweet and searches specifically for those that have weather info
    for tweets in tweet_list: 
        tweet_body = tweets.find('p').text
        if 'InSight' and 'sol' in tweet_body:
            holds_tweet.append(tweet_body)
            #break statement to only print the first weather tweet found
            break
        else: 
            #if not weather related skip it and try again
            pass
        
    #cleaned up tweet removes unncessary link to twitter image included in string, :-26 removes the last 26 characters which is the length of the img url
    #after reviewing several links they all appear to work with the value of -26
    mars_weather = ([holds_tweet[0]][0][:-26])
    tweet_img_link = ([holds_tweet[0]][0][-26:])
    print(f"{mars_weather}: {tweet_img_link}")

    ######################################################################################################################################################
    # Website that the mars facts table will be pulled from in the front end application
    facts_url = "https://space-facts.com/mars/"

    # Use Pandas to scrape the tables found in the url, the first table is the one we need
    raw_table_data = pd.read_html(facts_url)
    mars_facts = raw_table_data[0]

    # Add names to the columns so they are not 0 and 1
    mars_facts.columns = ['Description','Value']

    # Reset Index to be description so that the table reads in correctly and makes sense
    mars_facts.set_index('Description', inplace=True)
    
    #exporting table data to html for use in the flask app.
    mars_facts = mars_facts.to_html(classes="table table-striped")

    ###################################################################################################################################
    browser = Browser("firefox", executable_path = "/Users/Austin Potts/Downloads/geckodriver", headless=True)
    images_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(images_url)
    soup = bs(browser.html, 'lxml')

    #create empty lists which will be appended by the for loop
    titles = []
    image_urls = []

    #finding div that holds all 4 images and then isolating the images
    items = soup.find_all('div', class_ = 'item')
                    
    #for loop that grabs the title and images url from the html elemnts in 'items'    
    for i in items:
        #grabbing the title from the heading 3 and removing "enhanced" from the string
        title = i.find('h3').text
        title = title.replace("Enhanced", "")
        titles.append(title)
        #finding the url to the specific images that we need and then opening a new broswer to those links to get the url for the img
        finish_line = i.find('a')['href']
        #finish_line = /search/map/Mars/Viking/cerberus_enhanced, website url is https://astrogeology.usgs.gov
        new_link = f'https://astrogeology.usgs.gov{finish_line}'
        #re-initiang browser because we moved to a new page that has to be parsed for its html
        browser.visit(new_link)
        soup = bs(browser.html, 'lxml')
        #finding the image div and copying the href from it, and adding to the list image_urls
        pic = soup.find('div', class_='downloads')
        image_url = pic.find('a')['href']
        image_urls.append(image_url)

    browser.quit()
    #Creates the final list of dictionaries by zipping together the 2 lists that were appended in the for loop.
    hemisphere_image_urls = []
    for title, url in zip(titles, image_urls):
        hemisphere_image_urls.append({"title": title, "img_url": url})
    print(hemisphere_image_urls)
    ########################################################################################################################################
    # Store data in a dictionary
    mars_data = {"news_title": news_title, "news_p": news_p, "featured_image_url": featured_image_url, "mars_weather": mars_weather, "mars_facts": mars_facts, "hemisphere_image_urls": hemisphere_image_urls}
    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()