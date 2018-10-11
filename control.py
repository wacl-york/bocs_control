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
        Check whether or not the port property of this object refers to a valid
        serial port exposed through /dev.
        """
        pass

    def check_port_function(self):
        """
        Check whether or not data can be read from the serial port, and whether
        or not any data that can be read seems sensible.
        """
        pass

    def enqueue_data(self):
        """
        Put an incoming line of data into the shared queue, ready for a
        DataWriter to process.
        """
        pass

    def run(self):
        """
        Main entry point for DataReader threads.
        """
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

    def dequeue_data(self):
        """
        Pull a line of data from the front of the shared queue.
        """
        pass

    def filter_data(self, data):
        """
        Determine and return the type of data that was passed.
        """
        pass

    def write_data(self, data, data_type):
        """
        Write data to the appropriate log file, decided by the passed type.
        """
        pass
#===============================================================================
def main():
    """
    Main entry point for the program.
    """
    pass
#===============================================================================
if __name__ == '__main__':
    main()
