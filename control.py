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
                                           '/dev/ttyusb0',
                                           global_queue)
    writer_thread = data_writer.DataWriter('writer_1', global_queue)

    reader_thread.run()
    writer_thread.run()
#===============================================================================
if __name__ == '__main__':
    main()
