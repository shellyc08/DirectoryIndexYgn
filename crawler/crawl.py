import scrapy
ascii = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
class BlogSpider(scrapy.Spider):
    name = 'BlogSpider'
    base = 'http://www.myanmaryellowpages.biz/web/categories/searchByName/'
    start = 'A'
    urls = []
    for i in ascii:
        urls.append(base+i)
    start_urls = urls
    def parse(self, response):

        category = response.css('#mobile-padding-top5 a::text').extract_first()
        if category:
            category = category.rstrip().strip('\n').strip()
        for product in response.css('div.ypg-content-color'):
            infos = product.css('ul.fa-ul li')
            value = []
            for info in infos:
                try:
                    temp = info.css('::text').extract_first().rstrip().strip().strip()
                    value.append(temp)
                except:
                    value.append('')
                    print('error')

            yield {
                'name': product.css('div.col-md-6 a::text').extract_first().rstrip().strip(),
                'category': category,
                'address': value[0],
                'contact': value[1],
                'email': value[2],
                'website': value[3]
                }
        next_pages = response.css('ul.category-list-style a ::attr(href)').extract()
        for next_page in next_pages:
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        pagination_next_page = response.css('ul.pagination li:last-child a::attr(href)').extract_first()
        print(pagination_next_page)
        if pagination_next_page:
            yield scrapy.Request((pagination_next_page), callback=self.parse)
