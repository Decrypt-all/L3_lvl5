
import time


def log(txt):
    print(txt)
    file = open("log.txt", "a")  # append mode
    file.write(f"{txt} \n")
    file.close()


def timer(sec):
    if sec >= 0:
        print(f'wait: {sec} sec.   ', end='')
        time.sleep(1)
        print('\r', end='')
        sec -= 1
        timer(sec)