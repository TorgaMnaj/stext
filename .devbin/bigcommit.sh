#!/bin/bash
# This script is supposed to run from Makefile in parent directory.
# Commit requires long and short description as well as version of commit number.
# TODO: zahrnout pytest testy a pylint. Zkusit prospector, mypy, Pylama.
if [ ! -d .git ]
then
	cd ..
	if [ ! -d .git ]
	then
		echo "
		I cant find .git directory! Terminating.
		"
		exit 1
	fi
fi

clear
echo "

Printing GIT STATUS:

"
sleep 1
git status

github () {
if [ -e .github ]
then
	git push origin master && echo -e "\nPushed to github.\n"
fi
}

commit () {
	# At first tests must pass.
	clear
	echo -e "\n\nTestuji:\n"
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
	)
	# Pytests:
	PYFILES=$(find . -name "*.py")
  python3 -m pytest tests/
  for i in $PYFILES
  do
    pylint "$i"
  done
	#
	while true
	do
		echo -e "\nTesty provedeny. Chcete pokračovat s commitem? (y/n)"
		read -r anw
		case $anw in
		y|Y)
			break
			;;
		n|N)
			exit 0
			;;
		*)
			echo -e "\nNeplatný znak. Znovu.\n"
			sleeps 1s
			clear
			;;
		esac
	done
	echo "Enter changelog number: "
	read -r number
	echo "Enter short description: "
	read -r sdesc
	echo "Enter long description:
	"
	read -r ldesc
	head="$number - $sdesc"
	# Commit and push.
	echo "--- $head" >> changelog && echo "    $ldesc" >> changelog && echo "" >> changelog && git add changelog
	git commit -m "$head" -m "$ldesc" && github && \
	echo "
	Commit, kontrola a zápis do changelogu provedeny.
	" || echo "
	Commit a kontrola se nezdařily."
}

sleep 1
while true
do
	echo "

	Do You want to add some files and changes to git, before proceeding?
	Press 'c' for proceeding commit or 't' for terminating and manualy adding changes to git.
	"
	read -r answer

	case $answer in
	c|C)
		commit
		break
		;;
	t|T)
		break
		;;
	*)
		echo "
		Neplatný znak! Znovu.
		"
		sleep 1
		clear
		;;
	esac
done

exit 0
