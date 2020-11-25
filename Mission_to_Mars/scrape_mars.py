#Import Dependencies
import pymongo
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import re
from pandas import DataFrame
import pandas as pd


def scrape():
    # connect to mongo
    mars_data ={}
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    #Web Path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #set url
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    news_title = soup.find( class_='content_title').text
    mars_data.update({'news_title': news_title})
    #print(news_title)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    news_p = soup2.find( class_='article_teaser_body').text
    #print(news_p)
    mars_data.update({'news_p': news_p})

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    # https://stackoverflow.com/questions/37843903/getting-style-of-tr-tag-using-beautifulsoup
    link = soup2.find('article')#['style']
    #print(link)
    link = soup2.find('footer')
    #print(link)

    something = link.find('a')['data-fancybox-href']

    url = soup2.find( class_='jpl_logo')
    url = url.find('a')['href']
    #print(url)
    featured_image_url = 'https:' + str(url) + str(something)
    #print(featured_image_url)
    mars_data.update({'featured_image_url': featured_image_url})

    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    table = pd.read_html('https://space-facts.com/mars/')
    #print(table)
    df= DataFrame(table[0])
    df = df.to_html()
    mars_data.update({'table': df})

    url_hem1 ='https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    url_hem2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    url_hem3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    url_hem4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    urls = [url_hem1, url_hem2 , url_hem3, url_hem4]
  
    img_images = []
    
    
    for earl in urls:
        browser.visit(earl)
        html4 = browser.html
        soup4 = BeautifulSoup(html4, 'html.parser')
        url  = soup4.find( 'li')
        img_url = url.find('a')['href']
       
        titles = soup4.find(class_ = 'title').text
        
        #print(link)
        img_images.append({"title": titles,
        "img_url": img_url})
        
        
    browser.quit()

    # Return results
    mars_data['img_images']=img_images
    return mars_data
        

