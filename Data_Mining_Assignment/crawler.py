import requests
from bs4 import BeautifulSoup
import time
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f_dm = open('data_mining.csv', 'a')
data_writer = csv.writer(f_dm, delimiter="\t")
column_fields = ['conference_acronym','conference_name','conference_location']
data_writer.writerow(column_fields)

def data_from_url(target_url):
    #page number range
    for page_num in range(1,21):
        #temporary url
        turl = target_url
        #appending page number
        turl+=str(page_num)
        #HTTP request
        req_1 = requests.get(turl)
        #soupify
        soup_1 = BeautifulSoup(req_1.content, "lxml")
        links = soup_1.find_all("a")
        useful_links = []
        for link in links:
            if "/cfp/servlet/event.showcfp" in link.get("href"):
                useful_links.append("http://www.wikicfp.com/" + str(link.get("href")))
        #list of list
        data = []
        for url in useful_links:
            req_2 = requests.get(url)
            soup_2 = BeautifulSoup(req_2.content, "lxml")
            conf =  soup_2.find_all("title")[0].text
            info = conf.split(':',1)
            table_data = soup_2.find_all("table", {"class": "gglu"})
            req_item = []
            for item in table_data:
                req_item.append(item.find_all("td", {"align" : "center"}))
            info.append(req_item[0][1].text)
            data.append(info)
            #add delay for crawling
            time.sleep(10)
        #writing all the 20 rows of data
        for row in data:
            try:
                #csv writer function
                data_writer.writerow(row)
            except:
                pass
        #add delay for crawling
        time.sleep(10)
    return;

#crawling for data mining conferences
url_dm = "http://www.wikicfp.com/cfp/call?conference=data%20mining&page="
data_from_url(url_dm)

#crawling for databases conferences
url_db = "http://www.wikicfp.com/cfp/call?conference=databases&page="
data_from_url(url_db)

#crawling for artificical intelligence conferences
url_ai = "http://www.wikicfp.com/cfp/call?conference=artificial%20intelligence&page="
data_from_url(url_ai)

#crawling for machine learning conferences
url_ml = "http://www.wikicfp.com/cfp/call?conference=machine%20learning&page="
data_from_url(url_ml)
f_dm.close()