import scrapy
import logging

class UnderhentaiSpider(scrapy.Spider):
    name = 'underhentai'
    allowed_domains = ['underhentai.net']
    # start_urls = ['https://www.underhentai.net/']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.underhentai.net/',callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.97 Safari/537.36'})
    def parse(self, response):
        hentais=response.xpath("//div[@class='article-section loading']/a")
        for hentai in hentais:
            title=hentai.xpath(".//@title").get()
            link=hentai.xpath(".//@href").get()
            link=response.urljoin(link)
            # yield response.follow(url=link,callback=self.parse_video,meta={'title':title})
            yield{
                title : link
                # 'User-Agent':response.request.headers
            }
        
    # def parse_video(self,response):
    #     title=response.request.title
    #     logging.info(url)