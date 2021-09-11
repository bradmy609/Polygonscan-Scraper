import pandas as pd
import scraper as scraper

def set_dict(rows):
    d = {
    'rank': [], 
    'tokens': [], 
    'prices': [], 
    'change%': [],
    'volume24h': [], 
    'market_cap': [], 
    'holders': []
    }
    
    # The following commented out section is the start of a strategy for definining
    # the dictionary keys passively by looping through soup object. To improve the file
    # finish that method when you are done being lazy.
    '''
    p = {}
    
    for lst in headers_list:
        p[lst[0]] = []
    '''
    
    for row in rows[1:]:
        current = row.td
        try:
            for key, value in d.items():
                value.append(current.text.strip())
                current = current.next_sibling
        except:
            continue
            
    return d

# Extracts 'tokens' column values from d, restructures them into multiple key: value pairs,
# then adds them all back to the original dictionary. Deletes tokens. Returns nothing.
def restructure_dict(d):
    d['token_name'] = []
    d['symbol'] = []

    for desc in d['tokens']:
        start = desc.index('(')
        if start == 0:
            desc = desc[6:]
        desc = desc.replace('(PoS)', '')
        first = desc.index('(')
        last = desc.index(')')
        d['token_name'].append(desc[:first - 1])
        d['symbol'].append(desc[first + 1:last])
        #d['description'].append(desc[last+1:])
        
    d.pop('tokens')

# Function to reformat prices from the original dictionary. This function makes the next function more readable.
def strip_string_num(string):
    to_remove = [',', '%', '$']
    for i in range(len(to_remove)):
        try:
            string = string.replace(to_remove[i], '')
        except:
            continue
            
    index = string.index('.')
    second = string[index+1:].index('.')
    third = string.index('BTC')
    fourth = string.index('MATIC')
                               
    usd = float(string[:index+second])
    btc = string[index+second:third].strip()
    matic = float(string[third+3:fourth].strip())
    
    return usd, btc, matic

# update_dict function will remove unwanted symbols like %, $, ',', from the values of the original dict. It will then replace them with the new values.
def update_dict(d):
    td = {'rank': [], 'mcap': [], 'vol': [], 'change%': [], 'usd': [], 'btc': [], 'matic': [] }
    
    for key, val in d.items():
        for i in range(len(val)):
            if key == 'rank':
                try:
                    td['rank'].append(int(val[i]))
                except:
                    td['rank'].append(val[i])
            elif key == 'market_cap' or key == 'volume24h':
                mcap = val[i][1:].replace(',', '')
                p = mcap.split('.')
                if key =='market_cap':
                    try:
                        td['mcap'].append(int(p[0]))
                    except:
                        td['mcap'].append(p[0])
                elif key == 'volume24h':
                    try:
                        td['vol'].append(int(p[0]))
                    except:
                        td['vol'].append(p[0])
            elif key == 'change%':
                td['change%'].append(val[i].replace('%', ''))

    for price in d['prices']:
        usd, btc, matic = strip_string_num(price)

        td['usd'].append(usd)
        td['btc'].append(btc)
        td['matic'].append(matic)
        
    d.pop('prices')
    
    d['rank'] = td['rank']
    d['market_cap'] = td['mcap']
    d['volume24h'] = td['vol']
    d['change%'] = td['change%']
    d['usd'] = td['usd']
    d['btc'] = td['btc']
    d['matic'] = td['matic']

def rearrange_dict(d, date_list, time_list, contract_list):
    dictionary = {
        'rank': d['rank'],
        'token_name': d['token_name'],
        'symbol': d['symbol'],
        'usd': d['usd'],
        'btc': d['btc'],
        'matic': d['matic'],
        'market_cap': d['market_cap'],
        'holders': d['holders'],
        'volume24h': d['volume24h'],
        'change%': d['change%'],
        'date': date_list,
        'time': time_list,
        'contract_link': contract_list
    }
    return dictionary

def create_df(d):
    try:
        df = pd.DataFrame.from_dict(d, orient='columns')
        df = df.set_index('rank')
    except:
        for key, val in d.items():
            print('{} column has array length: '.format(key))
            print(len(val))
    return df
