import aiohttp
from selectorlib import Extractor

async def scrape(url):
    headers = {
        'authority': 'www.imdb.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers= headers) as response:
            if response.status == 200:
                e = Extractor.from_yaml_file('selector.yml')
                data1 = e.extract(await response.text())
                data = data1["movie"]
                
                #print(data['sr'])
                i = 0
                #int(data[0]["runtime"][0].split()[:1][0])
                j = 0
                z = 0
                for r1 in data:
                    r2 = r1["runtime"]
                    if r2 is not None:
                        r = r2[0]
                        if int(r.split()[:1][0]) > i:
                            i = int(r.split()[:1][0])
                            z =j
                            print(i)
                    j =j+1
                return [data[z]["sr"],data[z]["name"],i]
            
            else:
                print("Blocked by imdb\n Retry after few minutes")
