#! /bin/bash

if [ ! -e $1 ]; then
	echo "Unknown source file $1"
	exit
fi

echo "Building program..."
g++ -std=c++14 -pedantic -o kryptonians $1

sleep 1
echo "Transmitting to ships.."
sleep 2
echo "Starting simulation..."
sleep 2

./ascii-art.sh

echo "Simulation ended"
