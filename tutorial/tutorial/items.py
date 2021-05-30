# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # 电影名称
    name = scrapy.Field()
    # 电影导演
    director = scrapy.Field()
    # 电影编剧
    screenWriter = scrapy.Field()
    # 电影主演
    actors = scrapy.Field()
    # 电影类型
    type = scrapy.Field()
    # # 制片国家/地区
    # productCountry = scrapy.Field()
    # # 电影上映时间
    # time = scrapy.Field()
    # 电影评分
    rate = scrapy.Field()


