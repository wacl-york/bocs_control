"""=============================================================================
DataWriter CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
import sys
import threading
#===============================================================================
class DataWriter(threading.Thread):
    """
    DataWriter describes a thread whose purpose is to flush lines of serial
    input from a shared FIFO queue into different files, depending on the nature
    of the serial input to be flushed.
    """
    def __init__(self, name, shared_queue):
        threading.Thread.__init__(self)
        sys.stderr.write(f"INFO: DataWriter {name} INITIALISING\n")
        self.name = name
        self.queue = shared_queue

    def dequeue_data(self):
        """
        Pull a line of data from the front of a shared queue.
        """
        # TODO: MODIFY CALL TO queue.get TO INCORPORATE A SUITABLE TIMEOUT,
        # BASED ON ATTACHED INSTRUMENT RESPONSE TIMES
        sys.stderr.write(f"INFO: DataWriter {self.name} DEQUEUEING DATA\n")
        sys.stderr.write(f"INFO: QUEUE SIZE IS NOW {self.queue.qsize()}\n")
        return self.queue.get(block=True, timeout=None)

    def filter_data(self, data):
        """
        Determine and return the type of data that was passed.
        """
        sys.stderr.write(f"INFO: DataWriter {self.name} FILTERING DATA\n")
        # TODO: IMPLEMENT THIS METHOD

    def write_data(self, data, data_type):
        """
        Write data to the appropriate log file, decided by the passed type.
        """
        # TODO: FULLY IMPLEMENT THIS METHOD
        info_string = (f"INFO: DataWriter {self.name} WRITING DATA TO LOG FILE"
                       "\n")
        sys.stderr.write(info_string)
        try:
            date = dt.now()
            id_string = (data.split(',')[0])
            date_string = f"{date.year}-{date.month}-{date.day}"
            filename = f"{id_string}_{date_string}_data.log"
            with open(f"logs/{filename}", 'a') as data_log:
                data_log.write(data)
        except OSError:
            # TODO: HANDLE INABILITY TO OPEN DATA LOG
            err_string = (f"ERROR: DataWriter {self.name} UNABLE TO APPEND TO "
                          "DATA LOG\n")
            sys.stderr.write(err_string)

    def run(self):
        """
        Main entry point for DataWriter threads.
        """
        while True:
            self.write_data(self.dequeue_data(), None)
