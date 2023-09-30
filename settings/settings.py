import platform

if platform.uname().system == 'Windows':
  CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
elif platform.uname().system == 'Darwin':
  CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

REWARD_FILTER = False

COUNTER_URL = 'http://127.0.0.1:8080/api/gcpvcount/'

CHECKED_PROPERTY_URL = 'http://127.0.0.1:8080/api/checked_property/'

API_URL = {
  'geocode': 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBJHeH2Di8LGfkQO_1M6leWRrN_0NTrJVQ&language=ja&address=',
  'checked_property': 'http://127.0.0.1:8080/api/checked_property/',
  'counter': 'http://127.0.0.1:8080/api/gcpvcount/',
}