import scrapy
from pathlib import Path
from urllib.parse import urlparse,parse_qs, urlunparse, urlencode
from etymoscrape.utils import stripper,cleaner
    

class TestSpider(scrapy.Spider):
    name = "etym_all"

    start_urls = [f"https://www.etymonline.com/search?q={chr(c)}" for c in range(ord('A'), ord('Z')+1)]

      
    def parse(self, response):

        base_url = "https://www.etymonline.com"

        entries = response.xpath("//div[contains(@class,'flex flex-col') and .//span[contains(@class,'hyphens-auto')]]")

        for entry in entries:
                word = entry.xpath(".//span[contains(@class,'hyphens-auto')]/text()").get(default="").strip()
                pos = entry.xpath(".//span[contains(@class,'text-battleship-gray')]/text()").get(default="")
                pos = stripper(pos)
                
                etym_nodes = entry.xpath(".//section[contains(@class,'prose')]/descendant::text()").getall()
                etymology = cleaner(etym_nodes)

                word_url = entry.xpath(".//a[contains(@class,'group')]/@href").get(default="")
                word_url = base_url + word_url if word_url else ""
    
                yield {
                        "word": word,
                        "part_of_speech": pos,
                        "etymology": etymology,
                        "url": word_url
                    }





        #SAD ATTEMPTS AT MAKING THIS SHIT WORK
        #I KEPT THEM MOSTLY TO TEST IN THE SCRAPY SHELL 

        #raw_words = response.xpath("//span[contains(@class, 'hyphens-auto')]/text()").getall()
        #words = [stripper(w) for w in raw_words]
        #raw_pos = response.xpath(".//span[contains(@class, 'text-battleship-gray')]/text()").get()
        #pos = stripper(raw_pos)
        #etym_nodes = response.xpath(".//section[contains(@class,'-mt-4')]/descendant::text()").getall()
        #etymology = cleaner(etym_nodes)
        #words = stripper(response.xpath("//span[contains(@class, 'hyphens-auto')]/text()").getall())
        #pos = stripper(response.xpath("//span[contains(@class, 'text-battleship-gray')]/text()").get())
        #etym_nodes = response.xpath("//section[contains(@class,'-mt-4')]/descendant::text()").getall()
        #etym_text = cleaner(etym_nodes)
    
        #for word in words:
            #if word:
               #yield {
                #"word": word,
                #"part_of_speech": pos,
                #"etymology" : etymology
               #}

#WE CHECK IF THE NEXT BUTTON IS ACTIVE TO STOP THE LOOP AT EXACTLY THE LAST PAGE
#MAY NEED MORE ROBUST LOGIC SINCE THE PAGINATION IN ETYMONLINE IS FUCKING JS (MAYBE PLAYWRIGHT MIGHT BE BETTER)
#FOR NOW WE JUST USE THIS INCREMENTAL APPROACH ON THE ETYMONLINE URL 
        next_button_active = response.xpath("//li[@data-slot='next' and not(@aria-disabled='true')]")
        if next_button_active:
            parsed_url = urlparse(response.url)
            query_params = parse_qs(parsed_url.query)
            try:
                current_page = int(query_params.get('page', ['1'])[0]) 
                next_page = current_page + 1
            except ValueError:
                self.logger.error(f"Could not parse page number from URL: {response.url}")
                return
            
            query_params['page'] = [str(next_page)]
            next_query = urlencode(query_params, doseq=True)
            next_url = urlunparse(parsed_url._replace(query=next_query))

            yield scrapy.Request(url=next_url, callback=self.parse)

        else:
            self.logger.info(f"Reached the last page: {response.url}.")    