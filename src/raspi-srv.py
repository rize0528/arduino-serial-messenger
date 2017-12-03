#!/usr/local/bin/python3
#
import sys,urllib
import random,string
import configparser,argparse
import dweepy as dp
from bs4 import BeautifulSoup
#
import pdb
#
def watch_tb():
  #
  pass
#

#
def get_serial(port, baud_rate):
  pass

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
  parser.add_argument('-l','--cralwer',default='../crawlers/default.ini')
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



  dweet_payload = get_dweet_payload(dthing, dauth)

  print(dweet_payload)

#

if __name__ == "__main__":
  sys.exit(main())
