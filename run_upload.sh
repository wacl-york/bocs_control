#!/usr/bin/env bash
################################################################################
# run_upload
#===============================================================================
# Upload recorded BOCS data from logs/* to the site S3 bucket, whose name is
# derived from the passed site name.
#
# To install, create a cron task to run nightly which runs this script with the
# the correct site name as its only argument, e.g.
# 
# 0 1 * * * /usr/bin/bash /home/bocs_control/run_upload.sh ivory-coast 2>&1 > /dev/null
################################################################################
WORKDIR="$(readlink -f "$(dirname "${0}")")"
LOGDIR="${WORKDIR}/logs"
LOGFILE="${LOGDIR}/upload.log"
PYTHON="$(command -v python3)"

if [[ -z "${1}" ]]; then
  echo "ERROR: A SITE NAME MUST BE PROVIDED AS THE FIRST ARGUMENT"
  exit 1
fi

SITE="${1}"

cd "${WORKDIR}" || exit 1
for ID in A; do
  ${PYTHON} "${WORKDIR}/upload.py" "${SITE}" "${LOGDIR}/SENSOR_ARRAY_${ID}" >> "${LOGFILE}" 2>&1
done;
