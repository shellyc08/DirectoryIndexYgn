from peewee import *
from sets import Set

db = SqliteDatabase('./sqlite.db')

def before_request_handler():
    db.connect()

def after_request_handler():
    db.close()

class Company(Model):
    NAME = CharField()
    CATEGORY = CharField()
    CONTACT = CharField()
    EMAIL = CharField()
    WEBSITE = CharField()
    STREET = CharField()
    TOWNSHIP = CharField()
    STATE = CharField()

    class Meta:
        database = db # This model uses the "sqlite.db" database.


def get_all_businesses(NAME=''):
    dictionary = {}
    dictionary = set()

    query = Company.select().where(Company.NAME.contains(NAME))
    results = get_result_array(query)
    print(len(results))
    if len(results) > 10:
        for result in results:
            dictionary.add(result['category'])
            if len(dictionary) >= 10:
                return "Too many results",dictionary
        return "Too many results",dictionary
    else:
        return results


def get_all_business(NAME='', CATEGORY = ''):
    query = Company.select().where(Company.CATEGORY.contains(CATEGORY) & Company.NAME.contains(NAME))
    result = get_result_array(query)
    print(len(result))
    if len(result) >10:
        return result[:10]
    return result


def get_list (TOWNSHIP='', CATEGORY=''):
    queries = Company.select().where(Company.TOWNSHIP.contains(TOWNSHIP) & Company.CATEGORY.contains(CATEGORY))
    result = get_result_array(queries)
    return result

def get_result_array(query):
    company_list = []
    
    for business in query:
        temp_dict = {}
        temp_dict['name'] = business.NAME
        temp_dict['category'] = business.CATEGORY
        temp_dict['email'] = business.EMAIL
        temp_dict['contact'] = business.CONTACT
        temp_dict['website'] = business.WEBSITE
        temp_dict['street'] = business.STREET
        temp_dict['township'] = business.TOWNSHIP
        temp_dict['state'] = business.STATE

        company_list.append(temp_dict)
    return company_list

#for business in get_all_businesses("Shwe Kaung"):
#	print business

#for business in get_all_business("Shwe Kaung","Restaurants"):
#    print business
# for business in get_list("botahtaung", "car"):
#     print business

	
