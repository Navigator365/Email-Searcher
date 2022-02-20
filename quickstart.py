import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account()

sh = gc.open("Email Signup Website Sheet")

print(sh.sheet1.get('A1'))

finalSheet = gc.create('testing')
finalSheet.share('bensdodge255@gmail.com', perm_type='user', role='writer')

