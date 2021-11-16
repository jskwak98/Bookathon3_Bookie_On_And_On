import scrapy
from os import path


class TeenSpider(scrapy.Spider):
    name = "teen"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.pages = []

    def start_requests(self):
        url_main = 'https://teen.munjang.or.kr/archives/category/old-excl'
        yield scrapy.Request(url=url_main, callback=self.parse_page)
        for page_num in range(2,40):
            url = url_main + '/page/' + str(page_num)
            yield scrapy.Request(url=url, callback=self.parse_page)
        for page in self.pages:
            yield scrapy.Request(url=page, callback=self.parse)

    def parse_page(self, response):
        for post in response.css('[class=post_title] a::attr(href)').extract():
            if 'archives' in post:
                self.pages.append(post)

    def parse(self, response):
        title = response.xpath('//header/h1/text()').get()
        category = response.xpath('//div[@class="entry-meta"]/span[@class="cat-links"]/a/text()').getall()
        passages = response.xpath('//div[@class="entry-content"]/p/text()').getall()
        if '수필' in category:
            new_title = title + ".txt"
            with open(path.join("/opt/ml/supil_myeongjeon", new_title), "w", encoding="utf-8") as f:
                f.writelines(passages)