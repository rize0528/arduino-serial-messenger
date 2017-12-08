#!/usr/local/bin/python3
#
import sys,urllib
import random,string
import configparser,argparse
import dweepy as dp
from bs4 import BeautifulSoup
from time import sleep
from bs4crawler import SoupCrawler
from serial import Serial
#
#
#
def get_dweet_payload(thing_name,auth=""):
  #
  try:
    dweet_returns = dp.get_latest_dweet_for(thing_name)
  except dp.api.DweepyError as e:
    print('[pyMySerialThing] Dweep error. Error msg: {}'.format(str(e)))
    dweet_returns = []
  #
  # Filter out the payload which does not match the key(dweet_auth)
  accept_payload = list(filter(lambda z: z['auth']==auth,\
                     filter(lambda y: 'auth' in y,\
                       map(lambda x: x['content'],dweet_returns))))

  return list(map(lambda x: x['data'], accept_payload))
#
def id_generator(size=10):
  chars = string.ascii_letters + string.digits
  return 'pySerialMsg_'+''.join([random.choice(chars) for _ in range(size)])
#
def main():
  #
  parser = argparse.ArgumentParser(description='''Arduino serial messenger''')
  parser.add_argument('-c','--conf',default='../conf/conf.ini')
  parser.add_argument('-l','--cralwer',default='../crawlers/default.json')
  #parser.add_argument('-d','--daemon',choices=["start","stop","restart"],required=True)
  args = parser.parse_args()
  #
  cfg = configparser.RawConfigParser()
  cfg.read(args.conf)
  #
  dauth = cfg.get('Dweet','dweet_auth')
  dthing = cfg.get('Dweet','dweet_thing')
  if dthing == "":
    print('[pyMySerialThing] Thing name does not found, randomly create one.')
    dthing = id_generator(10)
    cfg.set('Dweet','dweet_thing',dthing)
    with open(args.conf,'w') as wp: cfg.write(wp)
    print('  - New thing name is : {}'.format(dthing))
    print('  - Dweet thing name has writted to the config file')
  #



  #dweet_payload = get_dweet_payload(dthing, dauth)
  #crawled = SoupCrawler(args.cralwer) 

  #print(dweet_payload)
  #print(crawled.get_text())

  serial = Serial(cfg.get('Arduino','port'), cfg.get('Arduino','baud_rate'))
  
  #
  dweet_payload = get_dweet_payload(dthing, dauth)
  while True:
    dmessage = "".join(get_dweet_payload(dthing, dauth))
    try:
      crawled = SoupCrawler(args.cralwer) 
      #crawled_txt = crawled.get_text()[0]
      crawled_text = map(lambda x: x['output_text'],crawled.get_items())
    except:
      crawled_text = ["N/A"]
    
    cmessage = " ".join(list(map(lambda x: "["+x+"]", crawled_text)))
    #cmessage = "JPY = Cash: {}, Spot: {} = ".format(crawled_txt[1],crawled_txt[3]) 
    message = "    Live-> {}, Info-> {}".format(dmessage, cmessage)
    print('Send message: {}'.format(message))
    serial.write(message.encode())
    sleep(100)
#

if __name__ == "__main__":
  sys.exit(main())
