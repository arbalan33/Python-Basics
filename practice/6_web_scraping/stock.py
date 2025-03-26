# %%
import requests
from functools import cache
import re

from bs4 import BeautifulSoup

# %% [markdown]
# # Drawing the ASCII table


# %%
fields = ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"]
data = [["Pfizer Inc.", "PFE", "United States", 78500, "Dr. Albert Bourla D.V.M., DVM, Ph.D.", 1962]]
print(draw_table(fields, data, ' 5 stocks with most youngest CEOs '))

# %% [markdown]
# # Scraping Data

# %% [markdown]
# For the requests to pass:


# %% [markdown]
# ## Top 25 most active stocks

# %%
r = request('https://finance.yahoo.com/markets/stocks/most-active/?start=0&count=25')
soup = BeautifulSoup(r.text, 'html.parser')

ls = soup.find_all('table', class_='markets-table')
assert len(ls) == 1
table = ls[0]
stocks = []
stock_names = {}
for row in table.find_all('tr')[1:]:
    a = row.find('a', href=True)
    symbol = a['href'].split('/')[-2]
    name = row.find_all('td')[1].text.strip()
    stock_names[symbol] = name
    stocks.append(symbol)
print(stocks)

# %% [markdown]
# ## 1. Top 5 stocks with youngest CEOs
# 
# Fields: Country, Employees, CEO Name, CEO Year Born

# %%
def get_data1(stock):
    r = request(f'https://finance.yahoo.com/quote/{stock}/profile/')
    soup = BeautifulSoup(r.text)
    # assuming the CEO is on the first row
    ceo_row = soup.find('table').find_all('tr')[1]    
    try:
        year = int(ceo_row.find_all('td')[-1].text)
    except:
        year = None
    name = ceo_row.find('td').text.strip()
    country = soup.find('div', class_='address').find_all('div')[-1].text.strip()

    try:
        dt = soup.find('dt', string=re.compile('.*Employees.*'))
        employees = int(dt.find_next_sibling('dd').text.replace(',', ''))
    except:
        employees = None

    return country, employees, name, year


# %%
data1 = [(stock_names[s], s, *get_data1(s)) for s in stocks]
# sort by age
data1 = sorted(data1, key=lambda l: l[-1] or 0, reverse=True)

# %%
fields = ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"]
print(draw_table(fields, data1[:5], " 5 stocks with the youngest CEOs "))

# %% [markdown]
# ## 2. Top 10 Best 52 week
# 2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
# 
# Sheet's fields: Name, Code, 52-Week Change, Total Cash

# %%
def get_data2(stock):
    r = request(f'https://finance.yahoo.com/quote/{stock}/key-statistics/')
    soup = BeautifulSoup(r.text)

    change = None
    pattern = re.compile(r'52 Week Change')
    for dt in soup.find_all('td'):
        if not pattern.search(dt.get_text(strip=True)):
            continue
        dd = dt.find_next_sibling('td')
        change = float(dd.text[:-1])
        break

    cash = None
    pattern = re.compile(r'Total Cash')
    for dt in soup.find_all('td'):
        if not pattern.search(dt.get_text(strip=True)):
            continue
        dd = dt.find_next_sibling('td')
        cash = dd.text.strip()
        break
            
    return change, cash

# %%
data2 = [(stock_names[s], s, *get_data2(s)) for s in stocks]
data2 = sorted(data2, key=lambda l: l[-2], reverse=True)

# %%
fields = ["Name", "Code", "52-Week Change (%)", "Total Cash"]
print(draw_table(fields, data2[:10], " 10 stocks with best 52-Week Change "))

# %% [markdown]
# ## 3. Top 10 largest holds of Blackrock Inc
# 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
#     Blackrock Inc is an investment management corporation.
#     
#     Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
#     
#     All fields except first two should be taken from Holders tab.
# 

# %%
r = request(f'https://finance.yahoo.com/quote/BLK/holders')
soup = BeautifulSoup(r.text)


holders = []
for h3 in soup.find_all('h3', string=re.compile('Top.*Holders')):
    for row in h3.find_next('table').find_all('tr')[1:]:
        name, shares, date_reported, out, value = (tag.text.strip() for tag in row.find_all('td'))
        holders.append((name, shares, date_reported, out, value))
holders

# %%
fields = ["Name", "Shares", "Date Reported", "% Out", "Value"]

print(draw_table(fields, holders[:10], " 10 largest holds of Blackrock Inc. "))

# %%



