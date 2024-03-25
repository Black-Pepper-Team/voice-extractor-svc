#!/bin/sh

set -e

eval "exec python3 ./main.py run-api $@"