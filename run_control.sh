#!/usr/bin/env bash
################################################################################
# run_control
#===============================================================================
#
################################################################################
WORKDIR="$(readlink -f "$(dirname "${0}")")"
LOGDIR="${WORKDIR}/logs"
LOGFILE="${LOGDIR}/control.log"
PYTHON=$(command -v python3)

cd "${WORKDIR}" || exit 1
${PYTHON} "${WORKDIR}/control.py" > "${LOGFILE}" 2>&1
