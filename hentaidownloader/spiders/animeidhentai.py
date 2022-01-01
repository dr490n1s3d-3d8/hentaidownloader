import scrapy


class AnimeidhentaiSpider(scrapy.Spider):
    name = 'animeidhentai'
    allowed_domains = ['animeidhentai.com']
    # start_urls = ['https://animeidhentai.com/']

    def start_requests(self):
        print('Choose the options below : \n 1.Latest Hentai \n 2.Uncensored Hentai \n 3.Choose a Genre')
        option = int(input('Enter Option Number Here :) - '))
        if option == 1 :
            yield scrapy.Request(url='https://animeidhentai.com/year/2021/',callback=self.parse,meta={'option':option})
        if option == 2 :
            yield scrapy.Request(url='https://animeidhentai.com/genre/hentai-uncensored/',callback=self.parse,meta={'option':option})
        if option == 3 :
            print('Choose a genre from below list :) - ')
            yield scrapy.Request(url='https://animeidhentai.com',callback=self.genre_parse)
        
    
    def parse(self,response):
        option = response.request.meta['option']
        if option == 1 :
            hentais=response.xpath("//a[@class='lnk-blk']")
            for hentai in hentais:
                title=hentai.xpath('.//@aria-label').get()
                # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
                link=hentai.xpath('.//@href').get()
                
                yield{
                    title,
                    link
                }
        elif option == 2:
            hentais=response.xpath("//a[@class='lnk-blk']")
            for hentai in hentais:
                title=hentai.xpath('.//@aria-label').get()
                # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
                link=hentai.xpath('.//@href').get()
    
                yield{
                    'title':title,
                    'source_link':link
                }
                
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
        for hentai in hentais:
            title=hentai.xpath('.//@aria-label').get()
            # title=response.xpath('//div[@class="ttl fz14 link-co"]/text()').get()
            link=hentai.xpath('.//@href').get()

            yield{
                'title':title,
                'source_link':link
            }
    
    ###################  Now Parsing Videos  #######################

        


          