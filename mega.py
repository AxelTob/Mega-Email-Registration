import requests
import concurrent.futures
import threading
from queue import Queue, Empty
import time






file = open('emails.txt', 'r')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://mega.nz/',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://mega.nz',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

params = (
    ('id', '-843777466'),
    ('domain', 'meganz'),
    ('v', '2'),
    ('lang', 'en'),
)
URL = 'https://g.api.mega.co.nz/cs'


def ScrapeResult(email):
    
    data = '[{"a":"ere","m":"' + email.rstrip() + '","v":2}]' # not pretty

    re = requests.post(URL, headers=headers, params=params, data=data,timeout=2)
    print(re.text)
    if re.json()[0] != -9: # if it exists
        return email

MAX_THREADS = 6

def threadS(): # 279615
    emails = file.readlines()[279615:]
    nbrlines = len(emails)
    print(nbrlines)

    threads = min(MAX_THREADS, nbrlines)
    _completed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for result in executor.map(ScrapeResult, emails, timeout=None):
        
            if result is not None:
                with open("result.txt", "a+") as f:
                    print("writing " )
                    f.write(result)
        f.close()

def noThreadS():
    emails = file.readlines()[:100]
    nbrlines = len(emails)
    print(nbrlines)

    threads = min(MAX_THREADS, nbrlines)
    
    
    for email in emails:
        result = ScrapeResult(email)
        if result is not None:
            with open("result2.txt", "a+") as f:
                print("writing " )
                f.write(result)
       

if __name__ == '__main__':
    
    # 16sek
    start_time = time.time()
    threadS()
    print("--- %s seconds ---" % (time.time() - start_time))

    #No threads 38sek
    # start_time = time.time()
    # noThreadS()
    # print("NO THREADS--- %s seconds ---" % (time.time() - start_time))