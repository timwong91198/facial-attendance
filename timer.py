import threading


def gfg():
    print("GeeksforGeeks\n")


timer = threading.Timer(5, gfg)
timer.start()
print("Exit\n")