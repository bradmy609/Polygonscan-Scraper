from aggregateFuncs import get_polygonscan_tokens
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

df = get_polygonscan_tokens()

dt = datetime.now()

date_h = dt.strftime('%y%m%d_%H')

table = 'poly' + date_h

engine = create_engine('sqlite:///polygonscan.db', echo=False)

df.to_sql(table, con=engine, if_exists='replace')

engine.execute("SELECT * FROM {} WHERE symbol = 'BNB'".format(table)).fetchall()

db_table = pd.read_sql("SELECT * FROM {}".format(table), con=engine)
db_table.set_index('rank')

print(db_table)