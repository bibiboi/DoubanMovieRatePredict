import json

import scrapy
from scrapy import Spider, Request,Selector
from tutorial.items import MovieItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.com']
    start_urls = ['https://movie.douban.com/tag/#/']
    movie_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={count}'
    cookies = 'bid=tY8tdPBu0jQ; douban-fav-remind=1; __yadk_uid=8FmH4Gh3YbkvRBgkAPIoTbwRbgzfkUMj; ll="118268"; __gads=ID=3177cf6bcb18f2fd-2226e26cd9c700ff:T=1620271681:RT=1620271681:S=ALNI_MbVymfZbTC27oOz2WnpqNnxzSTKrA; ct=y; __utmc=30149280; __utmz=30149280.1621172875.16.6.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1621844067%2C%22https%3A%2F%2Fblog.csdn.net%2Fzhulove86%2Farticle%2Fdetails%2F84435751%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.589918251.1618415901.1621841437.1621844068.18; dbcl2="203460835:wR/GtMGaJkY"; ck=fBaG; _pk_id.100001.8cb4=bc337347ce692910.1618415899.7.1621844145.1621841436.; push_doumail_num=0; __utmv=30149280.20346; __utmb=30149280.3.10.1621844068; push_noty_num=2'
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

    def start_requests(self):
        """
        设置开始请求的url
        """
        for count in range(self.settings.get('MAX_PAGE')):
            url = self.movie_url.format(count=(count * 20))
            yield Request(url, self.parse, cookies=self.cookies, dont_filter=True)
            # yield Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        # for count in range(50):
        #     url = self.movie_url.format(count = (count*20))
        #     yield scrapy.Request(
        #         url,
        #         callback=self.parse_main
        #     )
        """
        获取电影详情页
        :param response:
        """
        result = json.loads(response.text)
        for movie in result.get('data'):
            # item = MovieItem()
            # item['name'] = movie.get('title')
            # item['director'] = movie.get('directors')
            # item['rate'] = movie.get('rate')
            # item['actors'] = movie.get('casts')
            # yield item
            detailed_movie_url = movie.get('url')
            yield Request(detailed_movie_url, callback=self.parse_movie, cookies=self.cookies, dont_filter=True)

    def parse_movie(self,response):
        """
        解析电影信息
        :param response:
        """
        # result = json.loads(response.text)
        selector = Selector(text=response.text)
        movie = MovieItem()
        # 名字
        movie['name'] = " ".join(selector.xpath('//*[@id="content"]/h1/span[1]/text()').extract())
        # 导演
        movie['director'] = " ".join(selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract())
        # 编剧
        movie['screenWriter'] = " ".join(selector.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract())
        # 主演
        movie['actors'] = " ".join(selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract())
        # //*[@id="info"]/span[3]/span[2]/span[1]/a
        # //*[@id="info"]/span[3]/span[2]/a[1]
        # 类型
        Type = []
        for i in range(5, 8):
            s = '//*[@id="info"]/span[% s]/text()' % str(i)
            # //*[@id="info"]/span[6]
            t = selector.xpath(s).extract()
            if (t not in [['制片国家/地区:'],['官方网站:']]):
                Type.extend(t)
            else:
                break
        movie['type'] = " ".join(Type)
        movie['rate'] = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        # //*[@id="interest_sectl"]/div[1]/div[2]/strong
        # movie['rate'] = float(rate)
        yield movie



