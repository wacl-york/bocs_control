#!/usr/bin/env bash
################################################################################
# run_archive
#===============================================================================
# Compresses yesterday's data log and removes the raw text file.
# It finds the log using the passed site name.
#
# To install, create a cron task to run nightly which runs this script with no
# arguments, e.g.
# 
# 0 1 * * * /usr/bin/bash /home/bocs_control/bin/run_archive.sh 2>&1 > /dev/null
################################################################################
WORKDIR="$(readlink -f "$( dirname "$(dirname "${0}")")")"
MODULEDIR="bocs_control"
LOGDIR="${WORKDIR}/logs"
LOGFILE="${LOGDIR}/archive.log"
PYTHON="$(command -v python3)"

cd "${WORKDIR}" || exit 1
for ID in A B; do
  ${PYTHON} -m "${MODULEDIR}.archive" "${LOGDIR}/SENSOR_ARRAY_${ID}" >> "${LOGFILE}" 2>&1
done;
