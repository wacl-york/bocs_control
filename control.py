"""=============================================================================
AQ INSTRUMENT CONTROL
--------------------------------------------------------------------------------

============================================================================="""
import queue

import data_reader
import data_writer
#===============================================================================
def main():
    """
    Main entry point for the program.
    """
    global_queue = queue.Queue()

    reader_thread = data_reader.DataReader('reader_1',
                                           '/dev/cu.usbmodem1411',
                                           global_queue)
    writer_thread = data_writer.DataWriter('writer_1', global_queue)

    reader_thread.start()
    writer_thread.start()
#===============================================================================
if __name__ == '__main__':
    main()
