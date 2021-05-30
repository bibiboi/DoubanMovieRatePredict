# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from faker import Factory
#  生成不同的user-agent
f = Factory.create()
USER_AGENT = f.user_agent()
# 爬取到的最大页面
MAX_PAGE = 500


BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 延时设置
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# cookie设置
# COOKIES_ENABLED = False
COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
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
        # 'cookies': 'bid=tY8tdPBu0jQ; douban-fav-remind=1; __yadk_uid=8FmH4Gh3YbkvRBgkAPIoTbwRbgzfkUMj; ll="118268"; __gads=ID=3177cf6bcb18f2fd-2226e26cd9c700ff:T=1620271681:RT=1620271681:S=ALNI_MbVymfZbTC27oOz2WnpqNnxzSTKrA; ct=y; __utmc=30149280; __utmz=30149280.1621172875.16.6.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1621844067%2C%22https%3A%2F%2Fblog.csdn.net%2Fzhulove86%2Farticle%2Fdetails%2F84435751%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.589918251.1618415901.1621841437.1621844068.18; dbcl2="203460835:wR/GtMGaJkY"; ck=fBaG; _pk_id.100001.8cb4=bc337347ce692910.1618415899.7.1621844145.1621841436.; push_doumail_num=0; __utmv=30149280.20346; __utmb=30149280.3.10.1621844068; push_noty_num=2'

}
LOG_STDOUT = True

PROXIES = [
        '85.114.120.201:999',
        '58.253.158.194:9999',
        '60.7.208.240:9999',
        '58.253.158.102:9999',
        '60.169.150.41:9999',
        '27.147.210.35:8080',
        '113.194.50.163:9999',
        '39.96.25.191:8090',
        '61.161.28.199:9999',
        '60.169.135.78:9999',
        '41.220.114.154:8080',
        '59.63.74.101:9999',
        '45.231.223.252:999',
        '103.146.30.178:8080',
        '175.212.226.32:80',
        '59.55.160.157:3256',
        '59.55.166.181:3256',
        '58.253.154.225:9999',
        '52.90.32.235:80',
        '58.255.4.140:9999',
        '223.243.177.90:9999',
        '118.194.242.125:80',
        '177.135.228.3:53281',
        '159.192.97.42:8080',
        '54.254.24.192:3128',
        '58.255.207.113:9999',
        '60.31.89.69:9999',
        '58.253.157.77:9999',
        '60.31.89.99:9999',
        '58.253.145.242:9999',
        '46.35.249.189:41419',
        '60.19.236.217:9999',
        '181.115.67.3:999',
        '89.33.192.34:3128',
        '58.255.199.77:9999',
        '60.7.209.212:9999',
        '103.205.15.97:8080',
        '106.14.41.224:8080',
        '58.253.153.139:9999',
        '190.145.200.126:53281',
        '58.253.149.28:9999',
        '119.123.245.202:9000',
        '60.174.188.47:9999',
        '117.102.92.13:8080',
        '58.253.159.47:9999',
        '60.174.190.220:9999',
        '60.7.162.106:9999',
        '45.65.224.14:8080',
        '49.86.58.22:9999',
        '47.104.255.144:8118',
        '61.161.29.13:9999',
        '58.253.157.177:9999',
        '45.114.38.57:8080',
        '60.177.157.178:9000',
        '84.29.64.254:8080',
        '84.244.31.19:8080',
        '202.29.237.211:3128',
        '60.31.89.227:9999',
        '58.255.206.56:9999',
        '59.33.53.240:9999'
]

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tutorial.middlewares.TutorialSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'tutorial.middlewares.ProxyMiddleware': 543,
#    # 'tutorial.middlewares.TutorialDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# pipelines设置
ITEM_PIPELINES = {
        'tutorial.pipelines.MysqlPipeline': 300,
   # 'tutorial.pipelines.TutorialPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 1.5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# mysql 设置
MYSQL_HOST ='localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ly.19720424'
MYSQL_DATABASE = 'movie'
MYSQL_PORT = 3306