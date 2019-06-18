import scrapy
import mysql.connector
import re

from ..items import PcapItem


class QuoteSpider(scrapy.Spider):
    name = "spyder"

    def start_requests(self):

        db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='pcap02'
        )
        cur = db.cursor()
        cur.execute("SELECT a.shop_id,a.competitor_id,a.product_url,a.product_id,c.price_numeric,"
                    + "c.price_decimal, c.stock "
                    + "FROM za_product_urls a "
                    + "inner join za_crawler_configuration c on a.competitor_id=c.competitor_id "
                    + "where (a.product_url is not null and a.product_url <> '') and c.crawler_type='SPYDER'")

        for url in cur.fetchall():
            if url is not None:
                yield scrapy.Request(url[2], dont_filter=True,
                                     meta={'shopId': url[0], 'competitorId': url[1], 'productId': url[3],
                                           'priceNumeric': url[4], 'priceDecimal': url[5], 'stock': url[6]})
        cur.close()

    def parse(self, response):
        print("response" + str(response))
        url = response.request.url
        items = PcapItem()
        price_numeric = response.meta['priceNumeric']
        price_decimal = response.meta['priceDecimal']
        stock = response.meta['stock']
        stock = response.css(stock).extract_first()
        stock = stock.strip()
        if stock.find('stock') is True:
            print("STRING>>>>>>>>>>>>>>>>>>>"+stock)

        print(stock)
        numeric = response.css(price_numeric).extract_first()
        numeric = re.sub(r"[^0-9.]+", '', numeric)
        items['price'] = numeric
        if price_decimal is not None:
            decimal = response.css(price_decimal).extract_first()
            items['price'] = numeric + '.' + decimal
        items['url'] = url
        items['shopId'] = response.meta['shopId']
        items['competitorId'] = response.meta['competitorId']
        items['productId'] = response.meta['productId']

        yield items
