#!/usr/bin/python

import MySQLdb

def get_all_businesses(NAME='',TOWNSHIP=''):
    db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="yangonthar_db")
    cur = db.cursor()
    dictionary = []
    try:
        queryTownship = ''
        queryParameter = (NAME,NAME,NAME,NAME,NAME)
        if TOWNSHIP != '':
            queryTownship = 'and soundex(township) = soundex(%s) '
            queryParameter = (NAME,NAME,NAME,NAME,NAME,TOWNSHIP)
        cur.execute("select distinct businessname, street, township, contact, category, MATCH (businessname,category) " + 
        "AGAINST (%s IN NATURAL LANGUAGE MODE) as score from yangon_thar where ((MATCH (businessname,category) " +
        "AGAINST (%s IN NATURAL LANGUAGE MODE)>4  and %s sounds like substring(businessname,1,length(%s))) "+
        "OR businessname = %s )" + queryTownship +  " order by score desc;",queryParameter)    
        results = cur.fetchall()

        trimmedName = NAME.split(" ")
        trimmedName.pop()

        if len(results) == 0 and len(trimmedName):	
            while len(results)<10 and len(trimmedName):
                nametrim = trimmedName[0]
                for i in range(1,len(trimmedName)):
                    nametrim = nametrim + " " + trimmedName[i]
                queryTrimmedParameter = (nametrim, nametrim, nametrim, nametrim, nametrim)
                if TOWNSHIP != '':
                    queryTrimmedParameter = (nametrim, nametrim, nametrim, nametrim, nametrim,TOWNSHIP)
                cur.execute("select distinct businessname, street, township, contact, category, MATCH (businessname,category) " + 
                "AGAINST (%s IN NATURAL LANGUAGE MODE) as score from yangon_thar where ((MATCH (businessname,category) " +
                "AGAINST (%s IN NATURAL LANGUAGE MODE)>4  and %s sounds like substring(businessname,1,length(%s))) " + 
                "OR businessname = %s) "+ queryTownship +" order by score desc;",queryTrimmedParameter)
            
                if len(results) == 0:
                    results = cur.fetchall()
                else:
                    results = tuple(list(results) + list(cur.fetchall()))
                trimmedName.pop()
    
        if len(results)==0:
            queryNoSpaceParameter = (NAME,NAME,NAME+'%')
            if TOWNSHIP != '':
                queryNoSpaceParameter = (NAME,NAME, NAME+'%', TOWNSHIP)
            cur.execute("select distinct businessname, street, township, contact, category, MATCH(TRIMMEDNAME) AGAINST (%s in NATURAL language mode) AS score"+
            " from yangon_thar where ((MATCH (trimmedname) AGAINST (%s IN NATURAL LANGUAGE MODE)>4)"+ " or trimmedname like  %s) "+ queryTownship +" order by score desc;", queryNoSpaceParameter)
            results = cur.fetchall()	
            
        count = 1
        for result in results:
            dicty = {}
            dicty['businessName'] = result[0].strip() + " (" + result[4].strip() + ")"
            dicty['street'] = result[1].strip()
            dicty['township'] = result[2].strip()
            dicty['contact'] = result[3].strip()
            dictionary.append(dicty)

            count = count + 1
            if count > 10:
                break
        return dictionary
    except MySQLdb.Error, e:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        return []
    finally:
        cur.close()
        db.close()


def get_list(TOWNSHIP='', CATEGORY=''):
    db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="yangonthar_db")
    cur = db.cursor()
    dictionary = []
    try:
        cur.execute("select distinct businessname, street, township, contact, MATCH (businessName,category) " +
        "AGAINST (%s IN NATURAL language mode) as score from yangon_thar where (MATCH (category) " +
        "AGAINST (%s IN boolean MODE) or MATCH (businessName,category) " + 
        "AGAINST (%s IN NATURAL language mode)>4 ) and soundex(township) = soundex(%s) order by score desc;", 
        (CATEGORY, CATEGORY+'*', CATEGORY, TOWNSHIP))
        results = cur.fetchall()

        if len(results) == 0:
            print "Our first suggestions:"
            cur.execute("select distinct businessname, street, township, contact, MATCH (businessName,category) " +
            "AGAINST (%s IN NATURAL language mode) as score from yangon_thar where (MATCH (category) " +
            "AGAINST (%s IN boolean MODE) or MATCH (businessName,category) " + 
            "AGAINST (%s IN NATURAL language mode with query expansion)>20 ) and soundex(township) = soundex(%s) order by score desc;", 
            (CATEGORY, CATEGORY+'*', CATEGORY, TOWNSHIP))
            results = cur.fetchall()

            if len(results) == 0:
                print "Our second suggestions:"
                cur.execute("select distinct businessname, street, township, contact, MATCH (businessName,category) " +
                "AGAINST (%s IN NATURAL language mode) as score from yangon_thar where (MATCH (category) " +
                "AGAINST (%s IN boolean MODE) or MATCH (businessName,category) " + 
                "AGAINST (%s IN NATURAL language mode with query expansion)>10 ) and soundex(township) = soundex(%s) order by score desc;", 
                (CATEGORY, CATEGORY+'*', CATEGORY, TOWNSHIP))
                results = cur.fetchall()
        count = 1
        for result in results:
            dicty = {}
            dicty['businessName'] = result[0].strip()
            dicty['street'] = result[1].strip()
            dicty['township'] = result[2].strip()
            dicty['contact'] = result[3].strip()
            dictionary.append(dicty)
            count = count + 1
            if count > 10:
                break
        return dictionary
    except MySQLdb.Error, e:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        return []
    finally:
        cur.close()
        db.close()

print get_all_businesses(NAME='shwe pu zun', TOWNSHIP='')
