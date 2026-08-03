import requests
import random
from bs4 import BeautifulSoup





browser_profiles = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    },
]




referers = [
    "https://www.google.com/",
    "https://chatgpt.com/",
    "https://www.scrapethissite.com/pages/",
]



accept_language = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.8",
    "en-US,en;q=0.9,fr;q=0.5",
]




def get_random_proxies():
    with open("pool.txt", "r") as file:
        proxies = file.read().splitlines()
    random.shuffle(proxies)
    return proxies
        


def get_random_header():
    profiles = random.choice(browser_profiles)
    headers = {
        "User-Agent": profiles["User-Agent"],
        "referer" : random.choice(referers),
        "Accept-Language": random.choice(accept_language),
        "Accept": profiles["Accept"],
    }
    return headers


session = requests.Session()
session.headers.update(get_random_header())


def get_requests():
    
    proxy_list = get_random_proxies()
    for proxy in proxy_list:
        print(f"using {proxy}")
        proxies={
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
        
        try:
            response = session.get("https://free-proxy-list.net/en/", proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"Proxy failed: {e}")

    print("Falling back to system proxy...")

    try:
        response = session.get("https://free-proxy-list.net/en/", timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"System proxy also failed: {e}")
        raise



def get_proxies():
    result  = get_requests()
    H = []
    all_rows = []
    soup = BeautifulSoup(result, "lxml")
    container  = soup.select_one('.table-responsive.fpl-list')
#table head
    table = container.find('table')
    table_head  = table.find('thead')
    headers  =table_head.find_all('tr')
    for heads in headers:
        head_content = heads.find_all('th')
        for final_header in head_content:
            H.append(final_header.text.strip())
            
#table body
    table_body = table.find('tbody')
    rows  = table_body.find_all('tr')

    for content in rows:
        cells  = content.find_all('td')
        B = [cell.text.strip() for cell in cells]
        row_dict = dict(zip(H, B)) 
        all_rows.append(row_dict)
    return all_rows
        


