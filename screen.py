from main import get_proxies
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed



proxies = get_proxies()
matched_proxies = []
target_countries = [
    "United States", "Canada", "United Kingdom", "Germany", "France",
    "Netherlands", "Sweden", "Norway", "Denmark", "Finland",
    "Switzerland", "Austria", "Belgium", "Ireland", "Spain",
    "Italy", "Poland", "Portugal", "Czech Republic", "Romania",
    "Japan", "South Korea", "Singapore", "Australia", "New Zealand",
    "Brazil", "Mexico", "India", "South Africa", "United Arab Emirates",
    "Russian Federation"
]

#target_countries = ["Nigeria, Ghana"]
matched_proxies = []
for proxy in proxies:
    if (proxy['Country'] in target_countries
        and proxy['Anonymity'] == 'elite proxy'
        and proxy['Https'] == 'yes'):
        
        ip_port = f"{proxy['IP Address']}:{proxy['Port']}"
        matched_proxies.append((ip_port, proxy['Country']))   



def test_proxy(proxy, country):
    proxy_url = f"http://{proxy}"
    try:
        test = requests.get("https://api.ipify.org?format=json", proxies={"http": proxy_url, "https": proxy_url}, timeout=8)
        return proxy, country, "OK", test.json()
    except requests.exceptions.ProxyError:
        return proxy, country, "PROXY REJECTED", None
    except requests.exceptions.Timeout:
        return proxy, country, "TIMED OUT", None
    except requests.exceptions.ConnectionError:
        return proxy, country, "CONNECTION FAILED", None
    except Exception as e:
        return proxy, country, f"OTHER: {type(e).__name__}", None





#proxy alone

def give_proxxs():
    working_proxies = []
    futures = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        for p, country in matched_proxies:
            future = executor.submit(test_proxy, p, country)
            futures.append(future)
        
        for future in as_completed(futures):
            proxy, country, status, result = future.result()
            if status == "OK":
                print(f"{proxy} ({country}) → {status} {result}")
                working_proxies.append(proxy)

    return working_proxies




good_proxy  = give_proxxs()

with open("pool.txt", "w") as file:
        for proxy in good_proxy:
            print(f"writing {proxy} to proxy_pool.txt")
            file.write(proxy + "\n")

print(f"\nDone! Saved {len(good_proxy)} proxies to pool.txt")







