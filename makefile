PHRASES := $(wildcard ./phrases/*.txt)
WAVS := $(patsubst ./phrases/%.txt,./voice/%.wav,$(PHRASES))
POSES := $(wildcard 3/*.RM4)
POSEDEP := $(POSES:3/%.RM4=phrases/%.d)

# Default target
all: $(WAVS)

# Our phony targets for managing the project
.PHONY: clean 
clean:
	$(RM) $(WAVS)

#convert files
voice/%.wav: phrases/%.txt
	say -v Yannick -o "$@" --file-format=WAVE --data-format=LEI16@44100 < $<

poses: $(POSES) $(POSEDEP)

# the following part will create .d files with recipes in the form:
#3/233絶対勝ってね９.RM4:voice/233.wav
#	 python wave_rm4.py $@

phrases/%.d:
#	sed ’s,\($*\)\.o[ :]*,\1.o $@ : ,g’ < $@.$$$$ > $@
	echo '$(@:phrases/%.d=3/%.RM4)' | sed -E 's/(.*\/)([A-Z]?[0-9]+)(.*)/\1\2\3:voice\/\2.wav/' > $@
	echo '	python wave_rm4.py $(@:phrases/%.d=3/%.RM4)' >> $@

include $(POSEDEP)

cliplist.txt: $(PHRASES)
	./collectphrases.sh > $@