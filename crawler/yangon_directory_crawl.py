import scrapy
ascii = 'abcdefghijklmnopqrstuvwxyz'
#ascii = 'r'
class BlogSpider(scrapy.Spider):
    name = 'BlogSpider'
    base = 'http://www.yangondirectory.com/en/categories-index/list-alpha/'
    start = 'a'
    urls = []
    for i in ascii:
        urls.append(base+i+'.html')
    start_urls = urls
    def parse(self, response):
        
        category = response.css('.col-lg-5.col-md-5 p::text').extract_first()
        name = response.css('.digital-address-heading::text').extract_first()
        address = response.css('.address-list label::text').extract()
        if(address):
            street = address[0]
            township = address[1]
            state = address[2]
        phone = response.css('.show-tel a::attr(href)').extract()
        if name:
            yield {
                    'name': name.rstrip().strip(),
                    'category': category,
                    'street': street.rstrip().strip(),
                    'township': township.rstrip().strip(),
                    'state': state.rstrip().strip(),
                    'contact': phone,
                    }

        next_pages = response.css('.category.col-md-4.col-sm-6.col-xs-12 a::attr(href)').extract()
        for next_page in next_pages:
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

        pagination_next_page = response.css('.pagination-list a[title=Next]::attr(href)').extract_first()
        #print(pagination_next_page)
        if(pagination_next_page and pagination_next_page != "/en/categories-ind"):
            yield scrapy.Request(response.urljoin(pagination_next_page), callback=self.parse)

        single_pages = response.css('.listing-summary a.first-feature-tag-btn::attr(href)').extract()
        #print(single_pages)
        for single_page in single_pages:
         #   print(single_page)
            if single_page:
                yield scrapy.Request(response.urljoin(single_page), callback = self.parse)
