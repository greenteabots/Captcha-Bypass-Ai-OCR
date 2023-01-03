from asyncio import threads
from chrome_driver import *
import threading

max_threads = int(input("Enter the maximum number of threads: "))
apikey = input("Enter your API key from https://ocr.space/ (its free): ")
link = input('Enter the video link to your tiktok video: ') or 'https://www.tiktok.com/@db_crystal_choice/video/7152658281746500870'


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
