import time

login = True
flag = True
scanned = True
recorded = False

if login:
    #logincamera open, #logoutcamera close
    #scanned is got people or not
    if scanned:
        if flag:
            if not recorded:
                #send once to database
                recorded = True
        flag = False
    else:
        flag = True
        login = False

else:
    #logincamera open, #logoutcamera close
    #scanned is got people or not
    recorded = False
    if scanned:
        if flag:
            if not recorded:
                #send once to database
                recorded = True
        flag = False
    else:
        flag = True
        login = True



