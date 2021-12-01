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

import queue

# ===============================================================================
def main():
    """
    Main entry point for the program.
    """
    global_queue = queue.Queue()
    reader_threads = [
        dr.DataReader(f"{x}", f"/dev/{x}", global_queue)
        for x in cfg.INSTRUMENTS
    ]

    # TODO Is any error handling required in this script? what if reader can't create serial
    # connection, or writer can't write to file?

    writer_thread = dw.DataWriter(global_queue, cfg.INSTRUMENTS)

    writer_thread.start()
    for thread in reader_threads:
        thread.start()


# ===============================================================================
if __name__ == "__main__":
    main()
