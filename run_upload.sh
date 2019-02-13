#!/usr/bin/env bash
################################################################################
# run_upload
#===============================================================================
#
################################################################################
WORKDIR="$(readlink -f "$(dirname "${0}")")"
LOGDIR="${WORKDIR}/logs"
LOGFILE="${LOGDIR}/upload.log"
PYTHON="$(command -v python3)"
SITE="aviva"

for i in {1..2}; do
  ${PYTHON} "${WORKDIR}/upload.py" "${SITE}" "${LOGDIR}/SENSOR_ARRAY_${i}" > "${LOGFILE}" 2>&1
done;
