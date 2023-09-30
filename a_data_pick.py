from tool.driver import A_driver

import traceback

ad = A_driver(True)

ad.login()
try:
    ad.search()
    ad.logout()
except:
    input('error : press enter ...')
    print(traceback.format_exc())
    ad.logout()
    del ad