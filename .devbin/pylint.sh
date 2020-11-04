#!/bin/bash

PYFILES=$(find . -name "*.py")
for i in $PYFILES
do
  pylint "$i"
done

exit 0
