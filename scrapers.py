
"""
This module deals with the data collections side; 
it collects data from predefined resources, for each resource it first collect
the items urls, and the crawls the content of each item.

there is two main functions per resource :
1 - the urls collector :
    starting from a base_url (the resouce url), it collect the new added items urls 
    after a defined period of time.
    more details to follow ...

2 - the item crawler
    starting from a utl, the item crawler collects relevent details about an item
    and some meta-data about it, and returns a python dictionary with data,
    { "item_url" : "https://www.avito.ma/fr/sidi_moumen/ordinateurs_portables/Pc_portable_asus_mini__Comme_neuf_47817785.htm",
      "source": "Avito",
      "last_time_available": 02/11/2021 - 15:20,
      "price": 11000,
      "specs": {"producer":"HP",
                "model" : "EliteBook 14",
                "technical_specs :{"CPU":"core i5 10 gen",
                                   "RAM":" 8 GO DDR4",
                                   "Storage_1": "256 ssd nvme",
                                   "Storage_2": "1 TO HDD"}
                                   }
                "Weight": "2 kg"
                "Battery": "5 hours"                   
                }
        "city" : "Casablanca"
        }
3 - resources list
    -www.avito.ma/ordinateurs_portables
    -www.pcmaroc.ma
    -www.ultrapc.ma
    -www.zistore.ma
    -facebook_pages:
                    - elector_fatal
                    - electro_ordinateur
                    - electo_mourad
                    -..    


"""
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
from time import sleep

#from proxymanager import ProxyManager



session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'})
headers ={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Accept-Encoding": "gzip, deflate"
            }

proxies = {
            'http': 'http://148.251.249.240:3128',
            'https': 'http://1222.252.156.61:62694',
            }


#---------------------------------------- Avito scraper -----------------------------------------------------

def avito_urls_collector(base_url, **kwargs):

    """
    This function collects the links of available items on avito.ma, given some research parameters
    args :
    session :
    base_url:
    params :
    num_pages :

    """

    try:
        num_pages = kwargs['num_pages']
    except:
        num_pages = 1

    payload = {}
    links = []

    for page in range(1,(num_pages+1)):
        payload['o'] = page
        
        try:
            r = session.get(base_url,params = payload, headers=headers)
            time.sleep(3)
            soup = BeautifulSoup(r.content, "html.parser")
            items_posts = soup.find_all("div", class_ = "oan6tk-0 hEwuhz")

            for item in items_posts:
                item_link = item.find("a", class_ ="oan6tk-1 iZTmPK")["href"]
                links.append(item_link)
    
        except:
            print("problem with the request")


    return links




def avito_item_crawler(url):
    """
    Get the elements of a product
    title :
    description:
    price :
    localisation:
    time:

    """

    ##----------- To Do ------------------------
    """ use selenium/ requests html to show more description"""
    item ={}

    try :
        
        r = session.get(url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(r.content, "html.parser")

        try:
            title = soup.find("h1", class_="sc-1x0vz2r-0 iLDWht").text.strip() 
        except:
            title ="Not found"

        try:
            description = soup.find("p", class_="sc-ij98yj-0 jJVLjp").text.strip() #r.html.find("sc-ij98yj-0 ekgmnS").text      #sc-ij98yj-0 jJVLjp
        except:
            description ="Not found"
        
        try:
            price = soup.find("p", class_="sc-1x0vz2r-0 izYwIp").text.strip() 
            price = price[:-2]
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = int(price)

        except:
            price =None

        try:
            time_loc = soup.find_all("span", class_="sc-1x0vz2r-0 jWjZZH")
            localisation = time_loc[0].text.strip()
            last_seen_available = datetime.utcnow()
            # To do : Add  time processing feature

        except:
            localisation ="Not found"
            last_seen_available ="Not found"
        


        item = {
            '_id': form_id(url),
            'url': url,
            'title':title,
            'description':description,
            'price':price,
            'localisation':localisation,
            'last_seen_available':last_seen_available,
            'source' : 'avito'
        }

    except: 
        item = {
            '_id': form_id(url),
            'url': url,
            'title':None,
            'description':None,
            'price':None,
            'localisation':None,
            'last_seen_available':None,
            'source' : 'avito'
                }

    return item



#---------------------------------------- pcmacor scraper -----------------------------------------------------

def pcmaroc_urls_collector(base_url, **kwargs):
    """
    https://www.pcmaroc.com
    base_url = "https://pcmaroc.com/12-pc-portable#"
    """

    try:
        num_pages = kwargs['num_pages']
    except:
        num_pages = 1

  
    links = []

    for page in range(1,(num_pages+1)):
        base_url_page = base_url+"/page-" + str(page)
        
        try:
            r = session.get(base_url_page,headers=headers)
            time.sleep(3)
            soup = BeautifulSoup(r.content, "html.parser")
            items_posts = soup.find_all("div", class_ = "product-container") 
        
            for item in items_posts:
                try:
                    item_link = item.find("a", class_ ="product_img_link")["href"]
                    availability = item.find("span", class_ ="availability")
                    label = availability.find("span")["class"][0] # add text
                    if "success" in label:
                        links.append(item_link)
                except:
                    pass
    
        except:
            pass


    return links


def pcmaroc_item_crawler(url,city="CASABLANCA"):
    """
       some generic docstring

    """ 
    

    id = form_id(url)
    
    try :
        
        r = session.get(url, headers=headers)
        time.sleep(3)
        soup = BeautifulSoup(r.content, "html.parser")
        product_container = soup.find("div",class_= "pb-center-column col-xs-12 col-sm-6 col-md-7")

        try:
            title = product_container.find("h1", itemprop="name").text.strip()
        except:
            title =None

        try:
            description_div = product_container.find("div", id="short_description_content") #r.html.find("sc-ij98yj-0 ekgmnS").text      #
            description = description_div.find("p").get_text()
        except:
            description =None
        
        try:
            price = product_container.find("span", id="our_price_display").text.strip() # id ="our_price_display"
            price = price[:-5]
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = float(price)

        except:
            price =None

        localisation= city
        last_seen_available = datetime.utcnow()
        

        item = {
            '_id': id,
            'url': url,
            'title':title,
            'description':description,
            'price':price,
            'localisation':localisation,
            'last_seen_available': last_seen_available,
            'source' : 'pc maroc'
        }

    except: 
           item = {
            'url': url,
            'title':None,
            'description':None,
            'price':None,
            'localisation':None,
            'last_seen_available': None,
            'source' : 'pc maroc'
        }

    return item


#---------------------------------- ultra pc scraper -----------------------------------------
def ultra_pc_urls_collector(base_url,**kwargs):
    """
    https://www.ultrapc.ma
    """



    try:
        num_pages = kwargs['num_pages']
    except:
        num_pages = 1

    payload = {}
    links = []

    for page in range(1,(num_pages+1)):
        payload['page'] = page

        try:
            r = session.get(base_url,params = payload, headers=headers)
            time.sleep(3)
            soup = BeautifulSoup(r.content, "html.parser")
            items_posts = soup.find_all("div", class_ = "product-block clearfix")
        
            for item in items_posts:
                try:
                    item_link = item.find("a", class_ ="product-thumbnail img-thumbnail")["href"]
                    availability = item.find("div", class_ ="product-availability available font-weight-bold hidden-lg-up")
                    label = availability.get_text()
                    if "Produit" in label:
                        links.append(item_link)
                except:
                    pass
    
        except:
            pass


    return links



    pass

def ultra_pc_item_crawler(url,city= "CASABLANCA"):
    """
       some generic docstring

    """ 
    
    item ={}
    id = form_id(url)
    
    try :
        
        r = session.get(url, headers= headers)
        time.sleep(3)
        soup = BeautifulSoup(r.content, "html.parser")
        product_container_1 = soup.find("div",class_= "product-block-info col-lg-6")
        product_container_2 = soup.find("div",class_= "col-lg-6")

        try:
            title = product_container_1.find("h1", class_="product-title").text.strip()
        except:
            title =None

        try:
            description_div = soup.find("div", id="description") #r.html.find("sc-ij98yj-0 ekgmnS").text #
            description_p = description_div.find("p")
            description_span = description_div.find_all("span")
            description = []
            for span in description_span:
                s_text = span.text
                description.append(s_text)

            description = " ".join([x for x in description])
        except:
            description =None
        
        try:
            price_div = product_container_1.find("div", class_="current-price")# id ="our_price_display"
            price = price_div.find("span", class_="price").text
            price = price[:-7]
            price = re.sub(r"\s+", "", price, flags=re.UNICODE)
            price = float(price)

        except:
            price =None

        localisation= city
        last_seen_available = datetime.utcnow()
        
        item['_id']= id
        item["url"] = url
        item['title'] = title
        item['description'] = description
        item['price'] = price
        item['localisation'] = localisation
        item['last_seen_available'] = last_seen_available
        item['source'] = 'ultra pc'

    except: 

        item['_id']= '...'
        item["url"] = url
        item['title'] = None
        item['description'] = None
        item['price'] = None
        item['localisation'] = None
        item['time'] = None
        item['source'] = 'ultra pc'

    return item

    



#------------------------------------- Facebook pages scraper --------------------------------

def scrapp_facebook_page():
    """ scrap main laptops facebook pages to get the data"""
    pass

#------------------------------------ Utils --------------------------------------------------
def form_id(url):
    relevent_pattern = url.rsplit('/', 1)[-1]
    id = hash(relevent_pattern)

    return id


def urls_collector(source):

    if source == "pc maroc":
        base_url = "https://pcmaroc.com/12-pc-portable#"
        links = pcmaroc_urls_collector(base_url)

    elif source == "ultra pc":
        base_url = "https://www.ultrapc.ma/19-pc-portables"
        links = ultra_pc_urls_collector(base_url)

    elif source == "avito":
        base_url = "https://www.avito.ma/fr/maroc/ordinateurs_portables-%C3%A0_vendre"
        links = avito_urls_collector(base_url)

    else:
        return "please specify a source !"

    return links




def laptop_crawler(source,url):

    if source == "pc maroc":
        laptop = pcmaroc_item_crawler(url)

    elif source == "ultra pc":
        laptop = ultra_pc_item_crawler(url) 

    elif source == "avito":
        laptop = avito_item_crawler(url)
    else:
        return "please specify a source and a url !"

    return laptop