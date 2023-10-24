#!/bin/bash

TASK=$1
ARGS=${*:2}

options() {
  script_file=`basename "$0"`
  echo -e "\n\xF0\x9F\x9A\xA9 USAGE: ./$script_file ACTIONS\n"
  echo -e "ACTIONS:\n"
  echo -e "\trun:\t Run server"
  echo -e "\tlint:\t Run linter checks with flake8, black & isort"
}

case $TASK in
    run)
      # run uvicorn server
      uvicorn main:app --reload
    ;;
    lint)
      # run linter & formatter checks
      flake8 . && black --check . && isort -c .
    ;;
    help|*)
      # help menu
      options
    ;;
esac