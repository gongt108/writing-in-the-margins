# Define your item pipelines here
from itemadapter import ItemAdapter

# import mysql.connector
import os

db_password = os.getenv("DB_PASSWORD")


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        print(item["title"])
        return item


# class SaveToMySQLPipeline:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="tiffanygong",
#             password=db_password,
#             database="project4",
#         )

#         ## Create cursor, used to execute commands
#         self.cur = self.conn.cursor()

#         ## Create books table if none exists
#         self.cur.execute(
#             """
#         CREATE TABLE IF NOT EXISTS books(
#             id int NOT NULL auto_increment,
#             book_cover VARCHAR(255),
#             title text,
#             contributors VARCHAR(255),
#             avg_rating text,
#             num_rating text,
#             description LONGTEXT,
#             genres VARCHAR(255),
#             page_num VARCHAR(255),
#             publication_date VARCHAR(255),
#             book_id VARCHAR(255),
#         )
#         """
#         )

#     def process_item(self, item, spider):
#         ## Define insert statement
#         self.cur.execute(
#             """ insert into books (
#             url,
#             title,
#             upc,
#             product_type,
#             price_excl_tax,
#             price_incl_tax,
#             tax,
#             price,
#             availability,
#             num_reviews,
#             stars,
#             category,
#             description
#             ) values (
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s
#                 )""",
#             (
#                 item["url"],
#                 item["title"],
#                 item["upc"],
#                 item["product_type"],
#                 item["price_excl_tax"],
#                 item["price_incl_tax"],
#                 item["tax"],
#                 item["price"],
#                 item["availability"],
#                 item["num_reviews"],
#                 item["stars"],
#                 item["category"],
#                 str(item["description"][0]),
#             ),
#         )

#         # ## Execute insert of data into database
#         self.conn.commit()
#         return item

#     def close_spider(self, spider):
#         ## Close cursor & connection to database
#         self.cur.close()
#         self.conn.close()
