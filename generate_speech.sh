awk -F';' '{print $1; system("say -v Yannick -o ./voice/"$1" --file-format=WAVE --data-format=LEI16@44100 \""$2"\"")}' cliplist_de.txt 
