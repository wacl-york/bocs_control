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
SITE="wacl-co2-experiment"

cd "${WORKDIR}" || exit 1
for ID in A B; do
  ${PYTHON} "${WORKDIR}/upload.py" "${SITE}" "${LOGDIR}/SENSOR_ARRAY_${ID}" >> "${LOGFILE}" 2>&1
done;

${PYTHON} "${WORKDIR}/upload.py" "${SITE}" "${LOGDIR}/PURPLEAIR" >> "${LOGFILE}" 2>&1
