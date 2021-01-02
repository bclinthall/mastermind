from getpass import getpass
import random

alpha = 'rgbypw'


def get_num_players():
    num_players = input('One or two players? (type 1 or 2 and press enter): ')
    if num_players == '1' or num_players == '2':
        return num_players
    else: 
        return get_num_players()

def code_is_valid(code):
    if len(code) != 4:
        print('Code must be 4 letters long. Try again.')
        return False
    for letter in code:
        if letter not in alpha:
            print('Code entered is not valid. Try again.')
            return False
    return True

def get_code_2p():
    code = getpass('Enter the code (will not display as you type): ')
    if code_is_valid(code):
        return code
    else:
        return get_code_2p()

def get_code_1p():
    code = []
    for i in range(4):
        code.append(random.choice(alpha))
    return ''.join(code)

def make_attempt(code, attempt_num):
    print('Attempt: ', attempt_num)
    attempt = input('            Make attempt: ' )
    if not code_is_valid(attempt):
        return make_attempt(code, attempt_num)
    elif attempt_is_correct(code, attempt):
        print('You are correct!!!')
        exit
    else:
        make_attempt(code, attempt_num + 1)

def attempt_is_correct(code, attempt):
    attempt = list(attempt)
    code = list(code)
    response = []
    for i in range(4):
        if attempt[i] == code[i]:
            attempt[i] = '_'
            code[i] = 'x'
            response.append('r')
    for i in range(4):
        if attempt[i] != '_':
            for j in range(4):
                if attempt[i] == code[j]:
                    attempt[i] = '_'
                    code[j] = 'x'
                    response.append('w')
    response.sort()
    response = ''.join(response)
    print('                Response:       ', response)
    return response == 'rrrr'

def main():
    num_players = get_num_players()
    print('Available colors are: Red, Blue, Yellow, Green, Pink, and White. Use the first letter to represent the color.')
    if num_players == '2':
        code = get_code_2p()
    else:
        code = get_code_1p()
    make_attempt(code, 0)

main()