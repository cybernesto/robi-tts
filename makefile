PHRASES := $(wildcard ./phrases/*.txt)
WAVS := $(patsubst ./phrases/%.txt,./voice/%.wav,$(PHRASES))
DIRS := 1 2 3 4 5 6 7 9
POSES := $(foreach dir,$(DIRS),$(wildcard $(dir)/*.RM4))
NULLPOSES := $(wildcard 1/000*.RM4)
POSES := $(filter-out $(NULLPOSES) 4/000ダンス.RM4 9/songsouji3.RM4 9/songtimer3.RM4,$(POSES))
POSEDEP := $(POSES:%.RM4=%.d)

# Default target
all: $(WAVS) poses

# Our phony targets for managing the project
.PHONY: clean 
clean:
	$(RM) $(WAVS)
	
cleand:
	$(RM) $(POSEDEP)

#convert files
voice/%.wav: phrases/%.txt
	say -v Yannick -o "$@" --file-format=WAVE --data-format=LEI16@44100 < $<

poses: $(POSEDEP) $(POSES)

# the following part will create .d files with recipes in the form:
#3/233絶対勝ってね９.RM4:voice/233.wav
#	 python3 wave_rm4.py $@
%.d:
	iconv -c -f SHIFT_JIS -t utf8  $(@:%.d=%.RM4) | awk -F'"' '/.wav/{gsub(/¥/,"/",$$2);wave[$$2]=$$2} END{for(w in wave) pre= pre" "w; print "$(@:%.d=%.RM4)" ":"pre; print "\tpython3 wave_rm4.py $(@:%.d=%.RM4)"}' > $@

-include $(POSEDEP)

cliplist.txt: $(PHRASES)
	./collectphrases.sh > $@