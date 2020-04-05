#!/bin/bash

# exit when any command fails
set -e
# keep track of the last executed command
#trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
#trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

# The pseudo-code in the question does not correspond to the title of the question.
#
# If anybody needs to actually know how to run command 2 if command 1 fails, this is a simple explanation:
#
#cmd1 || cmd2: This will run cmd1, and in case of failure it will run cmd2
#cmd1 && cmd2: This will run cmd1, and in case of success it will run cmd2
#cmd1 ; cmd2: This will run cmd1, and then it will run cmd2, independent of the failure or success of running cmd1.

echo "FAJNIE"
cat bum.txt
echo "FAJNIE2"

testA() {
  echo "TEST A $1";
}

testB() {
  echo "TEST B $2";
}

if declare -f "$1" > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi