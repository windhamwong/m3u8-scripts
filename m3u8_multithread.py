import requests, re, logging, argparse
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait

def download(url):
  header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
  }
  res = requests.get(url, headers=header)
  if res.status_code != 200:
    logging.error("[*] Error Status Code: %s" % res.status_code)
    logging.error("[*] URL: %s" % url)
    logging.error("[*] Sleep for 30 sec...")
    sleep(30) # sleeping 30sec
    return download(url) # Redownloading
  name = url.split('?')[0].split('/')[-1]
  with open(name, 'ab+') as f:
    f.write(res.content)
  return True

def m3u8(url, name):
  req = requests.get(url)
  req.encoding = 'utf-8'
  content = req.text
  
  if "#EXTM3U" not in content:
    print("[*] Unknown Format.")
    return False

  url_prefix='/'.join(url.split('/')[0:7])
  urllist=[]
  for i in re.findall('EXTINF:(.*),\n(.*)\n#',content):
    urllist.append("%s/%s" % (url_prefix, i[1]))

  with ThreadPoolExecutor(5) as executor:
    futures = [executor.submit(download, link) for link in urllist]
    print('Waiting for tasks to complete')
    wait(futures)


  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", dest="url", required=True)

  args = parser.parse_args()

  if m3u8(args.url, args.url.split('/')[5]):
    print('[*] Finished Downloading.')

