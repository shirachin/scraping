from dotenv import load_dotenv

import os
import platform

load_dotenv()

if platform.uname().system == "Windows":
    CHROME_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
elif platform.uname().system == "Darwin":
    CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

REWARD_FILTER = False

COUNTER_URL = "http://127.0.0.1:8080/api/gcpvcount/"

CHECKED_PROPERTY_URL = "http://127.0.0.1:8080/api/checked_property/"

API_URL = {
    "geocode": "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBJHeH2Di8LGfkQO_1M6leWRrN_0NTrJVQ&language=ja&address=",
    "checked_property": "http://127.0.0.1:8080/api/checked_property/",
    "counter": "http://127.0.0.1:8080/api/gcpvcount/",
}

A_URL = {
    'login_top': os.environ['URL_A_LOGIN_TOP'],
    'top': os.environ['URL_A_TOP'],
}

LOGIN_DATA = [
    (os.environ["LOGIN_DATA14"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA15"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA16"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA17"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA18"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA19"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA20"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA21"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA22"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA23"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA24"], os.environ["LOGIN_DATAPW"]),
    (os.environ["LOGIN_DATA25"], os.environ["LOGIN_DATAPW"]),
]
