from collections import defaultdict
import pandas as pd
import random
from sys import float_info

# There are 6**4 = 1296 codes.
def get_all_codes():
    all_codes = []
    for a in range(6):
        for b in range(6):
            for c in range(6):
                for d in range(6):
                    all_codes.append((a,b,c,d))
    return all_codes

# There are are 15 responses 
#   Red, white, or blank can occupy four spots, order doesn't matter. 
#   How many ways are there to arrange four tallies and two plus signs? Six spots, choose two of them for plus signs. 
#   Six choose 2 = 15.


# For the first attempt, there are five options. All distinct, one pair, two pair, three of a kind, and four of a kind.
#   What is the likelihood of the 15 responses for the five options? 
#   How much benefit does each option/response pair give?

def respond(attempt, code):
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
    return response


# Let's just try the five options on the 1296 possible codes. 
def analyze_option(option, codes): 
    # Add up the risk*benefit for the possible responses to the option 
    total_possibilities_count = len(codes)
    possibilities_by_response = defaultdict(list)
    for code in codes:
        possibilities_by_response[respond(option, code)].append(code)
    score = 0
    for response, codes in possibilities_by_response.items():
        possibilities_remaining_count = len(codes)
        # Benefit = number of possibilities eliminated by response
        benefit = total_possibilities_count-possibilities_remaining_count
        # Chance of benefit = probability getting the response to the option
        chance_of_benefit = possibilities_remaining_count / total_possibilities_count
        score += benefit * chance_of_benefit
    return possibilities_by_response, score

def analyze_options(options, codes):
    possibilities_by_response_by_option = {}
    scores_by_option = {}
    max_score = 0
    for option in options:
        possibilities_by_response_by_option[option], scores_by_option[option] = analyze_option(option, codes)
        if scores_by_option[option] > max_score:
            max_score = scores_by_option[option]
    best_options = [option for option, score in scores_by_option.items() if score == max_score]
    best_option = random.choice(best_options)
    responses_by_option = {}
    for option, codes_by_response in possibilities_by_response_by_option.items():
        option = ''.join([str(num) for num in option])
        responses_by_option[option] = {response: round(100*len(possibilities)/len(codes),2) for response, possibilities in codes_by_response.items()}
    return {
        "best_option": best_option, 
        "possibilities_by_response": possibilities_by_response_by_option[best_option], 
        "scores_by_option": scores_by_option, 
        "responses_by_option": responses_by_option,
        "best_options": best_options
    }

# I'll need to modify this to randomly choose a 4 distinct, pair, two pair, three of a kind, four of a kind options
def analyze_first_move():
    options = [
        (0,1,2,3),
        (0,0,1,2),
        (0,0,1,1),
        (0,0,0,1),
        (0,0,0,0),
    ]
    return  analyze_options(options, get_all_codes())
# analysis = analyze_first_move()
# best_option = analysis['best_option']
# possibilities_by_response = analysis['possibilities_by_response']
# scores_by_option = analysis['scores_by_option']
# responses_by_option = analysis['responses_by_option']


def get_random_pair_attempt():
    alpha = list(range(6))
    random.shuffle(alpha)
    return (alpha[0], alpha[0], alpha[1], alpha[2])

def get_least_lucky_response(possibilities_by_response, codes):
    most_possibilities = 0
    least_lucky_response = ''
    for response, possibilities in possibilities_by_response.items():
        possibility_count = len(possibilities)
        if possibility_count > most_possibilities:
            most_possibilities = possibility_count
            least_lucky_response = response
    return least_lucky_response

def get_random_response(possibilities_by_response, codes):
    # return a random more-than-one-pos-remaining response if there are any.
    # Otherwise return a random exactly-one-pos-remaining response.
    for response, possibilities in possibilities_by_response.items():
        if len(possibilities) > 1:
            return random.choice([r for r, ps in possibilities_by_response.items() if len(ps)>1])
    return random.choice(tuple(possibilities_by_response.keys()))

def print_status(attempt_nbr, response, prev_possibilities, analysis): 
    # (attempt_nbr, attempt, response, possibilities_remaining, is_attempt_in_possibilities):
    possibilities_remaining = analysis["possibilities_by_response"][response]
    best_options = set(analysis["best_options"])
    len_intersect = len(best_options.intersection(possibilities_remaining))
    if len(best_options) < 10: 
        print('best options:', best_options)
    
    print(f'{attempt_nbr}:',
        f'best option count: {str(len(best_options)).rjust(4)},',
        f'attempt: {analysis["best_option"]},', 
        f'response: {response.rjust(4)},'
        f'possibilities remaining: {str(len(possibilities_remaining)).rjust(4)},',
        f'all_ops_pos: {len_intersect == len(best_options)},',
        f'no_ops_pos: {len_intersect == 0}',
        
    )
    
def get_possibilities_as_options(possibilities):
    return possibilities

def get_all_codes_as_options(possibilities):
    return get_all_codes()


def play(get_first_attempt, get_response, get_possibilities_as_options):
    # first_attempt = get_first_attempt()
    possibilities = get_all_codes()
    # possibilities_by_response, score = analyze_option(first_attempt, possibilities)

    # response = get_response(possibilities_by_response, possibilities)
    # possibilities = possibilities_by_response[response]

    attempt_nbr = 0
    # _print_status(
    #     attempt_nbr,
    #     first_attempt,
    #     response,
    #     len(possibilities),
    #     True
    # )
    #    print_status(attempt_nbr, first_attempt, response, possibilities, True)
    while len(possibilities) > 1 and attempt_nbr < 20:
        analysis = analyze_options(get_possibilities_as_options(possibilities), possibilities)
        best_option = analysis['best_option']
        possibilities_by_response = analysis['possibilities_by_response']
        scores_by_option = analysis['scores_by_option']
        responses_by_option = analysis['responses_by_option']
        best_options = analysis['best_options']

        attempt_nbr += 1
        prev_possibilities = possibilities
        response = get_response(possibilities_by_response, possibilities)
        possibilities = possibilities_by_response[response]
        print_status(attempt_nbr, response, prev_possibilities, analysis) 
    # print(possibilities)    
    for response, possibilities in possibilities_by_response.items():
        if len(possibilities) < 5:
            print('    ', response.ljust(4), possibilities)
        else:
            print('    ', response.ljust(4), ', possibilities remaining:', len(possibilities))

# play(get_random_pair_attempt, get_least_lucky_response, get_possibilities_as_options)
play(get_random_pair_attempt, get_random_response, get_possibilities_as_options)
# play(get_random_pair_attempt, get_least_lucky_response, get_all_codes_as_options)
# play(get_random_pair_attempt, get_random_response, get_all_codes_as_options)


