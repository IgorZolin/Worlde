from words import get_wordle_guesses, get_wordle_answers, get_wordmaster_guesses, get_wordmaster_answers, get_start_tears, get_WM_start_tears
import time 
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import keyboard
import numpy as np

def play(game_rows, browser, possible_guesses, possible_answers, classic_wordle=True):
    # get the word list
    words = possible_guesses
    narrowed_down_list = possible_answers

    for guess_number in range(5):
        # goal is to minimize the longest possible word list after guess & evaluation
        # start this metric at a million (we have under 100k words)
        min_wordcount = 1e6
        chosen_word = ""
        evaluation_to_wordlist_map = {}
        if guess_number != 0:
            words_to_consider = words
            # check every word in words_to_consider to see which one gives us most information
            for word_to_guess in words_to_consider:
                temp_eval_to_words_map = {}
                
                # evaluate with every possible answer
                for possible_answer in narrowed_down_list:
                    evaluation = get_evaluation(possible_answer, word_to_guess)
                            
                    # store word by evaluation tuple in a list
                    if tuple(evaluation) not in temp_eval_to_words_map:
                        temp_eval_to_words_map[tuple(evaluation)] = [possible_answer]
                    else:
                        temp_eval_to_words_map[tuple(evaluation)].append(possible_answer)
        
                # metric we are trying to minimize
                biggest_possible_remaining_wordcount = max([len(val) for val in temp_eval_to_words_map.values()])
                
                # if we found a new minimum
                if biggest_possible_remaining_wordcount < min_wordcount:
                    min_wordcount = biggest_possible_remaining_wordcount
                    chosen_word = word_to_guess
                    
                    # save current best wordlist map
                    evaluation_to_wordlist_map = temp_eval_to_words_map
        else:
            if classic_wordle==True:
                evaluation_to_wordlist_map=get_start_tears()
            else:
                evaluation_to_wordlist_map=get_WM_start_tears()
            chosen_word="tears"

        # evaluate chosen word with answer
        enter_guess(chosen_word)
        time.sleep(1)
        if classic_wordle:
            answer_evaluation = get_wordle_evaluation(chosen_word, game_rows[guess_number], browser)
        else:
            answer_evaluation = get_wordmaster_evaluation(chosen_word, game_rows[guess_number], browser)
        if answer_evaluation in evaluation_to_wordlist_map:
            narrowed_down_list = evaluation_to_wordlist_map[answer_evaluation]
            
        if answer_evaluation == [2, 2, 2, 2, 2]:
            return [chosen_word]
        time.sleep(1)
        
        # once narrowed down to 1, we are done
        if len(narrowed_down_list) == 1:
            enter_guess(narrowed_down_list[0])
            return [chosen_word]
    return narrowed_down_list
            
def get_wordle_evaluation(chosen_word, game_row, browser):
    row = browser.execute_script('return arguments[0].shadowRoot', game_row)
    tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
    evaluation = []
    eval_to_int = {
        "correct": 2,
        "present": 1,
        "absent": 0
    }
    for tile in tiles:
        evaluation.append(eval_to_int[tile.get_attribute("evaluation")])
    return tuple(evaluation)

def get_wordmaster_evaluation(chosen_word, game_row, browser):
    evaluation = []
    for tile in game_row:
        if 'nm-inset-n-green' in tile.get_attribute("class"):
            evaluation.append(2)
        elif 'nm-inset-yellow-500' in tile.get_attribute("class"):
            evaluation.append(1)
        elif 'nm-inset-n-gray' in tile.get_attribute("class"):
            evaluation.append(0)
    return tuple(evaluation)
    
def enter_guess(word):
    keyboard.write(word, delay=0.05)
    keyboard.press_and_release('enter')

def get_evaluation(answer, word):
    # 0 = nothing, 1 = yellow, 2 = green
    output = [0, 0, 0, 0, 0]
    # check for correct letter and placement
    for i in range(5):
        if word[i] == answer[i]:
            output[i] = 2
            answer = answer[:i] + ' ' + answer[i + 1:]
           
    # check for correct letter
    for i in range(5):
        char = word[i]
        if char in answer and output[i] == 0:
            output[i] = 1
            first_occurence = answer.find(char)
            answer = answer[:first_occurence] + ' ' + answer[first_occurence + 1:]
    return tuple(output)

#Usuall game with pc
def run_game():
    narrowed_down_list = get_wordle_answers()
    # real answer - randomly chosen
    answer = random.choice(narrowed_down_list)
    for guess_number in range(5):
        chosen_word =input("word:")
        current_eval=get_evaluation(answer, chosen_word)
        if current_eval==[2,2,2,2,2]:
            print("congratulations")
        else:
            print(current_eval)
    return print("You Died")

#Classic version solver
def run_classic(cheat):
    # set up Selenium browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://www.powerlanguage.co.uk/wordle/")
    # wait to start the program
    time.sleep(2)
    action = webdriver.ActionChains(browser)
    action.click()
    action.perform()
    #keyboard.wait(start_button)  
    if cheat:
        bword=browser.execute_script("return window.localStorage.getItem('gameState');")
        start=bword.find("solution")+11  
        end=bword.find("solution")+16
        word=bword[start:end]
        enter_guess(word)        
    else:       
        game_app = browser.find_element(By.TAG_NAME, 'game-app')
        board = browser.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app)
        game_rows = board.find_elements(By.TAG_NAME, 'game-row')
        play(game_rows, browser, get_wordle_guesses(), get_wordle_answers(), True)
    time.sleep(3)
    browser.close()
    My_input()

#Octokatherine version solver
def run_octokatherine(cheat):
    # how many rounds to play
    num_games = 10
    # set up Selenium browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://octokatherine.github.io/word-master/")
    # wait to start the program
    time.sleep(2)
    #exit instructions
    keyboard.press_and_release('esc')
    #keyboard.wait(start_button)
    for num in range(num_games):
        if cheat:
            word=browser.execute_script("return window.localStorage.getItem('stateAnswer');")[1:6]
            enter_guess(word)
        else:
            # get game rows
            game_rows = np.array(browser.find_elements(By.TAG_NAME, 'span')).reshape(6, 5)           
            # guess list and answer list is the same
            play(game_rows, browser, get_wordmaster_guesses(), get_wordmaster_answers(), False)            
        # play again
        time.sleep(2)
        keyboard.press('esc')
        time.sleep(2)
        keyboard.release('esc')
        time.sleep(2)
        browser.find_element(By.XPATH, '//button[text()="Play Again"]').click()
        time.sleep(2)
    time.sleep(3)
    browser.close()
    My_input()

#Cyclic input function       
def My_input():
    print("Choose game version:")
    print("0 - play wordl")
    print("1 - solve Josh Wordl's game")
    print("2 - solve Katherine Peterson's game")
    print("3 - cheat Josh Wordl game")
    print("4 - cheat Katherine Peterson's game")
    print("9 - exit")
    print("Please make browser active windows and don't change active window")
    print("Press space to start")
    print("Press ctrl+C to exit")
    version=input()
    try:
        match version:
            case '0':
                run_game()
                My_input()
            case '1':
                run_classic(False)
            case '2':
                run_octokatherine(False)
            case '3':
                run_classic(True)
            case '4':
                run_octokatherine(True)
            case '9':
                exit()
            case _:
                My_input(input('Try Again: '))
    except KeyboardInterrupt:
        exit()

start_button = 'space'

My_input()