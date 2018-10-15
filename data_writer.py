"""=============================================================================
DataWriter CLASS
--------------------------------------------------------------------------------

============================================================================="""
import queue
import threading
#===============================================================================
class DataWriter(threading.Thread):
    """
    DataWriter describes a thread whose purpose is to flush lines of serial
    input from a shared FIFO queue into different files, depending on the nature
    of the serial input to be flushed.
    """
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue

    def dequeue_data(self):
        """
        Pull a line of data from the front of a shared queue.
        """
        # TODO: MODIFY CALL TO queue.get TO INCORPORATE A SUITABLE TIMEOUT,
        # BASED ON ATTACHED INSTRUMENT RESPONSE TIMES
        return self.queue.get(block=True, timeout=None)

    def filter_data(self, data):
        """
        Determine and return the type of data that was passed.
        """
        # TODO: IMPLEMENT THIS METHOD
        pass

    def write_data(self, data, data_type):
        """
        Write data to the appropriate log file, decided by the passed type.
        """
        # TODO: FULLY IMPLEMENT THIS METHOD
        try:
            with open('~/aq_control_log', 'a') as data_log:
                data_log.write(data)
        except OSError:
            # TODO: HANDLE INABILITY TO OPEN DATA LOG
            pass

    def run(self):
        """
        Main entry point for DataWriter threads.
        """
        while True:
            self.write_data(self.dequeue_data, None)
