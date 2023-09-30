from tool.a_driver import ADriver

import traceback

ad = ADriver(True)

ad.login()
try:
    ad.search()
    ad.logout()
except:
    input('error : press enter ...')
    print(traceback.format_exc())
    ad.logout()
    del ad