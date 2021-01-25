"""=============================================================================
AQ INSTRUMENT CONTROL
--------------------------------------------------------------------------------
- Starts a data reading thread for each of the listed instrument names, which
  reads incoming data from serial ports and stores it in a shared data structure
- Starts a data writing thread which takes data from the shared data structure
  and writes it to log files
============================================================================="""
import queue

import data_reader as dr
import data_writer as dw

# ===============================================================================
def main():
    """
    Main entry point for the program.
    """
    global_queue = queue.Queue()
    instrument_names = ["SENSOR_ARRAY_A", "SENSOR_ARRAY_B"]
    reader_threads = [None] * len(instrument_names)

    for index, instrument_name in enumerate(instrument_names):
        reader_threads[index] = dr.DataReader(
            f"{instrument_name}", f"/dev/{instrument_name}", global_queue
        )

    writer_thread = dw.DataWriter("DATA_WRITER", global_queue, instrument_names)

    writer_thread.start()
    for thread in reader_threads:
        thread.start()


# ===============================================================================
if __name__ == "__main__":
    main()
