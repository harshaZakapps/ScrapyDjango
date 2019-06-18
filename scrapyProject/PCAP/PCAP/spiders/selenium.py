import scrapy
import mysql.connector
import re

from ..items import PcapItem
from selenium import webdriver
import time


class QuoteSpider(scrapy.Spider):
    name = "selenium"
    start_urls = ['https://www.uberkids.com/uk/uppababy-vista-rumble-seat-2003042/']

    def __init__(self, *args, **kwargs):
        super(QuoteSpider, self).__init__(*args, **kwargs)
        self.download_delay = 0.25
        self.browser = webdriver.Chrome('C:/Users/Lenovopc/Downloads/chromedriver_win32/chromedriver.exe')
        self.browser.implicitly_wait(60)

    def parse(self, response):
        self.browser.get(response.url)  # load response to the browser
        button = self.browser.find_element_by_xpath("//button[@class='super-attribute-select']")  # find
        # the element to click to
        button.click()  # click
        time.sleep(1)  # wait until the page is fully loaded
        source = self.browser.page_source  # get source of the loaded page
        print(source)
    # sel = Selector(text=source)  # create a Selector object
    # data = sel.xpath('path/to/the/data')  # select data
