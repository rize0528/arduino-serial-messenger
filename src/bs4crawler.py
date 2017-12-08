import os
import sys
import json
import re
import requests
from urllib import request
from bs4 import BeautifulSoup
from bs4.element import Tag
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
        if action == "select_one":
          target = step[1]
          _bs_tag = _bs_tag.select_one(target)
        elif action == "select_match":
          target = step[1]
          RE_SEARCH = re.compile(step[2])
          _selected = map(lambda x: x, _bs_tag.select(target))
          _filtered = list(filter(lambda x: RE_SEARCH.search(x.get_text()), _selected))
          if len(_filtered)>0: _bs_tag = _filtered[0]
        elif action == "parent":
          iterate = int(step[1])
          for _ in range(iterate):
            try: _bs_tag = _bs_tag.parent
            except: _bs_tag = None
        elif (action == "next" or action == "previous"):
          iterate = int(step[1])
          try: tag = step[2]
          except: tag = None
          if tag is None: tag = ""
          for _ in range(iterate):
            if _bs_tag is None: return None
            if action == "next": _bs_tag = _bs_tag.find_next_sibling(tag)
            if action == "previous": _bs_tag = _bs_tag.find_previous_sibling(tag)
        else:
          pass 
      return _bs_tag
    #
    def _html_opener(url, retry=3):
      #
      _rty, rtn_code = 1, 0
      while True:
        #
        # Use requests library to get html content
        try: 
          _r = requests.get(url)
          rtn_code = _r.status_code
          if _r.status_code == 200:
            try:
              html = str(_r.text.encode('ascii','ignore'))
              return html
            except:
              html = ""
        except: html = ""

        # Use urllib.request.urlopen to get html content
        try:
          _r = request.urlopen(url)
          rtn_code = _r.status
          if _r.status == 200:
            try:
              html = _r.read()
              return html
            except: html = ""
        except: html = ""
        #
        if html == "" and _rty <= retry:
          print('[Crawl] Status: {}, retrying: "{}" ({}/{})'.format(rtn_code,url,_rty,retry))
          _rty +=1
          continue
        return "<p>Failed to crawl the website</p>"

      
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
        if 'output_template' in mission:
          text_template = mission["output_template"]
        else:
          text_template = None
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
        html_content = _html_opener(url)
        #html_content = request.urlopen(url)
        #
        soup = BeautifulSoup(html_content,'html.parser')
        #
        queried = []
        for seq_no in seq:
          queried.append(_parse_seq(soup,seq_no))
        #
        try:
          _text = list(map(lambda x: x.get_text(),queried))
        except:
          _text = [""]
        if text_template is not None:
          try: output_text = text_template.format(*_text)
          except: output_text = "[!]format_err[!]"
        else: 
          output_text = ",".join(_text)
        #
        mission_report.append({"serial_no":serial,"quried":queried,"target_url":url,"output_text": output_text})
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
  #print(sc.get_text())
  _items = sc.get_items()
  print(list(map(lambda x: x['output_text'], _items)))
