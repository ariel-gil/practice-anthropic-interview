#!/bin/sh
export PYTHONBREAKPOINT=trepan.api.debug
ptw -p -- -k "$1"
