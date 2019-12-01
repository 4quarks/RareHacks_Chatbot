import urllib.request
from bs4 import BeautifulSoup
import string
from selenium import webdriver
from SQLconnection import SqlConnection
import time
import xlrd
import os
import platform
from selenium.webdriver.common.keys import Keys
import time
import requests
import types
from multiprocessing import Process
import pandas as pd


class Illness:
    def __init__(self):
        self.name=None
        self.brief=None
        self.text=None
        self.id=0
        self.reference=None
        self.entity=None
        self.keywords=None

    def scrapAllRareDiseasesId(self):
        scrap_names_and_orpha=True
        scrap_cie10=True
        if scrap_names_and_orpha:
            letters=string.ascii_uppercase
            for letter in letters:
                # print(letter,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                url = "https://www.orpha.net/consor4.01/www/cgi-bin/Disease_Search_List.php?lng=EN&TAG="+str(letter)
                fp = urllib.request.urlopen(url)
                mybytes = fp.read()
                html = mybytes.decode("utf-8", errors='ignore')
                fp.close()
                soup = BeautifulSoup(html, "html.parser")
                box=soup.findAll('div',{'id':'result-box'})
                lines=box[0].findAll('li')
                for line in lines:
                        illness = Illness()
                        try:
                            illness.name=line.get_text()
                            illness.id=str(line).split("Expert=")[1].split("\">")[0]
                            sql = SqlConnection()
                            sql.insert("diseases_id", ["name", "ORPHA"], [illness.name, int(illness.id)])
                            print(illness.name, illness.id)
                            # url = "https://www.orpha.net/consor4.01/www/cgi-bin/OC_Exp.php?lng=EN&Expert="+str(illness.id)
                            # fp = urllib.request.urlopen(url)
                            # mybytes = fp.read()
                            # html = mybytes.decode("utf-8",errors='ignore')
                            # fp.close()
                            # soup = BeautifulSoup(html,"html.parser")
                            # for script in soup(["script", "style"]):
                            #     script.extract()    # rip it out
                            # # get text
                            # info=soup.findAll("div",{"class":"articleInfo"})[0]
                            # text = info.get_text()
                            # # break into lines and remove leading and trailing space on each
                            # lines = (line.strip() for line in text.splitlines())
                            # # break multi-headlines into a line each
                            # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                            # # drop blank lines
                            # illness.text = '\n'.join(chunk for chunk in chunks if chunk)
                            # illness.reference =url
                            # illness.brief=soup.findAll('div',{'class':'definition'})[0].get_text().split("Disease definition")[1].strip()
                            # print(len(illness.name), len(illness.id), len(illness.brief),len(illness.text),len(illness.reference))
                            # sql = SqlConnection()
                            # sql.insert("diseases", ["illness_name", "id", "brief", "full_text", "reference"], [illness.name, int(illness.id), illness.brief, illness.text, illness.reference])
                        except:
                            pass
        if scrap_cie10:
            self.chrome_options = webdriver.ChromeOptions()
            self.browser = self.connectionChrome(self.chrome_options)
            url="https://webs.somsns.es/cnr/Visor_EERR.htm"
            self.browser.get(url)
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            rows=soup.findAll('tr')
            for row in rows:
                try:
                    if len(row.findAll('a',{'target':'orpha'}))>0:
                        orpha=row.findAll('a',{'target':'orpha'})[0].get_text()
                        cie10=row.findAll('a',{'target':'cie10mc'})[0].get_text()
                        if cie10 and " " in cie10:
                            cie10=cie10.strip().replace("   ",";").replace("  ",";").replace(" ",";")
                        if orpha and cie10:
                            sql = SqlConnection()
                            print(orpha, cie10)
                            sql_statement = "update diseases_id set CIE10=" + "'"+cie10+ "'" + " where ORPHA=" + str(int(orpha))
                            sql.update(sql_statement)
                except:
                    pass
        self.browser.close()

    def scrapDiseases(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.browser = self.connectionChrome(self.chrome_options)
        #here you can write the illness you want to get info:
        illness_to_search=['melanoma']
        for illness in illness_to_search:
            url="https://www.orpha.net/consor/cgi-bin/Disease_Search_Simple.php?lng=EN"
            self.browser.get(url)
            time.sleep(1)
            label_search=['input','type','text']
            self.writeInBox(illness, label_search)
            self.clickOnButton(['button','type','submit'])
            # self.scrollDown()
            time.sleep(1)
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            illness_list = []
            orpha_list=[]
            elements=soup.findAll('div',{"class":"oneResult"})
            for element in elements:
                illness = Illness()
                illness.name=element.findAll('a')[0].get_text().strip()
                illness_list.append(illness.name)
                illness.id=element.findAll('h4')[0].get_text().split(" ")[0].split(":")[1].split("  ")[0].strip()
                orpha_list.append(illness.id)
                illness.reference="https://www.orpha.net/consor4.01/www/cgi-bin/OC_Exp.php?lng=EN&Expert="+str(illness.id)
                # print(illness.reference)
                fp = urllib.request.urlopen(illness.reference)
                mybytes = fp.read()
                html = mybytes.decode("utf-8", errors='ignore')
                fp.close()
                soup = BeautifulSoup(html, 'html.parser')
                illness.brief=soup.findAll("section")[0].get_text().strip()
                sql = SqlConnection()
                sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, illness.brief,"divulgation", "Melanoma", illness.reference,illness.id])
                article=soup.findAll('div',{'class':'articleInfo'})[0]
                if article:
                    subtitles=article.findAll("h3")
                    subarticles=article.findAll("p")
                    for index in range(len(subtitles)):
                        type=subtitles[index].get_text().strip()
                        text=subarticles[index].get_text().strip()
                        if type=="Epidemiology" or type=="Clinical description":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference", "ORPHA"], [illness.name, text,"definition", "Melanoma", illness.reference,illness.id])
                            pass
                        if type=="Etiology":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, text,"risk_factor", "Melanoma", illness.reference,illness.id])
                            pass
                        if type=="Diagnostic methods":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, text,"diagnostic_test", "Melanoma", illness.reference,illness.id])
                            pass
                        if type=="Genetic counselling":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, text,"genetic", "Melanoma", illness.reference,illness.id])
                            pass
                        if type=="Differential diagnosis":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, text,"diagnostic", "Melanoma", illness.reference,illness.id])
                            pass
                        if type=="Management and treatment":
                            sql = SqlConnection()
                            sql.insert("diseases", ["name", "text","entity","family","reference","ORPHA"], [illness.name, text,"treatment", "Melanoma", illness.reference])
                            pass
                        if type=="Prognosis":
                            sql.insert("diseases", ["name", "text","entity","family","reference"], [illness.name, text,"prognosis", "Melanoma", illness.reference])
                            pass
            time.sleep(1)
            illness.reference="https://www.orpha.net/consor/cgi-bin/Clinics.php?lng=EN"
            for ill in illness_list:
                illness.name=ill
                self.browser.get(illness.reference)
                time.sleep(1)
                label_search = ['input', 'type', 'text']
                self.writeInBox(ill, label_search)
                self.clickOnButton(['button', 'type', 'submit'])
                # self.scrollDown()
                time.sleep(1)
                self.clickOnXPath("//*[@id=\"ContentType\"]/div[2]/div/div[1]/h4/a")
                time.sleep(2)
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                centers=soup.findAll('div',{'class':'oneResult advancedRes'})
                centers_string=None
                centers_to_send=[]
                if centers:
                    for center in centers:
                        country=center.findAll('strong')[0].get_text().strip()
                        # print(country)
                        center_label=center.findAll('h4')[0]
                        center_name=center_label.findAll('div')[0].get_text().strip()
                        # print(center_name)
                        if centers_string:
                            centers_string = centers_string+";"+ country + ";" + center_name
                        else:
                            centers_string =country+";"+center_name
                sql = SqlConnection()
                sql.insert("diseases", ["name", "text", "entity", "family", "reference"],[illness.name, centers_string, "expert_centers", "Melanoma", illness.reference])
            illness.reference="https://www.orpha.net/consor/cgi-bin/Drugs.php?lng=EN"
            for indexation,ill in enumerate(illness_list):
                try:
                    illness.name=ill
                    illness.id=orpha_list[indexation]
                    self.browser.get(illness.reference)
                    time.sleep(1)
                    label_search = ['input', 'type', 'text']
                    self.writeInBox(ill, label_search)
                    self.clickOnButton(['button', 'type', 'submit'])
                    # self.scrollDown()
                    time.sleep(1)
                    self.clickOnXPath("//*[@id=\"ContentType\"]/div[2]/div/div[1]/h4/a")
                    time.sleep(2)
                    soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    results=soup.findAll('div',{'class':'blockResults'})
                    treatments=results[0].findAll('li')
                    treatment_string=None
                    for element in treatments:
                        treatment=element.get_text().strip().lower()
                        if treatment:
                            if treatment_string:
                                treatment_string=treatment_string+treatment+";"
                            else:
                                treatment_string=treatment+";"
                    if treatment_string:
                        sql = SqlConnection()
                        sql.insert("diseases", ["name", "text", "entity", "family", "reference"],[illness.name, treatment_string, "treatment", "Melanoma", illness.reference])
                except:
                    pass

    def scrapDataExcel(self):
        illness=Illness()
        df = pd.read_excel(r'C:\Users\David\Desktop\Hackaton.xlsx')
        illness_list=list(df)
        illness.reference="https://www.ncbi.nlm.nih.gov/books/NBK65895/"
        for index in range(len(illness_list)-1):
            illness.name=illness_list[index+1]
            for index_table in range(df.shape[0]):
                type=df.iloc[index_table,0]
                message=df.iloc[index_table,1]
                # print(type,":",message)
                if type and message:
                    sql = SqlConnection()
                    sql.insert("diseases", ["name", "text", "entity", "reference"],[illness.name, message, type, illness.reference])

        # illness.name="Melanoma"
        # illness.name=df.iloc[0,1]
        # print(illness.name)

    def clickOnXPath(self, x_path):
        element = self.browser.find_element_by_xpath(x_path)
        # print (element.location_once_scrolled_into_view)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        self.browser.execute_script("arguments[0].click();", element)

    def writeInBox(self, message, label_message):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        box = self.getScrapData(soup, label_message)
        if box:
            x_path = self.getXPathFromBeautifulSoupComponent(box[0])
            element = self.browser.find_element_by_xpath(x_path)
            if element:
                self.browser.execute_script("arguments[0].value = '{}';".format(message), element)

    def getScrapData(self, place_to_search, label_list):
        if len(label_list) == 3:
            scraped_data = place_to_search.findAll(label_list[0], {label_list[1]: label_list[2]})
        elif len(label_list) == 2:
            first_value = place_to_search.findAll(label_list[0][0], {label_list[0][1]: label_list[0][2]})
            second_value = place_to_search.findAll(label_list[1][0], {label_list[1][1]: label_list[1][2]})
            scraped_data = []
            if first_value:
                scraped_data.append(first_value[0])
            if second_value:
                scraped_data.append(second_value[0])
        elif len(label_list) == 1:
            scraped_data = place_to_search.select(label_list[0])
        else:
            scraped_data = None
        return scraped_data

    def getXPathFromBeautifulSoupComponent(self, element):

        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name
                if siblings == [child] else
                '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    def clickOnButton(self, label_to_click, browser=False):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        if len(label_to_click) > 1:
            button = soup.findAll(label_to_click[0], {label_to_click[1]: label_to_click[2]})
            if len(button) > 0:
                x_path = self.getXPathFromBeautifulSoupComponent(button[0])
                if browser:
                    element = self.browser.find_element_by_xpath(x_path)
                    element.click()
                else:
                    self.clickOnXPath(x_path)
            # else:
            #     print("Error de scrapeo al clicar en ", self.self.bookmaker.name)
        elif browser:
            self.browser.find_element_by_xpath(label_to_click[0]).click()

    def scrollDown(self):
        for num_press in range(60):
            self.browser.find_element_by_css_selector('body').send_keys(Keys.DOWN)

    def connectionChrome(self, chrome_options=webdriver.ChromeOptions()):
        browser = webdriver.Chrome("chromedriver.exe", options=chrome_options)

        return browser

illness=Illness()
# illness.scrapAllRareDiseasesId()
illness.scrapDiseases()
illness.scrapDataExcel()

