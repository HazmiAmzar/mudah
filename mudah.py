import requests
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup

list_phone_name = []
list_phone_price = []
list_phone_condition = []
list_phone_date_advertised = []
list_phone_region = []

page_numbers = 50
for page_num in range(1, page_numbers, 1):
    url = 'https://www.mudah.my/malaysia/mobile-phones-and-gadgets-for-sale?o={}'.format(page_num)
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers)
    print(response.status_code)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        page_soup = BeautifulSoup(response.content, 'html.parser')

        for item in page_soup.find_all('div', {'class': 'sc-dvCyap GJyzO'}):
            
            try:
                name = item.find('a', {'class': 'sc-cqpYsc iFcqQE'}).text
                print(name)
            except:
                pass

            try:
                price = item.find('div', {'class': 'sc-drKuOJ fmFQHe'}).text
                print(price)
            except:
                pass
            
            try:
                condition = item.find('div', {'class': 'flex items-center text-[11px] text-black font-normal'}).text
                print(condition)
            except:
                pass
            
            try:
                date = item.find('span', {'class': 'sc-fHxwqH clBGGa'}).text
                print(date)
            except:
                pass
            
            try:
                region = item.find('span', {'class': 'sc-kXeGPI cLGhgw'}).text
                print(region)
            except:
                pass
            
            list_phone_name.append(name)
            list_phone_price.append(price)
            list_phone_condition.append(condition)
            list_phone_date_advertised.append(date)
            list_phone_region.append(region)

        phone = list(zip(list_phone_name, list_phone_price, list_phone_condition, list_phone_date_advertised, list_phone_region))
        print("Number of pages that have been scraped: ", page_num)

    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

df_name = pd.DataFrame(list_phone_name, columns=['Name'])
df_price = pd.DataFrame(list_phone_price, columns=['Price'])
df_condition = pd.DataFrame(list_phone_condition, columns=['Condition'])
df_date = pd.DataFrame(list_phone_date_advertised, columns=['Date'])
df_region = pd.DataFrame(list_phone_region, columns=['Region'])

df_phone = pd.concat([df_name, df_price, df_condition, df_date, df_region], axis = 1)
df_phone
df_phone.to_csv('mudah.csv', index=False, mode='w')