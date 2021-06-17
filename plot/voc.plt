#===============================================================================
# @author Killian Murphy <killian.murphy@york.ac.uk>
# @date   2021-06-15
# @brief  Plot last 100 VOC sensor signals stored in today's single manifold
#         BOCS data.
#===============================================================================

#-------------------------------------------------------------------------------
# CUSTOMISATION
#-------------------------------------------------------------------------------
set term qt noraise

set datafile separator ","
set key autotitle columnhead

set title "VOC Sensor Signals"
set xlabel "Timestamp"
set ylabel "Sensor Signal (mV)"
set key left top
set grid ytics

set xdata time
set timefmt "%s"
set format x "%Y-%m-%d %H:%M:%S"
set xtics rotate by 45 right

#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
data_file(filename) = sprintf("< tail -n 100 %s", filename)

#-------------------------------------------------------------------------------
# PLOTTING LOOP
#-------------------------------------------------------------------------------
while(1) {
    date = system("date -u +'%Y-%m-%d'")
    filename = sprintf("../logs/SENSOR_ARRAY_A/SENSOR_ARRAY_A_%s_data.log", date)

    plot data_file(filename) using 1:(0.1875 * $8) with lines title "Total VOC 1",  \
         data_file(filename) using 1:(0.1875 * $9) with lines title "Total VOC 2",  \
         data_file(filename) using 1:(0.1875 * $10) with lines title "Total VOC 3", \
         data_file(filename) using 1:(0.1875 * $11) with lines title "Total VOC 4", \
         data_file(filename) using 1:(0.1875 * $12) with lines title "OVOC 1", \
         data_file(filename) using 1:(0.1875 * $13) with lines title "OVOC 2", \
         data_file(filename) using 1:(0.1875 * $14) with lines title "OVOC 3", \
         data_file(filename) using 1:(0.1875 * $15) with lines title "OVOC 4"

    pause 1
}
