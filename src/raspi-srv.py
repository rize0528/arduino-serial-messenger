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
#

#
def get_serial(port, baud_rate):
  pass

#
def get_dweet_payload(dweet_base_url,thing_name):
  pass

#
def id_generator(size=10):
  chars = string.ascii_letters + string.digits
  return 'pySerialMsg:'+''.join([random.choice(chars) for _ in range(size)]
#
def main():
  #
  parser = argparse.ArgumentParser(description='''Arduino serial messenger''')
  parser.add_argument('-c','--conf',default='../conf/conf.ini')
  parser.add_argument('-l','--cralwer',default='../crawlers/default.ini')
  parser.add_argument('-tn','--thingname', dest='thingname',
  args = parser.parse_args()
  #
  cfg = configparser.ConfigParser()
  cfg.read(args.conf)
  pass
#

if __name__ == "__main__":
  sys.exit(main())
