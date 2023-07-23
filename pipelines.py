# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NorsemenscraperPipeline:
    def process_item(self, item, spider):
         # Check if the field is present
        if "actor_description" in item:
            # If the field is a list
            if isinstance(item["actor_description"], list):
                # Join the list items into a single string, then split and join to remove extra spaces
                item["actor_description"] = ' '.join(' '.join(item["actor_description"]).split())
            
            # Clean the string
            item["actor_description"] = self.clean_text(item["actor_description"])

        return item

    @staticmethod
    def clean_text(text):
        # Split and join the text to remove extra spaces, then remove unwanted characters
        text = ' '.join(text.split())
        return text.replace('"', '').replace('[', '').replace(']', '')
        
        
    
import psycopg2
import os 
class SaveToPostgreSQLPipeline:

    def __init__(self):
        DATABASE_URL = os.getenv('postgres://lucvierdfxortp:e91b0f5461b26645ae2dd72ab45ea1115e1b2924e2b26ddb4b96f6d5fbbc5832@ec2-35-169-9-79.compute-1.amazonaws.com:5432/df3uf8k36nralt')  # Get the Heroku Postgres URL from the environment variable
        self.conn = psycopg2.connect('postgres://lucvierdfxortp:e91b0f5461b26645ae2dd72ab45ea1115e1b2924e2b26ddb4b96f6d5fbbc5832@ec2-35-169-9-79.compute-1.amazonaws.com:5432/df3uf8k36nralt', sslmode='require')  # Connect to the Heroku Postgres database
        self.cur = self.conn.cursor()
        # Drop the table if it exists
        self.cur.execute("DROP TABLE IF EXISTS norsemen")
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS norsemen(
                            id SERIAL PRIMARY KEY,
                            img_url VARCHAR(2048),
                            character_description TEXT,
                            actor_name VARCHAR(255),
                            actor_description TEXT
                         )
                         """)
    
    def process_item(self,item,spider):
        self.cur.execute("""
                         INSERT INTO norsemen( 
                            img_url,
                            character_description,
                            actor_name,
                            actor_description
                            ) VALUES ( %s, %s, %s, %s)""",
                         ( item['img_url'], item['character_description'], item['actor_name'], item['actor_description']))
        self.conn.commit()
        return item


    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()



        