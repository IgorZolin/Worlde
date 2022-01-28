# Wordle

The project was empowerd by John Wordle, Katherine Peterson, Tech Tribe

The goal was to get prctise of selenium software and get some fun.
Solve algorithm was taken from Tech Tribe. 

`words.py` contains helper functions to load the list of guess and answer words from the `.txt` files. Wordmaster (https://octokatherine.github.io/word-master/) lets you play multiple times a day, but it has a different word and guess list, so this Python file contains helper functions to load those text files as well.

tears_file contains wordlist_map for word `tears` for Jogh Wordle version of game, WM_tears_file contain wordlist_map for word `tears` for Katherine Peterson version of game.

`play_wordle.py` uses Selenium to actually play Wordle without human input. Just follow the instructions. Once you choose option the programm do evrything by itself, just wait. After programm finish to solve Wordle, you can choose new option or exit.

Decription of algorithm from Tech Tribe:
    The algorithm I used in `play_wordle.py` for the websites tries to minimize the worst-case length of the narrowed down answer list after a certain guess. This has more consistent performance. For the botfights submission, I tried to minimize the average (expected) length of the narrowed down answer list after a certain guess. While there is more variance to this algorithm, it leads to the lowest number of average guesses per wordle puzzle, which is ultimately what the competition tests. This algorithm takes forever to run for botfights (2+ hours for 1000 words in the competition), but guesses the correct answer (from 13,000 possible words) in 4.1 tries on average. Pretty solid!

Description of cheat algorithm:
    The programm just get the word for guess from local storage of the web page.
