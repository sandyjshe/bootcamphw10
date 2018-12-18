#Imports & Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

#define chrome executable path
executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)



# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News

def marsNews():
    url_news  = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_news = [news_title, news_p]
    return mars_news


# # JPL Mars Space Images - Featured Image
def marsImage():
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)

    html = browser.html
    soup = bs(html, "html.parser")

    image_url = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    return featured_image_url


# # Mars Weather
def marsWeather():
    
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather

# # Mars Facts
def marsFacts():
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    data_html = pd.read_html(url_facts)
    data_facts = pd.DataFrame(data_html[0])
    mars_facts = data_facts.to_html(header = False, index = False)

    
    return mars_facts


# # Mars Hemispheres
def marsHem():
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)

    html = browser.html
    soup = bs(html, "html.parser")
    

    results_hem = soup.find("div", class_ = "result-list" )
    items_hem = results_hem.find_all("div", class_="item")

    mars_hemisphere = []

    for item in items_hem:
        title = item.find("h3").text
        href_link = item.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + href_link    
        browser.visit(image_link)
        html_item = browser.html
        soup_item=bs(html_item, "html.parser")
        downloads = soup_item.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere
