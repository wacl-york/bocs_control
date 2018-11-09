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
    instrument_names = ('SENSOR_ARRAY_1', 'SENSOR_ARRAY_2', 'PM_INSTRUMENT')
    reader_threads = [None] * len(instrument_names)

    for index, instrument_name in enumerate(instrument_names):
        reader_threads[index] = dr.DataReader(f'instrument_name',
                                              f'/dev/{instrument_name}',
                                              global_queue)

    writer_thread = dw.DataWriter('DATA_WRITER', global_queue, instrument_names)

    for thread in reader_threads:
        thread.start()
    writer_thread.start()
#===============================================================================
if __name__ == '__main__':
    main()
