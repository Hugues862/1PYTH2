
import threading


class TimerClass(threading.Thread):

    def __init__(self, count: int, name="timerThread"):
        """
        Creates a usable timer with a thread.

            Parameters:
                count (int): Beginning value of the timer in seconds. Or -1 for Endless timer.
                name (str, optional): Name of the timer. Defaults to "timerThread".
        """

        threading.Thread.__init__(self)
        self.__event = threading.Event()
        self.__count = count  # Count that will decrease until it reaches 0
        self.__name = name
        self.__timer = "Endless"
        # Endless as default because if count = -1, then it doesn't enter the loop later on to modify the timer

# Getters Start

    def getName(self):
        """
        Gets the name of the timer.

            Returns:
                str: Name of the timer.
        """
        return self.__name

    def getTimer(self):
        """
        Gets the remaining time.

            Returns:
                str: A timer in the form of '1:56' for 1 minute and 56 seconds.
        """
        return self.__timer

# End

# Setters Start

    def setName(self, name: str):
        """
        Sets the name of the timer.

        Args:
            name (str): New name of the timer.
        """
        self.__name = name

    def setTimer(self, count: int):
        """
        Sets the remaining time of the timer.

            Parameters:
                count (int): Remaining time of the timer in seconds.
        """

        self.__count = count
        mins, secs = divmod(self.__count, 60)
        self.__timer = '{:02d}:{:02d}'.format(mins, secs)

# End

# Methods Start

    def run(self):
        """
        Loop that changes the value of the timer every seconds until 0 or forced to quit. 
        Used in a Thread.
        """

        # if count is not 0 or -1 (Endless) And the "event" is not set
        while self.__count > 0 and not self.__event.is_set():
            self.__count -= 1  # Decrease the count
            # Change the count value in seconds into minutes and seconds
            mins, secs = divmod(self.__count, 60)
            # Write the time remaining in __timer
            self.__timer = '{:02d}:{:02d}'.format(mins, secs)
            self.__event.wait(1)  # Wait a second

    def stop(self):
        """
        Stops the events of the object to stop the thread.
        """
        self.__event.set()


# End
