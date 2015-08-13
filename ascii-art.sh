#! /bin/bash
if [ ! -e bobempire ]; then
	echo "Could not run simulation"
	exit
fi
if [ ! -e kryptonians ]; then
	echo "Could not run simulation"
	exit
fi

./spacebattle.py bobempire kryptonians