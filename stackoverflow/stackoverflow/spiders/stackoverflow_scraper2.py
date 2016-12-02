import scrapy
import json
# #Crawl Stackoverflow using Scrapy

class mySOSpider(scrapy.Spider):
    name = "stackoverflow2"

    def start_requests(self):
        with open("../output/linkstocrawl.json") as fp:
            urls = json.load(fp)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        foldername = "../output/temp/"
        f1 = open(foldername+"arraynames"+".txt", 'a')
        tempurl =  response.url.split("/")[-1]
        page = tempurl[0:tempurl.find('?')]
        f1.write("'" + page+"' ,")
        f1.close()
        questions = response.css('div.question-summary')
        finalres=[]
        for ques in questions:
            result={}
            result['source'] = "stackoverflow"
            result['url'] = "http://stackoverflow.com" + ques.xpath('div/h3/a/@href').extract()[0]
            result['question'] = ques.xpath('div/h3/a/text()').extract()[0]
            result['tags'] = ques.css('a.post-tag::text').extract()
            result['questionvotes'] = ques.css('div.votes span.vote-count-post strong::text').extract()[0]
            result['answers']=ques.css('div.status strong::text').extract()
            result['views']=ques.css('div.views::text').extract()[0]
            finalres.append(result)
        f = open(foldername+page+".json", 'w+')
        f.write( json.dumps(finalres, indent=4))