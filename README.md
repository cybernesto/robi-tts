Robi Text-To-Speech generated voice
===================================

DeAgostini's Robi is a robot capable of walking, talking, singing, dancing and much more. It has been sold in Japan, Italy and some english speaking countries. 

A german speaking version was launched but it was cancelled because of lack of interest which left german customers only with the option of buying the english version of Robi.

Unfortunately the speech recognition system uses a fixed vocabulary which cannot be changed to german. But everything that Robi is able to say is stored in wav files in its Micro-SD card. 

This repository includes a list of the wave files present in the english version of Robi created with the command:

'''
ls -hl | awk '{print $9";"}' > ../../cliplist.txt
'''

A translation of each sentence was used as the input of an awk script that would use the Mac OS X say command to speak it into the corresponding wav file. 

##Creating your own german version of Robi's heart

Just copy the cliplist_de.txt file and the generate speech.sh script into duplicate of the micro-sd card. 

**Make sure you use a duplicate since the script will overwrite all original sound files making this change irreversible.**
 
Executing the script will print the wave files as they are spoken into the memory card. After this, Robi will be able to speak any language, even if he will only understand english.

Click to see a [demonstration](https://vimeo.com/220123404)

##Contributing

I took some liberties while translating. I found that the japanese version of Robi said way too often OK so I banned this word completely. If you want to have it back you are free to do it in your own fork. But also the coordination with the movements is not perfect. If you have some suggestions, your pull requests are welcome!
