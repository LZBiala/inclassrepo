from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import requests

def init_browser():
        executable_path = {"executable_path": "C:/chromedrv/chromedriver.exe"}
        return Browser("chrome", **executable_path, headless= False)

def scrape():
        browser = init_browser()
        mars_info = {}
        mars_url = "https://mars.nasa.gov/news/"

        browser.visit(mars_url)
        time.sleep(3)

        mars_html = browser.html
        mars_soup = BeautifulSoup(mars_html, "html.parser")

        news_title = mars_soup.find("div", class_ = "content_title").text.strip()
        news_p = mars_soup.find("div", class_ = "rollover_description_inner").text.strip()

        mars_info["news_title"] = news_title
        mars_info["news_subtitle"] = news_p


        jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        browser.visit(jpl_url)
        time.sleep(3)

        browser.click_link_by_partial_text("FULL IMAGE")
        time.sleep(3)

        browser.click_link_by_partial_text("more info")

        featured_pg = browser.html

        jpl_soup = BeautifulSoup(featured_pg, "html.parser")

        featured_img = jpl_soup.find("figure", class_ = "lede")
        featured_img_url =featured_img.a["href"]
        featured_img_url = ("https://www.jpl.nasa.gov" + featured_img_url)

        mars_info["featured_img"] = featured_img_url


        twitter_url = "https://twitter.com/marswxreport?lang=en"
        twitter_html = requests.get(twitter_url)
        twitter_soup = BeautifulSoup(twitter_html.text, "html.parser")
        time.sleep(3)

        mars_weather = twitter_soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()

        mars_info["weather"] = mars_weather

        facts_url = "http://space-facts.com/mars/"

        tables = pd.read_html(facts_url)

        facts_df = tables[0]
        facts_df.columns = ["Description", "Values"]
        facts_df.set_index("Description", inplace = True)

        facts_table = facts_df.to_html()
        mars_facts_table = facts_table.replace("\n", "")
        mars_info["facts_table"] = mars_facts_table

        hemisphere_img_urls = []
        hemisphere_dicts = {"title": [] , "img_url": []}

        astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

        browser.visit(astro_url)
        time.sleep(3)

        home_page = browser.html

        astro_soup = BeautifulSoup(home_page, "html.parser")
        results = astro_soup.find("h3")

        for result in results:
            raw_title = results.text
            title = raw_title[:-9]
                
            browser.click_link_by_partial_text(raw_title)
            time.sleep(1)
            img_url = browser.find_link_by_partial_href("download")["href"]
            
            hemisphere_dicts = {"title": title, "img_url": img_url}
            hemisphere_img_urls.append(hemisphere_dicts)
            time.sleep(3)
            browser.visit(astro_url)

        mars_info["hemi_imgs"] = hemisphere_img_urls

        return mars_info
