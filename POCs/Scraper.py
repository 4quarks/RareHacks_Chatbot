import googlesearch
import requests
from bs4 import BeautifulSoup, NavigableString
 

query = "melanoma treatment site:orpha.net"
https://www.orpha.net/consor/cgi-bin/Disease_Search_Simple.php?lng=EN


for url in googlesearch.search(query,  num=10,stop=10, pause=2): 
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    info_disease = dict()
    last_title_read=None
    is_reading_paragraph = False
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6","p"]):
        if tag.name=='p' and len(tag.attrs)==0 \
            and len(last_title_read)>0  and len (tag.get_text().strip())>15:
            if not is_reading_paragraph:
                info_disease[last_title_read]=list() 
            is_reading_paragraph=True
            info_disease[last_title_read].append(tag.get_text().strip())

        else:
            is_reading_paragraph=False
            last_title_read=tag.get_text().strip()

    print(info_disease)
    print("------------------------")
    # for num_tag in range(len(tags)):
    #     tags[num_tag]=tags[num_tag].next_element
    #     print (tags[num_tag])
    #     for elem in tags[num_tag].next_siblings:
    #         if elem.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
    #             break
    #         if elem.name =='p':
    #             print(elem)





    # num = 1
    # for i in soup.body:
    #     print (str(num)+" : "+str(i))
    #     num+=1