"""=============================================================================
AQ INSTRUMENT CONTROL
--------------------------------------------------------------------------------
- Starts a data reading thread for each of the listed instrument names, which
  reads incoming data from serial ports and stores it in a shared data structure
- Starts a data writing thread which takes data from the shared data structure
  and writes it to log files
============================================================================="""
import bocs_control.data_reader as dr
import bocs_control.data_writer as dw
import bocs_control.config as cfg

import logging
import queue
import sys

# ===============================================================================
def main():
    """
    Main entry point for the program.
    """
    global_queue = queue.Queue()
    reader_threads = []
    for instrument in cfg.INSTRUMENTS:
        try:
            reader = dr.DataReader(
                f"{instrument}", f"/dev/{instrument}", global_queue
            )
        except RuntimeError:
            logging.error(
                f"Unable to connect to {instrument}, terminating execution."
            )
            sys.exit(1)

        reader_threads.append(reader)

    writer_thread = dw.DataWriter(global_queue)
    writer_thread.start()
    for thread in reader_threads:
        thread.start()


# ===============================================================================
if __name__ == "__main__":
    main()
