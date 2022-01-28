from os import terminal_size


def get_wordle_guesses():
    words = []
    with open("wordle_guesses.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words

def get_wordle_answers():
    words = []
    with open("wordle_answers.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words

def get_wordmaster_guesses():
    words = []
    with open("wordmaster_guesses.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words

def get_wordmaster_answers():
    words = []
    with open("wordmaster_answers.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words

def get_start_tears():
    tears={}
    with open("tears_file.txt", "r") as f:
        for lines in f:
            strings = lines.split(':')
            skey = strings[0].split(", ")
            key = [int(item) for item in skey]
            value = strings[1].rstrip()
            aval=value.split(", ")
            tears[tuple(key)] = aval
    return tears

def get_WM_start_tears():
    tears={}
    with open("WM_tears_file.txt", "r") as f:
        for lines in f:
            strings = lines.split(':')
            skey = strings[0].split(", ")
            key = [int(item) for item in skey]
            value = strings[1].rstrip()
            aval=value.split(", ")
            tears[tuple(key)] = aval
    return tears   
