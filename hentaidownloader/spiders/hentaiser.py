import scrapy
import json
import encodings
import unicodedata

class HentaiserSpider(scrapy.Spider):
    name = 'hentaiser'
    allowed_domains = ['app.hentaiser.com/animes/tag/impregnation']
    # start_urls = ['https://app.hentaiser.com/animes/tag/impregnation/']

    def start_requests(self):
        yield scrapy.Request(url='https://api.hentaiser.com/1.2/videos/search/tag/impregnation/page/1',callback=self.parse,headers={'accept-encoding': 'gzip, deflate, br','authority': 'api.hentaiser.com','method': 'GET','path': '/1.2/videos/search/tag/impregnation/page/1','content' : 'application/json','origin': 'https://app.hentaiser.com','referer': 'https://app.hentaiser.com/','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.97 Safari/537.36'})
    
    # anime_path = 'https://app.hentaiser.com/anime/'
    def parse(self, response):
        # hentais = response.xpath("//div[@class='thumb-video']")
        # for hentai in hentais:
        #     title = hentai.xpath('.//p/text()').get()
        #     link  = hentai.xpath('.//@gid').get()
        #     link = anime_path + link
        #     yield {
        #         'title' : title,
        #         'link'  : link
                
        #      }
        # yield{
        #     'User-Agent' : response.request.headers
        # }
        # raw_data = json.loads(response.text)
        # print(raw_data)
        raw_data = response.body
        yield raw_data