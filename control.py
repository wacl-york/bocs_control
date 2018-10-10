"""=============================================================================
AQ INSTRUMENT CONTROL
--------------------------------------------------------------------------------

============================================================================="""
import threading
#===============================================================================
class DataReader(threading.Thread):
    """
    DataReader describes a thread whose purpose is to read lines of serial
    input from a specified serial port and enqueue said lines of serial input
    into a shared FIFO queue.
    """
    def __init__(self, name, port):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port

    def check_port_available(self):
        """
        TODO: IMPLEMENT THIS METHOD
        """
        pass

    def check_port_function(self):
        """
        TODO: IMPLEMENT THIS METHOD
        """
        pass

    def enqueue_data(self):
        """
        TODO: IMPLEMENT THIS METHOD
        """
        pass

    def run(self):
        pass

class DataWriter(threading.Thread):
    """
    DataWriter describes a thread whose purpose is to flush lines of serial
    input from a shared FIFO queue into different files, depending on the
    nature of the serial input to be flushed.
    """
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    # TODO: DESIGN AND IMPLEMENT THIS CLASS
#===============================================================================
def main():
    """
    Main entry point for the program.
    """
    pass
#===============================================================================
if __name__ == '__main__':
    main()
