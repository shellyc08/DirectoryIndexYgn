#import re
#word1 = '\"North Dagon Township. \"'
#word1 = " ".join(re.findall("[a-zA-Z ]+", word1))
#print(word1)

import re
import sqliteMethods

def clean(word):
	word = " ".join(re.findall("[a-zA-Z0-9 ]+", word))
	word = word.strip().rstrip()
	return word

queries = sqliteMethods.Company.select();

for query in queries:
	cleaned_township = clean(query.TOWNSHIP)
	cleaned_name = clean(query.NAME)
	cleaned_category = clean(query.CATEGORY)
	query.SEARCH_NAME = cleaned_name
	query.SEARCH_CATEGORY = cleaned_category
	query.TOWNSHIP = cleaned_township
	query.save()