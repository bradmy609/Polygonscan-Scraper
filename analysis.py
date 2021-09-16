import pandas as pd
from sqlalchemy import create_engine, inspect
from execute import *
import ssl
import smtplib
import datetime

execute()

def config_engine():
    engine = create_engine('sqlite:///polygonscan.db', echo=False)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return engine, tables

def set_tables():
    recent = pd.read_sql("SELECT symbol, rank, usd, volume24h, date, time FROM {} WHERE volume24h > 0 AND usd > 0 AND symbol <> 'BONE'".format(tables[len(tables)-1]), con=engine)
    previous = pd.read_sql("SELECT symbol, rank, usd, volume24h, date, time FROM {} WHERE volume24h > 0 AND usd > 0 AND symbol <> 'BONE'".format(tables[len(tables)-3]), con=engine)
    recent = recent.set_index('symbol')
    previous = previous.set_index('symbol')
    return recent, previous

def compare_indices(new_table, old_table):
    new_indices = []
    for i in list(new_table.index):
        if i not in list(old_table.index):
            new_indices.append(i)

    if new_indices:
        new_coin_data = new_table.loc[new_indices]
        for i in new_indices:
            new_table = new_table.drop(i)
        return new_coin_data, new_table
    else:
        return 'None', new_table

def remove_dupes(new_table, old_table):
    nt_dupes = new_table[new_table.index.duplicated()]
    ot_dupes = old_table[old_table.index.duplicated()]
    if not nt_dupes.empty:
        new_table = new_table[~new_table.index.duplicated(keep='first')]
    if not ot_dupes.empty:
        old_table = old_table[~old_table.index.duplicated(keep='first')]
        
    duplicates = [nt_dupes, ot_dupes]
        
    return new_table, old_table, duplicates

def get_deltas(new_table, old_table, remove):
    deltas = pd.DataFrame({'symbol': new_table.index})
    d = {}
    for label in remove:
        for i in new_table.index:
            recent_coin_data = new_table.loc[i][label]
            previous_coin_data = old_table.loc[i][label]
            diff = (recent_coin_data - previous_coin_data)/recent_coin_data*100
            d[i] = round(diff, 2)
        deltas[label + ' % change'] = deltas['symbol'].map(d)
        
    return deltas

def get_new_coins(recent, previous):
    new_indices = []
    for i in list(recent.index):
        if i not in list(previous.index):
            new_indices.append(i)
    return new_indices

def get_time_difference(recent, previous):
    recent_time = recent['time'][1]
    previous_time = previous['time'][1]
    rec = datetime.datetime.strptime(recent_time, '%H:%M:%S')
    prev = datetime.datetime.strptime(previous_time, '%H:%M:%S')
    difference = rec-prev
    hour_difference = difference.seconds/3600
    hour_difference = round(hour_difference, 1)
    
    recent_date = recent['date'][1]
    previous_date = previous['date'][1]
    recd = datetime.datetime.strptime(recent_date, '%Y-%M-%d')
    prevd = datetime.datetime.strptime(previous_date, '%Y-%M-%d')
    dif = recd-prevd
    if dif.days:
        hour_difference += 24
    return hour_difference

def set_alert():
    recent_date = recent['date'][1]
    previous_date = previous['date'][1]
    recent_time = recent['time'][1]
    previous_time = previous['time'][1]
    
    message_header = "Comparing Polygonscan data from {} at {} (PST) to {} at {} (PST)".format(previous_date, previous_time, recent_date, recent_time)
    new_coins = "There were {} new coins added to the Polygon Network in this {} hour time period. The new coins are: {}".format(len(new_tokens), hour_difference, new_tokens)

    message = message_header + '\n'*2 + new_coins + '\n'*2 + "The top 15 coins for the past {} hour period are ".format(hour_difference)
    top_coin_data = deltas.head(15)
    alert = [message, top_coin_data]
    return alert

def send_email(email_lst, message):
    port = 465 # For SSL
    smtp_server = 'smtp.gmail.com'
    sender_email = 'polygonscanscraper@gmail.com'
    password = 'Apple!123'
    message = """Subject: Polygonscan Notification!
    \n\n
    
    {}\n\n
    
    {}""".format(message[0], message[1])
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        for receiver_email in email_lst:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

engine, tables = config_engine()

recent, previous = set_tables()

new_tokens = get_new_coins(recent, previous)

new_token_data, recent_newcoins_dropped = compare_indices(recent, previous)

recent, previous, duplicates = remove_dupes(recent, previous)

deltas = get_deltas(recent_newcoins_dropped, previous, ['usd', 'volume24h'])
deltas = deltas.set_index('symbol')

recent.loc['WETH']

deltas

deltas = deltas.sort_values(['usd % change', 'volume24h % change'], axis=0, ascending=False)

top_coin_data = deltas.head(15)

hour_difference = get_time_difference(recent, previous)

alert = set_alert()
# 'cryptofarmbets@gmail.com'
email_lst = ['bradleymyers574@gmail.com']

send_email(email_lst, alert)

print(deltas.head(20))
