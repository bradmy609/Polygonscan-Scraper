from scraper import request_content, set_soup, get_page_links, set_next_url, local
from restructureData import set_dict, update_dict, restructure_dict, rearrange_dict, create_df
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def scrape_data(url):
    res, date_list, time_list = request_content(url)
    soup, headers, rows, contract_list = set_soup(res)
    page_links = get_page_links(soup)
    
    keys = page_links.keys()
      
    if 'Next' in keys:
        next_url = set_next_url(page_links['Next'])
    else:
        next_url = None
        print('End of pages, no next page link found within page_links!')
    
    return rows, date_list, time_list, contract_list, next_url

def build_d(rows, date_list, time_list, contract_list):
    
    d = set_dict(rows)

    restructure_dict(d)
    
    update_dict(d)

    d = rearrange_dict(d, date_list, time_list, contract_list)
    
    return d

def get_polygonscan_tokens():
    count = 0
    base_url = 'https://polygonscan.com/tokens'
    
    print('Starting query loop, initial query destination:')
    print(base_url)
    
    while base_url:
        rows, date_list, time_list, contract_list, next_url = scrape_data(base_url)
        d = build_d(rows, date_list, time_list, contract_list)
        
        if count == 0:
            df = create_df(d)
        elif count > 0:
            ndf = create_df(d)
            df = df.append(ndf)
            
        base_url = next_url
        print('Querying next URL:')
        print(base_url)
        count += 1
    
    return df