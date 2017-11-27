import os
import sys
import json
from urllib import request
from bs4 import BeautifulSoup
from bs4.element import Tag
import pdb
#
class SoupCrawler:
  #
  stdout = sys.stdout
  stderr = sys.stderr
  #
  def get_text(self):
    c = self.get_items()
    if not isinstance(c, list): return None
    rtn = []
    for _ in c:
      if 'quried' in _: quried = _['quried']
      else: quried = []
      _rtn = []
      for __ in quried:
        if isinstance(__, Tag) or isinstance(__, BeautifulSoup):
          _rtn.append(__.get_text())
      rtn.append(_rtn)
    return rtn 
  #
  def get_items(self):
    #
    def _parse_seq(soup,sequence):
      #
      _bs_tag = soup
      for step in sequence:
        action = step[0]
        #
        if action == "select":
          target = step[1]
          _bs_tag = _bs_tag.select_one(target)
        elif action == "parent":
          iterate = int(step[1])
          for _ in range(iterate):
            try: _bs_tag = _bs_tag.parent
            except: _bs_tag = None
        elif (action == "next" or action == "previous"):
          iterate = int(step[1])
          tag = step[2]
          if tag is None: tag = ""
          for _ in range(iterate):
            if _bs_tag is None: return None
            if action == "next": _bs_tag = _bs_tag.find_next_sibling(tag)
            if action == "previous": _bs_tag = _bs_tag.find_previous_sibling(tag)
        else:
          pass 
      return _bs_tag
    #
    def _mission():
      mission_report = []
      for mission in self.crawler_items:
        #
        if 'url' in mission:
          url = mission["url"]
        else:
          self.__std_msg__(stderr, '[Warning] URL does not specify in the crawler configurations.')
          continue
        #
        if 'css_selector_sequence' in mission:
          seq = mission["css_selector_sequence"]
        else:
          self.__std_msg__(stderr, '[Warning] Select sequence didn\'t specified in the crawler configurations.')
          continue
        #
        serial = 0
        if "serial_no" in mission:
          serial = int(mission['serial_no'])
        #
        html_content = request.urlopen(url)
        soup = BeautifulSoup(html_content,'html.parser')
        #
        queried = []
        for seq_no in seq:
          queried.append(_parse_seq(soup,seq_no))
        #
        mission_report.append({"serial_no":serial,"quried":queried,"target_url":url})
      return mission_report
    return _mission()
  #
  def __check_path__(self,path):
    if not os.path.exists(path):
      self.__std_msg__(self.stderr, '[Error] Path "{}" doesn\'t exists. program aborted.\n'.format(path))
      return False
    return True
  #
  def __load_crawler_file__(self,path):
    with open(path,'r') as fp:
      try: crawler_cfg = json.load(fp)
      except ValueError as e:
        self.__std_msg__(self.stderr, "[Error] Crawler configuration did not accepted.\nAborted\n")
        return False
    try:
      self.crawler_display_text = crawler_cfg['display'] 
      self.crawler_items = crawler_cfg['items']
    except ValueError as e:
      self.__std_msg__(self.stderr, "[Error] Crawler definiation format are mismatch.\nAborted\n")
      return False
    return True
  #
  def __std_msg__(self, std_interface, message):
    std_interface.write('[{}]'.format(self.__class__.__name__)+message)
    std_interface.flush()
  #
  def __init__(self, crawler_path):
    #
    self.__crawler_path = crawler_path
    #
    if not self.__check_path__(crawler_path):
      sys.exit(1)
    #
    if not self.__load_crawler_file__(crawler_path):
      sys.exit(1)
    
#
if __name__ == "__main__":
  sc = SoupCrawler('../crawlers/default.json')
  #print(sc.get_items())
  print(sc.get_text())
