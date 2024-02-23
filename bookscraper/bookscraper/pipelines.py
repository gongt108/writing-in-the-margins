# Define your item pipelines here
from itemadapter import ItemAdapter
import os

key = "DB_PASSWORD"
db_password = os.getenv(key)
print("db_password", db_password)


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        short_list_keys = ["contributors", "genres"]
        for short_list_key in short_list_keys:
            list = adapter.get(short_list_key)
            if len(list) > 1:
                adapter[short_list_key] = ", ".join(list)
            else:
                adapter[short_list_key] = list[0]

        description = adapter.get("description")
        adapter["description"] = "/n/n".join(description)
        return item


import psycopg2


class SaveToPostgresPipeline:
    def __init__(self):
        self.host = "localhost"
        self.user = "tiffanygong"
        self.password = "testpass"
        self.database = "project4"

        ## Create cursor, used to execute commands
        self.connection = psycopg2.connect(
            host=self.host, user=self.user, password=self.password, dbname=self.database
        )
        self.cur = self.connection.cursor()

        ## Create books table if none exists
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS base_book(
            id serial PRIMARY KEY, 
            book_cover VARCHAR(255),
            title text,
            contributors VARCHAR(255),
            avg_rating text,
            num_rating text,
            description TEXT,
            genres VARCHAR(255),
            page_num VARCHAR(255),
            publication_date VARCHAR(255),
            book_id VARCHAR(255)
        )
        """
        )

    def process_item(self, item, spider):
        print("saving to db")

        ## Define insert statement
        self.cur.execute(
            """ insert into base_book (
            book_cover,
            title,
            contributors,
            avg_rating,
            num_rating,
            description,
            genres,
            page_num,
            publication_date,
            book_id
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                
                )""",
            (
                item["book_cover"],
                item["title"],
                item["contributors"],
                item["avg_rating"],
                item["num_rating"],
                item["description"],
                item["genres"],
                item["page_num"],
                item["publication_date"],
                item["book_id"],
            ),
        )

        # ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
