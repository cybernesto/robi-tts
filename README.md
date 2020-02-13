# Robi Text-To-Speech generated voice

DeAgostini's Robi is a robot capable of walking, talking, singing, dancing and much more. It has been sold in Japan, Italy and some english speaking countries.

A german speaking version was launched but it was cancelled because of lack of interest which left german customers only with the option of buying the english version of Robi.

Unfortunately the speech recognition system uses a fixed vocabulary which cannot be changed to german but everything that Robi is able to say is stored in wav files in its Micro-SD card.

This repository includes a list of the wave files present in the english version of Robi created with the command:

```
ls -hl | awk '{print $9";"}' > ../../cliplist.txt
```

A translation of each sentence was used as the input of an awk script that would use the Mac OS X say command to speak it into the corresponding wav file.

## Creating your own german version of Robi's heart

Just copy the cliplist_de.txt file and the generate speech.sh script into a duplicate of the micro-sd card.

**Make sure you use a backup SD Card since the script will overwrite all the original sound files making this change irreversible.**

Executing the script will print the wave files as they are spoken into the memory card. After this, Robi will be able to speak any language, even if he will only understand english.

Click to see a [demonstration](https://vimeo.com/220123404)

## Lip-Sync

The japanese version had a pretty convincing synchronisation of the mouth LED and the speech playback. The english version was not as effective indicating that some manual work was involved in setting the mouth state. After the german translation a lot of emphasis went lost through the speech synthesis, specially because many pauses were not present anymore. This left Robi with a blinking mouth even though the speech synthesis was over. 

To solve this I wrote a rather crude python script that reads a motion file and collects the sequence of delays of each pose executed during the playback of a sound file. It reads afterwards the .wav file and calculates the RMS value of the period corresponding to each pose. Based on a simple averaging of the RMS values afterwards to calculate a threshold, the mouth LED status is updated for each pose accordingly if the RMS value of the period is above or below the threshold. This script can be executed on every pose by using the following command.

```
for j in {1..7} 9; do for i in ./$j/*.RM4; do python wave_rm4.py $i; done; done 
```

**Make sure you use a backup SD Card since the script will overwrite all the pose files making this change irreversible.**

It would be possible to modify the threshold calculation to improve this approach or even replace the RMS calculation through an FFT to extract only relevant frequency ranges to cause the LED to light up. 

My simple solution works well in most of the cases but not for the songs, since the calculation does not separate the music from the voice. I reverted the files from the backup of songsouji3.RM4 and songtimer3.RM4 to correct this.

## Contributing

I took some liberties while translating. I found that the japanese version of Robi said way too often OK so I banned this word completely. If you want to have it back you are free to do it in your own fork.
