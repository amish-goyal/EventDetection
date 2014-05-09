EventDetection
==============

This repository includes code written for my Special Problem (CS 8903) on detecting events on twitter using LDA topic modeling.

Example command to run the LDA script
screen -a time python lda.py -f <locationOfCorpus> -t <locationOfTimeFile> -o <path_Of_OP_Directory> -k <total_topics> --num-proc 12

Follow this step by running the tests.py script with the correct parameters. This will generate files that map tweets to topics for manual evaluation.