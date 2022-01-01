import scrapy


class HanimeSpider(scrapy.Spider):
    name = 'hanime'
    allowed_domains = ['hanime.tv']
    start_urls = ['https://hanime.tv']

    def parse(self, response):
        # titles=response.xpath("//div[@class='hv-title']/text()")
        # links=response.xpath("//div[@class='elevation-3 mb-3 hvc item card']/a/@href")
        #we can use response.urljoin(video_link)
        #we can use response.follow(url=video_link)
        # for title in titles:
        #     title =str(title.get()).lstrip().rstrip()
        #     # yield{
        #     # 'title' : title
        #     # } 
        hentais = response.xpath("//div[@class='elevation-3 mb-3 hvc item card']/a")
        for hentai in hentais:
            video_link='https://hanime.tv'+str(hentai.xpath(".//@href").get())
            title =str(hentai.xpath(".//@title").get()).strip("hentai stream online HD 1080p, 720p")
            # yield{
            #     'link'  :video_link,
            # }
            yield response.follow(url=video_link,callback=self.parse_video,meta={'title':title})

       
        
    def parse_video(self,response):
        title=response.request.meta['title']
        download_pages=response.xpath("//a[@class='hvpab-btn flex align-center primary-color-hover']/@href")
        for page in download_pages:
            page='https://hanime.tv'+page.get()
            yield{
                title:page
            }
