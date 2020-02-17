for f in ./phrases/*.txt;
do
	awk '{sub(".txt",".wav", FILENAME); print substr(FILENAME,index(FILENAME,"s/")+2) ";" $0}' $f;
done