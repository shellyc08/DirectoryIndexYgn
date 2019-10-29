#import scrapy
import requests
import pandas as pd

base ='http://mmrd.herokuapp.com/api/v3/search?latitude&category_unique_id=all&township_unique_id=all&longitude&query&page='

all_item_list = []

#page ends at 6009
for i in range(1,6010):
    url = base + str(i)
    r = requests.get(url)
    data = r.json()

    for dct in data:
	if i%500 == 0:
	    print 'crawled: ', i
	temp_emails = []
	for item in dct['emails']:
	    if item['email'] != "":
	        temp_emails.append(item['email'])
	dct['emails'] = ','.join(temp_emails)[:-1]

	temp_phones = []
	for item in dct['phones']:
	    if item['phone'] != "":
                temp_phones.append(item['phone'])
        dct['phones'] = ','.join(temp_phones)[:-1]

    all_item_list+= data

df = pd.DataFrame(all_item_list)
df.to_csv('crawl_data.csv', encoding='utf-8')
'''
class BlogSpider(scrapy.Spider):
    name = 'BlogSpider'
    base ='http://mmrd.herokuapp.com/api/v3/search?latitude&category_unique_id=all&township_unique_id=all&longitude&query&page=' 
    urls = []
    #page ends at 6009
    for i in range(1,2):
	urls.append(base+str(i))
    start_urls = urls

    def parse(self, response):
	print response
	filename = 'temp_crawl.txt'

	with open(filename, 'wb') as f:
	    f.write(response.body)	
'''
