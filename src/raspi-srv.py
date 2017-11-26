#!/usr/local/bin/python3
#
import sys,urllib
import configparser,argparse
from bs4 import BeautifulSoup
#
import pdb
#
def watch_tb():
  url = "http://rate.bot.com.tw/xrt?Lang=en-US"
  find_items = [('div .sp-japan-div',2)]
  #
  try:
    html = urllib.urlopen(url).read()
  except:
    # Unable to fetch the source from target URL.
    return "Fail"
  #
  try:
    soup = BeautifulSoup(html)
  except:
    # Unable to parse the soup.
    return "Fail"

  for item in find_items:
    css_selector, parent_level = item
    #
#

#
def get_serial(port, baud_rate):
  pass

#
def get_dweet_payload(dweet_base_url,thing_name):
  pass

#
def main():
  #
  parser = argparse.ArgumentParser(description='''Arduino serial messenger''')
  parser.add_argument('-c','--conf',default='../conf/conf.ini')
  args = parser.parse_args()
  #
  cfg = configparser.ConfigParser()
  cfg.read(args.conf)
  pass
#

if __name__ == "__main__":
  sys.exit(main())
