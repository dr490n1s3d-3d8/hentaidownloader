import scrapy
from scrapy_splash import SplashRequest
import wget
from download import download
import os

class AnimeidhentaiSpider(scrapy.Spider):
    name = 'animeidhentai'
    allowed_domains = ['animeidhentai.com']
    # start_urls = ['https://animeidhentai.com/']
    
    def start_requests(self):
        print('Choose the options below : \n 1.Latest Hentai \n 2.Uncensored Hentai \n 3.Choose a Genre')
        option = int(input('Enter Option Number Here :) - '))
        if option == 1 :
            yield scrapy.Request(url='https://animeidhentai.com/',callback=self.parse,meta={'option':option})
        if option == 2 :
            yield scrapy.Request(url='https://animeidhentai.com/genre/hentai-uncensored/',callback=self.parse,meta={'option':option})
        if option == 3 :
            print('Choose a genre from below list :) - ')
            yield scrapy.Request(url='https://animeidhentai.com',callback=self.genre_parse)
        
    
    def parse(self,response):
        option = response.request.meta['option']
        if option == 1 :
            hentai_list={}
            refer_hentai=0
            hentais=response.xpath("//div[@class='tb-bx mgt']//a[@class='lnk-blk']")
            for hentai in hentais:
                title=hentai.xpath('.//@aria-label').get()
                # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
                link=hentai.xpath('.//@href').get()
                hentai_list.update({refer_hentai:[title,link]})
                refer_hentai+=1

            for n in range(len(hentai_list)):
                print(str(n)+'.'+hentai_list[n][0])
            hentai_chosen=int(input('Enter Desired Hentai Number from list :) -'))
            chosen_title=hentai_list[int(hentai_chosen)][0]
            yield scrapy.Request(url=hentai_list[int(hentai_chosen)][1],callback=self.video_parse,meta={'title':chosen_title})
        elif option == 2:
            hentai_list={}
            refer_hentai=0
            hentais=response.xpath("//a[@class='lnk-blk']")
            for hentai in hentais:
                title=hentai.xpath('.//@aria-label').get()
                # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
                link=hentai.xpath('.//@href').get()
                hentai_list.update({refer_hentai:[title,link]})
                refer_hentai+=1

            for n in range(len(hentai_list)):
                print(str(n)+'.'+hentai_list[n][0])
            hentai_chosen=int(input('Enter Desired Hentai Number from list :) -'))
            chosen_title=hentai_list[int(hentai_chosen)][0]
            yield scrapy.Request(url=hentai_list[int(hentai_chosen)][1],callback=self.video_parse,meta={'title':chosen_title})
                
    def genre_parse(self,response):
        list=response.xpath(".//section[7]//a[@class='lnk-blk']")
        genre_list={}
        refer_genre=0
        
        for genres in list:
            genre=genres.xpath('.//@aria-label').get()
            genre_link=genres.xpath('.//@href').get()
            genre_list.update({refer_genre:[genre,genre_link]})
            refer_genre+=1

        for n in range(len(genre_list)):
            print(str(n)+'.'+genre_list[n][0])
        genre_chosen=input('Enter Desired Genre Number from list :) -')
        yield scrapy.Request(url=genre_list[int(genre_chosen)][1],callback=self.parse_genre_list)
            
    def parse_genre_list(self,response):
        hentais=response.xpath("//a[@class='lnk-blk']")
        refer_hentai=0
        hentai_list={}

        for hentai in hentais:
            title=hentai.xpath('.//@aria-label').get()
            # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
            link=hentai.xpath('.//@href').get()
            hentai_list.update({refer_hentai:[title,link]})
            refer_hentai+=1

        for n in range(len(hentai_list)):
            print(str(n)+'.'+hentai_list[n][0])
        hentai_chosen=int(input('Enter Desired Hentai Number from list :) -'))
        chosen_title=hentai_list[int(hentai_chosen)][0]
        yield scrapy.Request(url=hentai_list[int(hentai_chosen)][1],callback=self.video_parse,meta={'title':chosen_title})
    ###################  Now Parsing Videos  #######################
    video_script='''
        function main(splash, args)
            splash.private_mode_enabled=False
            assert(splash:go(args.url))
            assert(splash:wait(15))
            return {
                html = splash:html()
            }
        end
    '''
    def video_parse(self,response):
       video_link=response.xpath('//div[@class="embed rad2"]/iframe/@data-litespeed-src').get()
       yield SplashRequest(url=video_link,callback=self.downvideo,endpoint='http://localhost:8050/execute',args={
           'lua_source' : self.video_script,
           'resource_timeout': 10
       },dont_filter=True,meta={'title':response.request.meta['title']})
    
    def downvideo(self , response):
        link=response.xpath('//a[@class="c-list__item dropdown-item"]/@href').get()
        print(link)
        home=os.path.expanduser('~')
        title=response.request.meta['title']
        hentaidir=f'{home}/.hentai' 
        if os.path.isdir(hentaidir):
            download(link,f'{home}/.hentai/{title}.mp4',progressbar=True)
        else:
            os.mkdir(f'{home}/.hentai')
            download(link,f'{home}/.hentai/{title}.mp4',progressbar=True)


          