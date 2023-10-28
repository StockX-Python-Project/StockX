from bs4 import BeautifulSoup
import pandas as pd
import requests
import glob
import json
import csv
import re
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# d:\DEV\Python\Advance_Python_Project\scrap

sc_id_values = ['AE01', 'AHE', 'API', 'BA06', 'BAF', 'BF04', 'BI', 'BPC', 'BTV', 'C', 'CI29', 'DL03', 'DRL', 'EM', 'GI01', 'H', 'HCL02', 'HDF01', 'HHM', 'HL', 'HSL01', 'ICI02', 'IIB', 'IT', 'ITC', 'JFS', 'JVS', 'KMF', 'LI09', 'LT', 'MM', 'MPS', 'MU01', 'NI', 'NTP', 'ONG', 'PGC', 'RI', 'SBI', 'SI10', 'SLI03', 'SPI', 'TCS', 'TEL', 'TI01', 'TIS', 'TM4', 'TT', 'UTC', 'UTI10', 'W']


def get_blog_url(soup):
    div_ = soup.find_all('div', attrs={'class': 'FL PR20'})
    url_list = []
    for title in div_:
        href=title.find('a')['href']
        url_list.append("https://www.moneycontrol.com/"+href)
    return url_list


def get_blog_content(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_scripts = soup.find_all('script', attrs= {'type':'application/ld+json'})
    raw_article_str = all_scripts[2].get_text().replace('\r\n', ' ')
    parts = re.split(r"""("[^"]*"|'[^']*')""", raw_article_str)
    parts[::2] = map(lambda s: "".join(s.split()), parts[::2])
    article_str = "".join(parts)
    article_str = article_str[1:]
    article_str = article_str[:-1]
    article_dict = json.loads(article_str)
    return article_dict


def get_page_no(url, sc_id, page_no, next, year):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_page_no = soup.find_all('div', attrs={'class': 'pages MR10 MT15'})
    
    # Check if 'all_page_no' is empty or not found
    if not all_page_no:
        print("Pagination not found on the page.")
        return 1, next

    page_list = [i.text for i in all_page_no[0].find_all('a')]
    
    # Check if 'page_list' is empty or not found
    if not page_list:
        print("Page numbers not found in pagination.")
        return 1, next

    if page_list and any(map(str.isdigit, page_list[-1])):
        return int(page_list[-1]), next
    else:
        next = next + 1
        page_no = int(page_list[-2])
        url = "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=" + sc_id + "&scat=&pageno=" + str(
            page_no) + "&next=" + str(next) + "&durationType=Y&Year=" + str(year) + "&duration=1&news_type="
        return get_page_no(url, sc_id, page_no, next, year)


def save_company_data(url_ = "https://www.moneycontrol.com/stocks/company_info/stock_news.php?", sc_id=[], page_no=1, next=0, years=[]):
    for company in sc_id:
        df = pd.DataFrame(columns=['company','headline',
                                   'description', 'articleBody'])
        for year in years:
            
            url = url_ + "sc_id="+company+"&scat=&pageno="+str(page_no)+"&next="+str(next)+"&durationType=Y&Year="+str(year)+"&duration=1&news_type="
            
            max_page_no, max_next = get_page_no(url, company, page_no, next, year)
            max_next = max_next + 1
            
            for i in range(max_next):
                for j in range((i*10)+1, (i*10)+11):
                    if j <= max_page_no:
                        url_list = []
                        url = url_ + "sc_id="+company+"&scat=&pageno="+str(j)+"&next="+str(i)+"&durationType=Y&Year="+str(year)+"&duration=1&news_type="
                        request = requests.get(url)
                        soup = BeautifulSoup(request.text, 'html.parser')
                        url_list = get_blog_url(soup)
                        
                        for url in url_list:
                            try:
                                article_dict = get_blog_content(url)
                                print(company)
                                
                                article_lst = [[company,
                                                article_dict['headline'],
                                                article_dict['description'],
                                                article_dict['articleBody'],
                                               ]]
                                
                                df = pd.concat([df, pd.DataFrame(article_lst, columns=['company', 'headline', 'description', 'articleBody'])], ignore_index=True)

                                
                            except:
                                article_lst = [[company, 'error', 'error', 'error']]
                                df = pd.concat([df, pd.DataFrame(article_lst, columns=['company', 'headline', 'description', 'articleBody'])], ignore_index=True)

                                
                                continue
                        else:
                            break
                    
                print(f"Data of {company} saved to news_scrape_{company}.csv")
                df.to_csv(ROOT_PATH + '/company_data/news_scrape_'+company+'.csv', index=False)


def merge_company_news():
    directory_path = ROOT_PATH + "/company_data"
    csv_files = glob.glob(f"{directory_path}/*.csv")
    output_file = "cleaned_data.csv"

    combined_data = pd.DataFrame()

    for file in csv_files:
        df = pd.read_csv(file)
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    output_csv_file = os.path.join(ROOT_PATH, output_file)

    combined_data.to_csv(output_csv_file, index=False)
    print(f"Combined data saved to {output_csv_file}")

def clean_news():
    file_path = os.path.join(ROOT_PATH, "cleaned_data.csv")
    # file_path_model = os.path.join(ROOT_PATH, "..", "models", "data" "cleaned_data.csv") # For model
    output_file = "cleaned_data.csv"
    df = pd.read_csv(file_path)
    df_cleaned = df[~df.apply(lambda row: row.astype(str).str.contains('error').any(), axis=1)]
    df_cleaned.to_csv(file_path, index=False)
    # df_cleaned.to_csv(file_path_model, index=False) # For model
    print(f"Cleaned the data & saved to {output_file}")

def scrap_news(sc_ids=[], years=[]):
    for sc_id in sc_ids:
        save_company_data(sc_id=[sc_id], years=years)
    merge_company_news()
    clean_news()
    
scrap_news(sc_ids=['RI'], years=[2019])