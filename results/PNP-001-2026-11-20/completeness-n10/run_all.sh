#!/bin/bash
# all compositions k0+k1+k2=n, ki>=1, canonical = lexicographic minimum over the three rotations (independent of the Python type list)
n=$1; types=$(for a in $(seq 1 $((n-2))); do for b in $(seq 1 $((n-1-a))); do c=$((n-a-b)); printf "%s\n%s\n%s\n" "$a $b $c" "$c $a $b" "$b $c $a" | sort -n -k1,1 -k2,2 -k3,3 | head -1; done; done | sort -u)
echo "$types" | xargs -P 3 -I{} sh -c 'set -- {}; ./enum_blind '$n' $1 $2 $3 fails_n'$n'_$1-$2-$3.txt'
