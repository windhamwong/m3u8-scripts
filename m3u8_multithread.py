import requests, re, os, logging, argparse
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait

def download(url, i):
  try:
    header = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    if os.path.exists(url.split('?')[0].split('/')[-1]):
      print("[*] Item %s Exists." % (i+1), end='\r')
      return True

    print("[*] Downloading Item %s" % (i+1), end='\r')
    try:
      res = requests.get(url, headers=header)
    
      if res.status_code != 200:
        logging.error("[*] Error 30sec...: [%s] %s" % (res.status_code, url))
        sleep(30) # sleeping 30sec
        return download(url, i) # Redownloading
    except: # Do not die
      import traceback
      traceback.print_exc()
      return download(url, i)

    name = url.split('?')[0].split('/')[-1]
    print("[*] Downloading Item %s [Size: %s kb]    " % (i+1, len(res.content)/1024), end='\r')
    with open(name, 'ab+') as f:
      f.write(res.content)
    return True
  except:
    import traceback
    traceback.print_exc()
    print("[*] Error: Connection Failed... Sleep for 30 sec...")
    sleep(30)

def m3u8(url, name):
  req = None
  while not req:
    try:
      req = requests.get(url)
      req.encoding = 'utf-8'
      content = req.text
    except Exception as e:
      import traceback
      traceback.print_exc()
      print("[*] Error: Connection Failed.")
      print("[*] Sleep for 30 sec...")
      sleep(30)

  
  
  if "#EXTM3U" not in content:
    print("[*] Unknown Format.")
    print(content)
    return False

  with open('index.m3u8', 'w') as f:
    f.write(content)

  url_prefix='/'.join(url.split('/')[0:7])
  urllist=[]
  for i in re.findall('EXTINF:(.*),\n(.*)\n#',content):
    urllist.append("%s/%s" % (url_prefix, i[1]))

  print("[+] Total: %s Files." % len(urllist))

  with ThreadPoolExecutor(args.thread) as executor:
    futures = [executor.submit(download, link, urllist.index(link)) for link in urllist]
    print('[-] Waiting for tasks to complete...')
    wait(futures)


  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", dest="url", required=True)
  parser.add_argument("--thread", dest="thread", required=False, default=2)

  args = parser.parse_args()

  if m3u8(args.url, args.url.split('/')[5]):
    print('\n\n[*] Finished Downloading.')

