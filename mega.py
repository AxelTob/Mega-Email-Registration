import requests
import concurrent.futures
import time
from threading import Thread
from queue import Queue

# email list. Line-by-line

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

q = Queue()

def getEmailStatus(email):
    
    data = '[{"a":"ere","m":"' + email + '","v":2}]' # not pretty

    re = requests.post(URL, headers=headers, params=params, data=data)
    print(re.text)
    if re.json()[0] != -9: # if it exists
        q.put(email)




def writer():
    while True:
        if not q.empty():
            i = q.get()
            # stop Thread if None is added. Dealing with with .join deadlock case
            if i is None:
                break
            # writes to file
            with open("result2.txt", "a+") as f:
                print("writing")
                f.write(i + "\n")
        


consumer = Thread(target=writer)
consumer.setDaemon(True)
consumer.start()

# how many threads we want to run. More threads than this cannot safely run without implementing a proxy solution
THREADS = 6

def th(): # 
   
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        for email in file:
            executor.submit(getEmailStatus, email.rstrip())

    # tell writer Thread to stop
    q.put(None)
    consumer.join()
                


if __name__ == '__main__':
    # test execution time
    start_time = time.time()
    th()
    print("--- %s seconds ---" % (time.time() - start_time))

