mkdir phrases
awk -F';' '{sub(/wav/,"txt",$1);$1="./phrases/"$1; print $2 > $1; close $1}' cliplist_de.txt
