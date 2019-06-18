import mysql.connector


class PcapPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='pcap02'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_history(item)
        self.store_db(item)
        # self.store_db(item)
        # self.close_connection()
        return item

    def store_db(self, item):
        insert_stmt = (
            "INSERT INTO za_competitor_products(sale_price,competitor_id,product_id) "
            "VALUES(%(price)s, %(competitorId)s, %(productId)s) "
            "ON DUPLICATE KEY UPDATE sale_price = %(price)s "

        )

        price = item['price']
        shop_id = item['shopId']
        competitor_id = item['competitorId']
        product_id = item['productId']
        self.curr.execute(insert_stmt, {'price': price, 'shopId': shop_id,
                                        'competitorId': competitor_id, 'productId': product_id})
        self.conn.commit()

    def store_history(self, item):
        parsed_price = item['price']
        shop_id = item['shopId']
        competitor_id = item['competitorId']
        product_id = item['productId']

        self.curr.execute(
            "select sale_price from za_competitor_products where "
            "competitor_id= %(competitorId)s  and product_id= %(productId)s ",
            {'competitorId': competitor_id, 'productId': product_id}
        )
        current_price = self.curr.fetchone()
        if current_price is None or (current_price is not None and str(current_price[0]) != str(parsed_price)):
            insert_stmt = (
                "insert into za_competitor_price_history (price,competitor_id,product_id)"
                " values ( %(price)s, %(competitorId)s, %(productId)s )"
            )

            self.curr.execute(insert_stmt, {'price': parsed_price, 'shopId': shop_id,
                                            'competitorId': competitor_id, 'productId': product_id})

            self.conn.commit()

    def close_connection(self):
        self.curr.close()
        self.conn.close()
