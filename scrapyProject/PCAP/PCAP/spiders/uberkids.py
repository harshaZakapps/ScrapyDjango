import scrapy
import mysql.connector
from ..items import PcapItem


class QuoteSpider(scrapy.Spider):
    name = "uberkids"

    start_urls = [
        "https://www.uberkids.com/uk/cybex-solution-s-fix-group-2-3-car-seat-2002065/"
    ]

    def parse(self, response):
        print("response" + str(response))
        price_decimal = None
        numeric = '$1,099.99'
        numeric = str(numeric).strip('$,£')
        print(numeric)
        if price_decimal is not None:
            decimal = response.css(price_decimal).extract_first()
            totalprice = numeric + '.' + decimal

        return totalprice
