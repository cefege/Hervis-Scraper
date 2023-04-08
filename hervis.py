from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re

def crawler(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        # Open new page
        page = context.new_page()

        # Go to Hervis
        page.goto(url, wait_until="networkidle", timeout=0)
        #time.sleep(10)
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        return soup, url


def extract_data(soup, url):
    #Elements
    title = 'n/a'
    header_1 = 'n/a'
    page_type = 'n/a'
    description_word_count = 0
    description_links = 0
    faq_exists = False
    products_count = 0
    #url = 'n/a'
    cannonical_url = 'n/a'
    facets = 'n/a'
    breadcrumbs = 'n/a'

    #Check page type
    try:
        if '/c/' in url:
            page_type = 'category'
        # elif ...
        #     page_type = 'product'
    except:
        pass

    #Grab Page Title:
    try:
        _title_extract = str(soup.find('title').get_text())
        _title_extract = _title_extract.strip()
        title =_title_extract
    except:
        pass

    #Grab Header 1:
    try:
        _header_extract = soup.select('.breadcrumb__title-text')[0].get_text()
        header_1 = _header_extract.strip()
    except:
        pass

    #Grab description + faq word count

    # NOW WORKING
    try:
        if "category" in page_type:
            description_html = soup.select('.blured-desc')
        if 'product' in page_type:
            description_html = soup.select('.blured-specs')
        #Convert list to string
        description_html = description_html[0]

        links_count = len(description_html.findAll('a'))
        description_links = links_count

        word_list = description_html.get_text().split()
        word_count = len(word_list)

        description_word_count = word_count

    #Number of words in description and FAQ  

    except:
        pass

    #Check if FAQ exist

    # Hervis does not support FAQ Schema, NOT WOKRING
    try:
        len(soup.find("div", {"itemtype": "https://schema.org/Question"}))
        faq_exists = True

    except:
        pass

    #Extract cannonical URL if it exists
    try:
        cannonical_url = soup.find("link", {"rel": "canonical"})['href']
    except:
        pass

    #Extract number of products
    try:
        if "category" in page_type:
            #Extract only number from text
            x = soup.select('.f-size--text-1')
            x = x[0].get_text()
            x = x.split(' ')[0]
            x = x.replace('(','')

            #Pass to df
            products_count = x
        
        if "product" in page_type:
            products_count = 1
    except:
        pass
    
    # Extract breadcrumbs
    try:
        breadcrumbs = []
        _breadcrumbs = soup.select('.breadcrumb__nav-item--category a',string=re.compile('/shop/'))
        for brd in _breadcrumbs:
            brd = brd.get('href')
            if brd != None:
                breadcrumbs.append('https://www.hervis.ro'+brd)

        if len(breadcrumbs) == 0:
            breadcrumbs = 'n/a'

        else:
            breadcrumbs =  breadcrumbs[-1]

        
    except:
        pass
    

      #Extract facets
    try:
        facets_list = []
        _facets_extract = soup.select(".facet__checkbox-label")
        for _facet in _facets_extract:
            _facet =  _facet.get_text()
            _facet = _facet.split('(')[0]
            _facet = _facet.strip()
            facets_list.append(_facet)

        facets = ', '.join(facets_list)
    
    except:
        pass  

    df = pd.DataFrame({ 'Meta Title': title,
                        'H1': header_1,
                        'Tip Pagina':page_type,
                        'Cuvinte Descriere': description_word_count,
                        'Linkuri Interne Descriere': description_links,
                        'Exista FAQ': faq_exists,
                        'Numar Produse': products_count,
                        'URL': url,
                        'URL Cannonical': cannonical_url,
                        'breadcrumbs': breadcrumbs,
                        'Facets': facets

                        }, 
                        index=[0])
    
    csv_path = Path('hervis/hervis.csv')

    if csv_path.is_file():
        df.to_csv(csv_path, mode='a', header=False, index=False, sep='\t')
    else:
        df.to_csv(csv_path, mode='w', header=True, index=False, sep='\t')


# ### Extracts products list function
# def extract_product_list(soup, url):
#     #Extract product list
#     product_list = soup.select('.picture')
#     product_list = list(set([x.find('a')['href'] for x in product_list]))
#     product_list = ['https://www.hervis.ro/' + x for x in product_list]
#     print(product_list[0])



url_list = pd.read_csv('hervis/url_list.csv').values.tolist()

## Extract normal data
for url in tqdm(url_list):
    to_extract = crawler(url[0])
    extract_data(to_extract[0], to_extract[1])


