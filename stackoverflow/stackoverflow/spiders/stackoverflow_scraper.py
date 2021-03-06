import scrapy
import json
# #Crawl Stackoverflow using Scrapy

class mySOSpider(scrapy.Spider):
    name = "stackoverflow"

    def start_requests(self):
        urls = [
         'http://stackoverflow.com/?tab=hot',
         'http://stackoverflow.com/?tab=featured',
         'http://stackoverflow.com/?tab=interesting',
         'http://stackoverflow.com/?tab=week',
         'http://stackoverflow.com/?tab=month',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("=")[-1]
        questions = response.css('div.question-summary')
        finalres=[]
        for ques in questions:
            result={}
            result['source'] = "stackoverflow"
            result['url'] = "http://stackoverflow.com" + ques.xpath('div/h3/a/@href').extract()[0]
            result['question'] = ques.xpath('div/h3/a/text()').extract()[0]
            result['tags'] = ques.css('a.post-tag::text').extract()
            ratings = ques.css('div.mini-counts').css('span::text').extract()
            result['questionvotes'] = ratings[0]
            result['answers']=ratings[1]
            result['views']=ratings[2]
            finalres.append(result)
        foldername = "../output/"
        f = open(foldername+page+".json", 'w+')
        f.write( json.dumps(finalres, indent=4))