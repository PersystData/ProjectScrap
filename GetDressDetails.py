from bs4 import BeautifulSoup
import requests
import sqlite3
import json
        
    


class PageDetails:
    
    def __init__(self):
        self.soup = str()
        self.urls = 0     
        
    def get_urls(self,file_name):
        fh = open(file_name)
        self.urls = []
        for line in fh:
            line = line.strip()
            start = line.find("http")
            self.urls.append(line[start:])
        
    def get_soup(self, url):
        webpage = url
        try:
            user_agent = "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
            headers = {"User-Agent":user_agent}
            response = requests.get(webpage,headers = headers)
            self.soup = BeautifulSoup(response.text,"html.parser")
        except Exception as badEggs:
            print("Some Really Bad Eggs of type:", type(badEggs),badEggs)
        
    def get_cloth_description(self):
        tags = self.soup.find_all("ul","prod-main-wrapper")
        
        tag = tags[0]
        children = []
        for child in tag:
            children.append(child)
        children.pop()
        self.description = {}
        
        for label in children:
            tags = []
            for tag in label:
                tags.append(tag)
            description_key = tags[0].contents[0]
            description_value = tags[1].contents[0]
            self.description[description_key] = description_value
        if "Type" not in self.description.keys():
            self.description['Type'] = ""
        if "Wash Care" not in self.description.keys():
            self.description['Wash Care'] = ""
        if "Style" not in self.description.keys():
            self.description['Wash Care'] = ""
        if "SKU" not in self.description.keys():
            self.description['Wash Care'] = ""
        if "Length" not in self.description.keys():
            self.description['Wash Care'] = ""
        if "Color" not in self.description.keys():
            self.description['Wash Care'] = ""
        
        
    
    def get_other_details(self):
            self.details = dict()
            brand = self.soup.find("span","brand")
            brand_name = brand.string
            self.details['brand'] = brand_name
            price = self.soup.find("span","actual-price")
            price = price.string
            self.details["price"] = price
            title = self.soup.find("span","product-title")
            title = title.string
            self.details['title'] = title
            product_img_tags = self.soup.find_all("div","col-xs-12 col-sm-12 col-md-8 product-image")
            target_soup = BeautifulSoup(str(product_img_tags),"html.parser") 
            self.img_tags = target_soup.find_all("img")
            if len(self.img_tags) == 4:
                target_tag = self.img_tags[0]
                target_data = target_tag[u'data-img-config']
                target_dict = json.loads(target_data)
                base_path = target_dict['base_path']
                img = target_dict['768']
                img_url = base_path + img
                self.details['img_url'] = img_url
            else:
                self.details['img_url'] = " "
            
    def get_page_info(self):
        self.get_cloth_description()
        self.get_other_details()
        info = self.description
        info['details'] = self.details
        return info
            
        
        
if __name__ == "__main__":
    try:
        connection = sqlite3.connect("Dresses.db")
        cursor = connection.cursor()
    except Exception as BadEgg:
        print "Caught Some Really Bad Eggs of type", type(BadEgg)
    
    pages_info = []
    print "Successfully Connected"
    obj = PageDetails()
    obj.get_urls("urls.txt")
    count = 0
    for url in obj.urls:
        count += 1
        obj.get_soup(url)
        info = obj.get_page_info()
        print(info)
        pages_info.append(info)
        other_details = info['details']
        details = info['details']
        if 'Style' in info:
            st = info['Style']
        record = [details['brand'], details['title'], details['price'],details['img_url'],
                    info['SKU'], st, info['Color'], info['Type'],info['Wash Care'],url]
        try:            
            cursor.execute("INSERT INTO Dresses(Brand, Title, Price, Image,SKU, Style, Color, Type, WashCare,Url) VALUES(?,?,?,?,?,?,?,?,?,?)",record)
            connection.commit()
        except Exception as BadEgg:
            connection.close()
            print "Caught Some Really Bad Bad Eggs of type", type(BadEgg), BadEgg
            break
        print(count)
    connection.close()
#print(info)
