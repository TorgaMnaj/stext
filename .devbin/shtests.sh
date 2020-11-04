#!/bin/bash
SHFILES=$(find . -name "*.sh")

for i in $SHFILES
do
	chmod 755 "$i"
done

# Check for syntax errors, stdout to /dev/null:
(
for i in $SHFILES
do
	bash -xn "$i"
done
) > /dev/null


# Finegrain check with spellcheck:
(
for i in $SHFILES
do
	shellcheck "$i"
done
) | less

exit 0
