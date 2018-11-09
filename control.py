"""=============================================================================
AQ INSTRUMENT CONTROL
--------------------------------------------------------------------------------

============================================================================="""
import queue

import data_reader as dr
import data_writer as dw
#===============================================================================
def main():
    """
    Main entry point for the program.
    """
    global_queue = queue.Queue()

    reader_threads = (dr.DataReader('sensor_array_reader_1',
                                    '/dev/SENSOR_ARRAY_1',
                                    global_queue),
                      dr.DataReader('sensor_array_reader_2',
                                    '/dev/SENSOR_ARRAY_2',
                                    global_queue),
                      dr.DataReader('pm_reader',
                                    '/dev/PM_INSTRUMENT',
                                    global_queue))
    writer_thread = dw.DataWriter('writer_1', global_queue)

    for thread in reader_threads:
        thread.start()
    writer_thread.start()
#===============================================================================
if __name__ == '__main__':
    main()
