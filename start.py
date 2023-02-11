from asyncio import threads
from chrome_driver import *
import threading

max_threads = 1
apikey = 'getkeyfrom OCR.SPACE'
link = 'https://www.tiktok.com/xxx here'


def open_threads(max_threads):
    # create a list of threads
    threads = []
    # create and start a thread for each URL
    for url in range(max_threads):
      t = threading.Thread(target=get_views, args=(apikey, link))
      threads.append(t)
      t.start()
      print("Started thread")

while True:
  open_threads(max_threads)
  time.sleep(45) # reopen threads every 60 seconds
