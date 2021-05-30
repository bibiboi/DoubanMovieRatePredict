# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
import pandas as pd

class TutorialPipeline:
    def process_item(self, item, spider):
        # return item
        data = dict(item)
        dataframe = pd.DataFrame(data)
        file_path = pd.ExcelWriter('D:\Python document\pachong\result\movie_result.xlsx')
        dataframe.to_excel(file_path,'movie_result',encoding='utf8')
        file_path.save()

class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
                   database=crawler.settings.get('MYSQL_DATABASE'),
                   user=crawler.settings.get('MYSQL_USER'),
                   password=crawler.settings.get('MYSQL_PASSWORD'),
                   port=crawler.settings.get('MYSQL_PORT'),
            )
    def open_spider(self, spider):
        self.db = pymysql.connect(user=self.user, password=self.password, host=self.host,
                                  database=self.database, port=self.port, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['% s'] * len(data))
        sql = 'insert into movie_detail3(% s) values (% s)' % (keys,values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item