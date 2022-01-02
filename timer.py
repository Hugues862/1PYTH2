
import threading

class TimerClass(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self)
        self.__event = threading.Event()
        self.__count = count
        self.__name = "timerThread"
        self.__timer = "Endless"

    def run(self):
        while self.__count > 0 and not self.__event.is_set():
            self.__count -= 1
            mins, secs = divmod(self.__count, 60)
            self.__timer = '{:02d}:{:02d}'.format(mins, secs)
            self.__event.wait(1)

    def stop(self):
        self.__event.set()

    def getName(self):
        return self.__name
    
    def getTimer(self):
        return self.__timer

    def setName(self, name):
        self.__name = name

    def setTimer(self, time):
        self.__timer = time