# DoubanMovieRatePredict


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 前言

<font color=#999AAA >这段时间对爬虫进行了一定的学习，爬虫除了requests和BeautifulSoup还有很多框架，使用requests等库写爬虫如果爬取量不是太大，速度要求不高，完全可以满足需求，但是爬虫内部许多代码和组件可以复用，如果把组件抽离出来将各个功能模块化，就可以形成一个框架，利用框架，可以不用再去关心某些功能的具体实现，只需要关心爬取逻辑即可。有了它们，可以大大简化代码量，而且架构也会变得清晰，爬取效率也会高许多。
常用的框架有pyspider、Scrapy等，为了提高学习效率，我用Scrapy爬取了豆瓣电影基本信息，构建了一个MLP模型预测豆瓣电影的评分。
</font>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 一、Scrapy爬虫爬取豆瓣电影


## 1. Scrapy框架介绍
### （1） Scrapy框架构造：

![Scrapy框架构造](https://img-blog.csdnimg.cn/2021053016525886.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

 - Engine，引擎，用来处理整个系统的数据流处理，触发事务，是整个框架的核心。
  - Item，项目，它定义了爬取结果的数据结构，爬取的数据会被赋值成该对象。
  -  Scheduler，调度器，用来接受引擎发过来的请求并加入队列中，并在引擎再次请求的时候提供给引擎。
 -  Downloader，下载器，用于下载网页内容，并将网页内容返回给蜘蛛。
  - Spiders，蜘蛛，其内定义了爬取的逻辑和网页的解析规则，它主要负责解析响应并生成提取结果和新的请求。 Item
 -  Pipeline，项目管道，负责处理由蜘蛛从网页中抽取的项目，它的主要任务是清洗、验证和存储数据。 Downloader
-   Middlewares，下载器中间件，位于引擎和下载器之间的钩子框架，主要是处理引擎与下载器之间的请求及响应。 
- Spider Middlewares， 蜘蛛中间件，位于引擎和蜘蛛之间的钩子框架，主要工作是处理蜘蛛输入的响应和输出的结果及新的请求。

### （2） 数据流
Scrapy 中的数据流由引擎控制，其过程如下:

- Engine 首先打开一个网站，找到处理该网站的 Spider 并向该 Spider 请求第一个要爬取的 URL。
- Engine 从 Spider 中获取到第一个要爬取的 URL 并通过 Scheduler 以 Request 的形式调度。
- Engine 向 Scheduler 请求下一个要爬取的 URL。
- Scheduler 返回下一个要爬取的 URL 给 Engine，Engine 将 URL 通过 Downloader Middlewares 转发给 Downloader 下载。
- 一旦页面下载完毕， Downloader 生成一个该页面的 Response，并将其通过 Downloader Middlewares 发送给 Engine。
- Engine 从下载器中接收到 Response 并通过 Spider Middlewares 发送给 Spider 处理。
- Spider 处理 Response 并返回爬取到的 Item 及新的 Request 给 Engine。
- Engine 将 Spider 返回的 Item 给 Item Pipeline，将新的 Request 给 Scheduler。
- 重复第二步到最后一步，直到 Scheduler 中没有更多的 Request，Engine 关闭该网站，爬取结束。

### （3） 项目结构
Scrapy通过命令行来创建项目，项目创建后的文件结构如下所示：

```bash
scrapy.cfg
project/
    __init__.py
    items.py
    pipelines.py
    settings.py
    middlewares.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
```

各个文件的功能描述如下：

- scrapy.cfg：它是 Scrapy 项目的配置文件，其内定义了项目的配置文件路径、部署相关信息等内容。
- items.py：它定义 Item 数据结构，所有的 Item 的定义都可以放这里。
- pipelines.py：它定义 Item Pipeline 的实现，所有的 Item Pipeline 的实现都可以放这里。
- settings.py：它定义项目的全局配置。
- middlewares.py：它定义 Spider Middlewares 和 Downloader Middlewares 的实现。
- spiders：其内包含一个个 Spider 的实现，每个 Spider 都有一个文件。

## 2. 创建爬虫爬取豆瓣

### （1）创建项目
安装好Scrapy库后，需要在命令行运行以下命令进行项目创建：

```bash
scrapy startproject tutorial
```
这个命令会创建一个名为tutorial的文件夹，文件夹结构如下所示：

```bash
scrapy.cfg     # Scrapy 部署时的配置文件
tutorial         # 项目的模块，引入的时候需要从这里引入
    __init__.py    
    items.py     # Items 的定义，定义爬取的数据结构
    middlewares.py   # Middlewares 的定义，定义爬取时的中间件
    pipelines.py       # Pipelines 的定义，定义数据管道
    settings.py       # 配置文件
    spiders         # 放置 Spiders 的文件夹
    __init__.py
```
创建项目后需要创建Spider，要生成quotes这个spider可执行以下命令：

```bash
cd tutorial # 进入tutorial文件夹
scrapy genspider quotes douban.com    # 执行genspider命令 'quotes':spider名称 'douban.com':网站域名
```
执行完毕后spiers文件夹中会多出一个quotes.py，它就是刚刚创建的Spider，内容如下：

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
```
- name，它是每个项目唯一的名字，用来区分不同的 Spider。
- allowed_domains，它是允许爬取的域名，如果初始或后续的请求链接不是这个域名下的，则请求链接会被过滤掉。
- start_urls，它包含了 Spider 在启动时爬取的 url 列表，初始请求是由它来定义的。
- parse，它是 Spider 的一个方法。默认情况下，被调用时 start_urls 里面的链接构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数。该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求。

### （2） 创建Item
Item是保存爬取数据的容器，它的使用方法和字典类似。不过，相比字典，Item 多了额外的保护机制，可以避免拼写错误或者定义字段错误。

考虑到要对评分进预测，我们爬取电影的名称、导演、编剧、类型作为特征，电影评分作为标签。
定义Item，将item.py修改如下：

```python
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
    # 电影评分
    rate = scrapy.Field()

```

### （3） 解析Response和Request
parse() 方法的参数 response 是 start_urls 里面的链接爬取后的结果。所以在 parse() 方法中，我们可以直接对 response 变量包含的内容进行解析，比如浏览请求结果的网页源代码，或者进一步分析源代码内容，或者找出结果中的链接而得到下一个请求。
为爬取到豆瓣的所有电影，我们将[https://movie.douban.com/tag/#/](https://movie.douban.com/tag/#/)作为入口，选择‘电影’，发现url变化为[https://movie.douban.com/tag/#/?sort=U&range=0,10&tag=电影](https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1)，因此将此URL设置为start_url

![选电影](https://img-blog.csdnimg.cn/20210530174503822.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

查看网页源码，使用插件Toggle JavaScript关闭js功能，发现页面无法加载，由此可知是本页面是动态加载，打开Network的JS或XHR类目，点击加载更多，将链接在新窗口打开

![页面分析](https://img-blog.csdnimg.cn/20210530203238614.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
发现返回的是一个json页面

![json](https://img-blog.csdnimg.cn/2021053020343818.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

同样的方式多打开几个页面，观察链接规律，发现每次加载URL变化的只有最后的start数值，因此翻页循环链接可以通过循环改变start数值获取。

此部分参考[scrapy爬取豆瓣所有电影信息](https://blog.csdn.net/qingminxiehui/article/details/81671161?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522162237734216780265439601%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=162237734216780265439601&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-81671161.first_rank_v2_pc_rank_v29&utm_term=Scrapy%E7%88%AC%E5%8F%96%E8%B1%86%E7%93%A3%E7%94%B5%E5%BD%B1&spm=1018.2226.3001.4187)

分析返回的json页面，发现只能获取到电影导演、评分、名字和主演，但是可以发现我们可以获取到电影的URL，任选其中一部电影的URL打开：

![电影详情](https://img-blog.csdnimg.cn/20210530205924601.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

恰好是电影的详情页面，对电影详情页进行解析，关闭js功能，页面仍然可以显示，查看页面源代码进行解析，使用Scrapy自己的数据提取方法Selector中的Xpath选择器对要提取的信息进行选择，Google提供直接获取XPath：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530211451572.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

依次选中需爬取的信息，然后生成Item存储信息。

修改quotes.py:

```python
import json

import scrapy
from scrapy import Spider, Request,Selector
from tutorial.items import MovieItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.com']
    start_urls = ['https://movie.douban.com/tag/#/']
    movie_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={count}'
    cookies = '你的cookies'
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

    def start_requests(self):
        """
        设置开始请求的url
        """
        for count in range(self.settings.get('MAX_PAGE')):
            url = self.movie_url.format(count=(count * 20))
            yield Request(url, self.parse, cookies=self.cookies, dont_filter=True)


    def parse(self, response):
        """
        获取电影详情页
        :param response:
        """
        result = json.loads(response.text)
        for movie in result.get('data'):
            detailed_movie_url = movie.get('url')
            yield Request(detailed_movie_url, callback=self.parse_movie, cookies=self.cookies, dont_filter=True)

    def parse_movie(self,response):
        """
        解析电影信息
        :param response:
        """
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
        # 类型
        Type = []
        for i in range(5, 8):
            s = '//*[@id="info"]/span[% s]/text()' % str(i)
            t = selector.xpath(s).extract()
            if (t not in [['制片国家/地区:'],['官方网站:']]):
                Type.extend(t)
            else:
                break
        movie['type'] = " ".join(Type)
        movie['rate'] = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        yield movie
```
为躲避豆瓣的反爬机制和解决爬取过程中的重定向问题，需要在setting.py进行设置

```python
# 爬取到的最大页面
MAX_PAGE = 500

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 延时设置
DOWNLOAD_DELAY = 3
# cookie设置
# COOKIES_ENABLED = False
COOKIES_DEBUG = True
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://accounts.douban.com/',
        'Host': 'movie.douban.com',
        # 'User-Agent': f.user_agent()
        'User-Agent': [
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                ],
}
LOG_STDOUT = True
```

*需注意的问题：*

 1. 关闭js功能和未关闭js功能的页面源码并不一致，如果在未关闭js功能时copy XPath，会导致电影主演名单无法获取到，因此需要关闭js功能后再copy XPath
 2. 尽管设置了延时等一系列操作，但是爬取几百条数据后豆瓣仍会显示ip检测异常，需要登录才显示页面，这个项目中我没有进行模拟登录，而是直接获取已登录账号的cookies，在quotes.py中每次获取requests时添加cookies

### （4） Item Pipeline连接mysql数据库存储数据
*注：运行Scrapy可直接将结果保存到文件，则可不使用数据库*

Item Pipeline的调用发生在 Spider 产生 Item 之后。当 Spider 解析完 Response 之后，Item 就会传递到 Item Pipeline，被定义的 Item Pipeline 组件会顺次调用，完成一连串的处理过程，比如数据清洗、存储等。

使用Navicat连接MySQL数据库，新建一个数据库movie，新建一个数据表movie_detail3，在pipeline.py中实现一个MySQLPipeline对Item中的数据进行存储：

```python

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
import pandas as pd

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
        # 插入数据
        sql = 'insert into movie_detail3(% s) values (% s)' % (keys,values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item
```
并在settings.py中进行设置：

```python
# mysql 设置
MYSQL_HOST ='localhost'
MYSQL_USER = '你的用户名'
MYSQL_PASSWORD = '你的密码'
MYSQL_DATABASE = 'movie'
MYSQL_PORT = 3306

# pipelines设置
ITEM_PIPELINES = {
        'tutorial.pipelines.MysqlPipeline': 300,
   # 'tutorial.pipelines.TutorialPipeline': 300,
}
```

### （5） 运行爬虫
命令行进入目录，运行如下命令，就可看到Scrapy的运行结果

```python
scrapy crawl quotes
```

要将输出结果保存到文件，运行如下命令：

```python
scrapy crawl quotes -o quotes.csv
```

若需要对Scrapy中代码的进行调试，在items.py的同路径下新建debug.py

```python
from scrapy.cmdline import execute
execute()
```
设置Edit Configurations

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530215641144.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021053021574972.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
对debug.py进行调试即可对各文件代码进行调试，也可直接运行debug,py运行爬虫，则不需要在命令行输入命令运行。

# 二、构建豆瓣电影评分预测模型
使用pytorch构建模型，见于movie_predict.py

## 1.连接数据库
导包并连接数据库
```python
from sklearn.preprocessing import LabelEncoder
import pymysql
import pandas as pd
import torch

db = pymysql.connect(host="localhost", database="movie", user="你的用户名", password="你的密码")
cursor = db.cursor()
sql = "select * from movie_detail3"
cursor.execute(sql)
data1 = cursor.fetchone()
data = cursor.fetchall()
# print(list(data))
columns = ['name', 'director', 'screenWriter', 'actors', 'type', 'rate']
movie = pd.DataFrame(list(data), columns=columns)
```
读取的数据如下
![电影](https://img-blog.csdnimg.cn/20210530221519328.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

## 2.数据预处理

查看特征重复率

```python
print("================特征值重复率================")
for item in columns:
    print("% s\t" % item, movie[item].duplicated().sum()/movie.shape[0])
```
![特征重复率](https://img-blog.csdnimg.cn/20210530221900954.png#pic_center)

因此考虑对"类型"这一特征哑编码，对“演员”这一特征标签编码，对“导演”、“编剧”进行目标编码


```python
# 将type这一离散值特征转换为连续值特征 进行哑编码
movie_type = pd.get_dummies(movie['type'], dummy_na=True)

# 对actors进行标签编码
actors_le = LabelEncoder()
actors_le.fit(movie['actors'])
actors_le.transform(movie['actors'])

from category_encoders.target_encoder import TargetEncoder
movie_rate = movie['rate'].astype(float)
# 对director screenWriter 进行目标编码
d_sW_enc = TargetEncoder(cols=['director','screenWriter']).fit(movie,movie_rate)
movie2 = d_sW_enc.transform(movie,movie_rate)
movie2['actors_enc'] = actors_le.transform(movie['actors'])

# 整合数据
movie2 = pd.concat([movie2,movie_type],axis=1)
movie2.drop(columns=['actors','type','语言: 上映日期: 2019-11-01(中国大陆网络)','name'],inplace=True)
```
## 3. 定义模型

```python
from torch import nn
from torch.utils import data
from torch import optim
import matplotlib.pyplot as plt
from IPython import display

# 导入数据
train_features = torch.tensor(movie2.values)
train_labels = torch.tensor(movie_rate.values)
in_features = train_features.shape[1]

# 定义损失函数
loss = nn.MSELoss()

# 模型1：线性回归模型
def net():
    net = nn.Sequential(nn.Linear(349,1))
                    
    #初始化模型参数
    for params in net.parameters():
        nn.init.normal_(params,mean=0,std=0.01)
    return net

# 模型2：MLP多层感知器 两层隐藏层
net2 = nn.Sequential(nn.Flatten(), nn.Linear(349,128), nn.ReLU(), nn.Linear(128,1))
def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)
net2.apply(init_weights)

# 模型3：MLP多层感知器 三层隐藏层
net3 = nn.Sequential(nn.Flatten(),nn.Linear(349,128),nn.ReLU(),nn.Linear(128,64),
                     nn.ReLU(),nn.Linear(64,1))
def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)
net3.apply(init_weights)

# 定义对数均方根误差计算得分
def log_rmse(net, features, labels):
    # 为了在取对数时进一步稳定该值，将小于1的值设置为1
    clipped_preds = torch.clamp(net(features.float()), 1, float('inf'))
    rmse = torch.sqrt(loss(torch.log(clipped_preds), torch.log(labels)))
    return rmse.item()
```

## 4. 训练模型

```python
# 训练模型
def train(net,train_features,train_labels,test_features,test_labels,
          num_epochs,learning_rate,weight_decay,batch_size):
    
    train_ls,test_ls = [],[] # 计算训练集和测试集损失
    dataset = data.TensorDataset(train_features,train_labels)
    data_iter = data.DataLoader(dataset,batch_size,shuffle=True)
    # 优化器：adam
    optimizer = optim.Adam(params=net.parameters(),lr=learning_rate,
                           weight_decay=weight_decay)
    net = net.float()
    for epoch in range(num_epochs):
        for x,y in data_iter:
            l = loss(net(x.float()),y.float()) # 计算损失
            optimizer.zero_grad() # 梯度归零
            l.backward() # 反向传播
            optimizer.step()
        train_ls.append(log_rmse(net,train_features,train_labels))
        if test_labels is not None:
            test_ls.append(log_rmse(net,test_features,test_labels))
    return train_ls,test_ls

# 画图
def use_svg_display():
    # 用矢量图表示
    display.set_matplotlib_formats('svg')

def set_figsize(figsize = (3.5,2.5)):
    use_svg_display()
    # 设置图像尺寸
    plt.rcParams['figure.figsize'] = figsize

# 半对数函数
def semilogy(x_vals,y_vals,x_label,y_label,x2_vals=None,y2_vals=None,
             legend=None,figsize=(3.5,2.5)):
    set_figsize(figsize)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.semilogy(x_vals,y_vals)
    if x2_vals and y2_vals:
        plt.semilogy(x2_vals,y2_vals,linestyle=':')
        plt.legend(legend)
    plt.show()
```

## 5. k折交叉验证

```python
def get_k_fold_data(k,i,X,y):
    assert k > 1
    fold_size = X.shape[0] // k
    x_train,y_train = None,None
    for j in range(k):
        idx = slice(j*fold_size,(j+1)*fold_size,1)
#         print(idx)
        x_part ,y_part = X[idx,:],y[idx]
        if j == i:
            x_valid,y_valid = x_part,y_part
        elif x_train is None:
            x_train,y_train = x_part,y_part
        else:
            x_train = torch.cat((x_train,x_part),dim=0)
            y_train = torch.cat((y_train,y_part),dim=0)
    return x_train,y_train,x_valid,y_valid

def k_fold(k,x_train,y_train,num_epochs,learning_rate,weight_decay,batch_size):
    train_l_sum,valid_l_sum = 0,0
    for i in range(k):
        data = get_k_fold_data(k,i,x_train,y_train)
		# train_ls,valid_ls = train(net=net(),*data,num_epochs,learning_rate,weight_decay,batch_size) 模型1
		# train_ls,valid_ls = train(net2,*data,num_epochs,learning_rate,weight_decay,batch_size) 模型2
        train_ls,valid_ls = train(net3,*data,num_epochs,learning_rate,
                                 weight_decay,batch_size)
        train_l_sum += train_ls[-1]
        valid_l_sum += valid_ls[-1]
        if i==0:
            semilogy(range(1,num_epochs + 1),train_ls,'epoch','rmse',
                     range(1,num_epochs + 1),valid_ls,['train','valid'])
        print('fold %d, train rmse %f, valid rmse %f' % 
              (i,train_ls[-1],valid_ls[-1]))
    return train_l_sum/k,valid_l_sum/k
```



## 6. 训练及调参

```python
# 模型1
k, num_epochs, lr, weight_decay, batch_size = 5, 100, 0.1, 0.01, 32

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530224948806.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

```python
# 模型2
k, num_epochs, lr, weight_decay, batch_size = 5, 50, 0.1, 0.01, 256

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530224958292.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

```python
# 模型2
k, num_epochs, lr, weight_decay, batch_size = 5, 100, 0.1, 0.01, 256

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530225006399.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
```python
# 模型2
k, num_epochs, lr, weight_decay, batch_size = 5, 50, 0.25, 0.01, 256

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530225014814.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
```python
# 模型3
k, num_epochs, lr, weight_decay, batch_size = 5, 50, 0.25, 0.01, 256

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021053022523621.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)


```python
# 模型3
k, num_epochs, lr, weight_decay, batch_size = 5, 100, 0.1, 0.01, 256

train_l, valid_l = k_fold(k,train_features,train_labels,num_epochs,lr,
                          weight_decay,batch_size)
print('%d-fold validation ：avg train rmse %f ,avg valid rmse %f' %(k,train_l,valid_l))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530225244697.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 总结
<font color=#999AAA >通过这个小项目对Scrapy有了初步了解，过程中遇到了很多问题好在最后解决得七七八八，搭建模型这块没有再深入思考，众多不足，日后改进。
