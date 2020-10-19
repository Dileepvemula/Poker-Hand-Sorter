Please make sure you have Python3 installed before you begin.

To run this application, using command prompt, move to the directory where these files are stored.
Run the following commands:

To run the main python file, run the following command:
        $ cat <absolute/relative path of input_file> | python my-poker-solution.py

2 sample input files are provided in IO folder with names "input1.txt" and "input2.txt"
whose expected outputs are :
    To run these test files, run the following commands:

    $ cat input1.txt | python my-poker-solution.py
        For input1.txt :
            Player 1: 263
            Player 2: 237

    $ cat input2.txt | python my-poker-solution.py
        For input2.txt :
            Player 1: 3
            Player 2: 2

Each input file contains a set of 10 cards. Each card is represented by 2 characters - the value and the suit. The first 5 cards in the line have been dealt to Player 1, the last 5 cards in the line belong to Player 2

Input:
    For example:
            AH 9S 4D TD 8S 4H JS 3C TC 8D
            |--Player 1--| |--Player 2--|

Output:
At the completion of the stream into STDIN (EOF), the output (in STDOUT) states how many hands Player 1 won, and how many hands Player 2 won.
    For example:
            Player 1: 3
            Player 2: 2
