import requests
from bs4 import BeautifulSoup
from datetime import datetime

def request_content(url):
    res = requests.get(url).content
    f = datetime.now()
    
    # Extracts date and time from the datetime object
    time = f.strftime('%H:%M:%S')
    date = f.strftime('%Y-%m-%d')
    time_list = []
    date_list = []

    temp_soup = BeautifulSoup(res, 'html.parser')
    table_rows = temp_soup.find_all('tr')
    # Sets a list of 50 of current date, and a list of 50 of current time to use as a column in the dataframe
    for i in range(len(table_rows)-1):
        time_list.append(time)
        date_list.append(date)
        
    return res, date_list, time_list

def set_soup(res):
    # assign BS4 Soup object
    soup = BeautifulSoup(res, 'html.parser')
    # extracts table headers and table rows from the BS4 object
    headers = soup.find_all('th')
    rows = soup.find_all('tr')
    
    link_list = []
    for child in rows[1:]:
        if(child.a):
            link_list.append(child.a['href'])

    contract_list = []
    for item in link_list:
        contract_link = 'https://polygonscan.com/tokens' + item
        contract_list.append(contract_link)
        
    
    return soup, headers, rows, contract_list

def get_page_links(soup):
    a = soup.find_all('a')
    page_links = {}
    for link in a[90:]:
        if 'Next' in link.text or 'Last' in link.text or 'Previous' in link.text or 'First' in link.text:
            page_links[link.text.strip()] = link['href']
            
    return page_links

def set_next_url(relative_path):
    url = 'https://polygonscan.com/'
    nxt = url + relative_path
    return nxt
