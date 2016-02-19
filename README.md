# KuroganeScrape
web scraper for Kurogane Hammer's Smash 4 Frame Data Repository (kuroganehammer.com)

uses Python 2.7 with lxml and requests libraries

requests:
   * linux: "sudo apt-get install python-requests"
   * windows: "C:/Python27/Scripts/pip.exe install requests"

lxml:
   * linux: "sudo apt-get install python-lxml" 
   * windows: 
      - download the wheel file, "lxml-3.5.0-cp27-none-win32.whl" or "lxml-3.5.0-cp27-none-win_amd64.whl", from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
      - from command line, run "pip install lxml.whl" using the correct paths. For example, on my computer it was "C:/Python27/Scripts/pip.exe install C:/Users/Obosa/Downloads/lxml-3.5.0-cp27-none-win_amd64.whl"
