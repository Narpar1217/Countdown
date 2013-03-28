"""
Countdown_shell_network.py - Contains Main for Networked Countdown game played in shell.

ToDo:
  * 3/24 Entire game hasn't been looked at in a while; Needs a once-over for ToDos
  * Test the scope of general network play, rather than just LAN
  * Restore UNIX compatibility
  * Possible general cleanup and refactoring of this file? This is much larger than I prefer files to be.
     Much of the length is inherent in creating/parsing text for the shell, so there may not be much cleanup possible,
     but I do feel a lot of this file in particular continues to look hacked together.


Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

import sys, getopt, platform
from CountdownGame import CountdownGame
from CountdownServer import CountdownServer
from time import sleep
from random import randint


##########################################################################
def Main(argv):
    """Entry point for game. Handles setup and primary game loop."""

    name = raw_input('\nEnter name: ').title()
    
    #Init game object.
    #If not provided by argv, default cases for names/time handled in CountdownGame
    server = CountdownServer()

    server.Start()
    clientName = server.Receive()

    roundTime = parse_argv_win(argv, 30)

    server.SendCountLen(roundTime)
    g = CountdownGame([(name, 'server'), (clientName, 'client')], roundTime)

    try:
        #print header
        header = create_header()
        timed_message(header, 0.5, server)
        print_to_all("\n~~~ It's more or less like regular Countdown, but played in a Python shell ~~~\n\n", server) 

        #Primary game loop
        while True:

            playerChoosing = get_rand_player(g.Players)

            #Get round type from user
            inp = ''
            while not (inp == 'L' or inp == 'N'):
                inp = print_to_all__input("Play Letters or Numbers round? Enter 'L' or 'N': ", server, playerChoosing).upper()
            print_to_all('', server)

            #do round
            if inp == 'L':
                do_letters_round(g.LettersGame, g.Players, g.RoundTime, server)
            elif inp == 'N':
                do_numbers_round(g.NumbersGame, g.Players, g.RoundTime, server)

            print_scores(g.Players, server)

            #User input: continue game loop or end
            inp = ''
            while not (inp == 'Y' or inp == 'N'):
                print_to_all('', server)
                inp = print_to_all__input('Play again? Y or N: ', server, g.ServerPlayer).upper()
            
            if inp == 'N':
                server.Close()
                break
    except KeyboardInterrupt:
        print 'Exiting... (KeyboardInterrupt)'
        server.Close()
        sys.exit()


#*************************************************************
# -------------------  LETTERS FUNCTIONS ------------------- *
#*************************************************************
def check_player_word(player, game, server):
    word = print_to_all__input("{0}, please enter your word: ".format(player.Name), server, player)#raw_input(playerName + ', please enter your word: ')
    
    res, msg = game.TestWord(word)
    print_to_all(msg + '\n', server)

    if res:
        return len(word), {player.Name: word}
    else:
        return 0, {player.Name: word}

#---------------------------------------------------------------------------------------
def choose_letters_loop(game, choosingPlayer, server):
    
    while not game.ShowingFull:
        inp = print_to_all__input("Press'C' for consonant, 'V' for vowel: ", server, choosingPlayer).lower()#raw_input("Press 'C' for consonant, 'V' for vowel: ")
        if inp == 'c':
            res, msg = game.AddRandomConsonant()
            if not res:
                print_to_all(msg + '!\n', server)
                continue
        elif inp == 'v':
            res, msg = game.AddRandomVowel()
            if not res:
                print_to_all(msg + '!\n', server)
                continue
        else:
            print_to_all('', server)
            continue

        print_box_containers(game.ShowingLetters, server)
        print_to_all('\n', server)

#---------------------------------------------------------------------------------------
def determine_result_letters(lens, players, server):
    high = max(lens)
    windices = [i for i,x in enumerate(lens) if x == high]
    
    if len(windices) == len(lens):                                       #tie
        print_to_all('Tie! All players receive {0} points.'.format(high), server)
        for p in players:
            p.Score += high
            
    elif len(windices) == 1:                                             #one winner
        i = windices[0]
        players[i].Score += high
        print_to_all('{0} wins! {1} points.'.format(players[i].Name, high), server)

    else:                                                               #multiple (but not all) winners
        line = 'Players '
        for i in windices:
            players[i].Score += high
            line += players[i].Name + ' & '*int(not i == indices[-1])
        line += ' win!'
        print_to_all(line, server)
            
    return

#---------------------------------------------------------------------------------------
def do_letters_round(game, players, roundTime, server):
    game.Reset()
    
    print_to_all('####################', server)
    print_to_all('#  LETTERS ROUND!  #', server)
    print_to_all('####################', server)

    choosingPlayer = get_next_player(players)
    serverPlayer = get_server_player(players)
    
    choose_letters_loop(game, choosingPlayer, server)

    print_to_all__input('Press enter to start clock! You will have %d seconds.\n' % roundTime, server, serverPlayer)
    server.SendStartCount()
    print_countdown(roundTime)

    lens = []
    words = {}
    for p in players:
        leng, word = check_player_word(p, game, server)
        lens.append(leng)
        words.update(word)

    for name in words:
        line = "{0}'s word was '{1}'.".format(name, words[name].upper())
        print_to_all(line, server)

    print_to_all('', server)
    sleep(1)
    scores = determine_result_letters(lens, players, server)
    sleep(1.5)

    return


#*************************************************************
# -------------------  NUMBERS FUNCTIONS-------------------- *
#*************************************************************

def check_player_expr(player, game, server):
    print_to_all('', server)
    while True:
        expr = print_to_all__input(player.Name + ', please enter your expression: ', server, player)
        valid, diffOrMsg = game.CheckSolution(expr.strip())

        if valid:
            diff = diffOrMsg
            break
        else:
            print_to_all(diffOrMsg, server)

    return diff

#---------------------------------------------------------------------------------------
def determine_result_numbers(diffs, players, game, server):
    absDiffs = [abs(x) for x in diffs]
    low = min(absDiffs)
    score = game.GetScore(low)
    windices = [i for i,x in enumerate(absDiffs) if x == low]
    

    #print results of expressions & differences
    for i, p in enumerate(players):
        line = "{0}'s result: {1} (Difference: {2})".format(p.Name,
                                                         str(game.Target - diffs[i]),
                                                         str(abs(diffs[i])))
        print_to_all(line, server)
                                                            
    sleep(2)
    print ''
    #case: tie
    if len(windices) == len(diffs):
        print 'Tie! All players receive ' + str(score) + ' points.'
        for p in players:
            p.Score += score

    #case: one winner
    elif len(windices) == 1:
        i = windices[0]
        
        if score > 0:
            print '{0} wins! {1} points.'.format(players[i].Name, score)
            players[i].Score += score
        else:
            print players[i].Name + ' was closest, but not +-10 from target, thus no points are awarded.'
            
    #case: multiple (but not all) winners
    else:
        line = 'Players '
        for i in windices:
            line += players[i].Name + ' & '*int(i == windices[-1])
            players[i].Score += score

        if score > 0:
            line += ' win! Each scores {0} points!'.format(score)
        else:
            line += ' were closest, but not +-10 from target, thus no points are awarded.'

    return

#---------------------------------------------------------------------------------------
def do_numbers_round(game, players, roundTime, server):
    
    print_to_all('####################', server)
    print_to_all('#  NUMBERS ROUND ! #', server)
    print_to_all('####################\n', server)

    choosingPlayer = get_next_player(players)
    serverPlayer = get_server_player(players)
    
    while True:
        inp = print_to_all__input('How many large numbers? Enter # between 0 and 4: ', server, choosingPlayer)
        try:
            numLarge = int(inp)
            break
        except ValueError:
            print_to_all('Invalid input. Please enter integer between 0 and 4.', server)
            
    print_to_all('', server)
    game.NewRound(numLarge)
    print_box_containers(game.Numbers, server)
    print_to_all('\n  TARGET: ' + str(game.Target) + '\n', server)

    print_to_all__input('Press enter to start clock! You will have %d seconds.\n' % roundTime, server, serverPlayer)
    server.SendStartCount()
    print_countdown(roundTime)

    diffs = []
    for p in players:
        diffs.append(check_player_expr(p, game, server))

    print ''
    sleep(1)
    determine_result_numbers(diffs, players, game, server)
    sleep(1.5)
    

    return

#*************************************************************
# -------------------  UTILITY FUNCTIONS ------------------- *
#*************************************************************

def create_header():
    sep = 38*'*'
    msg = 'WELCOME TO SHELL COUNTDOWN!!!!!!!!'.split(' ')
    header = '\n' + sep
    for word in msg:
        header += '\n*' + word.center(len(sep) - 2) + '*' #'{: ^36}'.format(word) + '*'

    header += '\n' + sep

    return header

#-------------------------------------------------------------------------
def get_next_player(players):
    """
    Note: Calling this before an initial player has been selected
    (e.g. by get_rand_player) will result in player at index 0
    being selected.
    """
    try:
        i = [i for i,x in enumerate(players) if x.LastToPick][0]
    except IndexError:
        i = -1

    if i < len(players) - 1:
        nextI = i + 1
    else:
        nextI = 0

    players[i].LastToPick = False
    players[nextI].LastToPick = True
    
    return players[nextI]

#---------------------------------------------------------------------------
def get_rand_player(players):
    randI = randint(0, len(players) - 1)

    for p in players:
        p.LastToPick = False

    players[randI].LastToPick = True

    return players[randI]

#---------------------------------------------------------------------------
def get_server_player(players):
    return [x for x in players if x.PType == 'server'][0]

#-------------------------------------------------------------------------
def parse_argv_win(argv, defaultTime):
    roundTime = None
    
    if '/t' in argv:
        i = argv.index('/t')
        try:
            roundTime = int(argv[i + 1])
            if roundTime > 999:
                raise ValueError
        except ValueError:
            print >>sys.stderr, 'Invalid value for round time. Must be integer <1000. Using default.'
            roundTime = defaultTime
        except IndexError:
            print >>sys.stderr, 'usage: Countdown_shell_network.py [/t int]'
            sys.exit(1)

        argv.remove(argv[i + 1])
        argv.remove('/t')
    else:
        roundTime = defaultTime
                     

    return roundTime

#---------------------------------------------------------------------------------------
def print_box_containers(lst, server):
    topBot = ''
    mid = ''
    
    for e in [str(x) for x in lst]:
        topBot += '|' + (len(e) + 2)*'-' + '|  '
        mid += '| ' + e + ' |  '

    print_to_all(topBot, server)
    print_to_all(mid, server)
    print_to_all(topBot, server)

#-------------------------------------------------------------------------
def print_countdown(secs):
    while secs >= 0:
        sys.stdout.write('%02d\r' % secs)
        sys.stdout.flush()
        secs -= 1
        sleep(1)
        sys.stdout.write('  \r')

#-------------------------------------------------------------------------
def print_scores(players, server):
    namesLine = ''
    scoresLine = ''
    sep = 5*' '
    for p in players:
        namesLine += p.Name + sep*int(not p == players[-1])
        scoresLine += str(p.Score).center(len(p.Name)) + sep*int(not p == players[-1])

    print_to_all('\n', server)
    print_to_all('SCORES:'.center(len(namesLine)), server)
    print_to_all(namesLine, server)
    print_to_all(scoresLine, server)
    print_to_all('', server)

#-------------------------------------------------------------------------
def _print_to_client(msg, mType, server):
    server.Send(msg, mType)
    inp = ''

    if mType == 2:
        inp = server.Receive()
        
    return inp

#-------------------------------------------------------------------------
def print_to_all(msg, server):
    _print_to_client(msg, 1, server)
    print msg

#-------------------------------------------------------------------------
def print_to_all__input(msg, server, inputPlayer):
    response = ''
    
    if inputPlayer.PType == 'server':
        _print_to_client('[{0}] {1} '.format(inputPlayer.Name, msg), 1, server)
        response = raw_input(msg)
                         
    elif inputPlayer.PType == 'client':
        print '[{0}] {1} '.format(inputPlayer.Name, msg)
        response = _print_to_client(msg, 2, server)

    else:
        response = raw_input(msg)
    
    return response
    
    
#-------------------------------------------------------------------------
##def print_to_client(msg, server):
##    response = _print_to(msg, 1, server, 'client')
##
##    return response
    
#TODO: PRINT TO SPECIFIC CLIENT (ability not yet implemented in CountdownServer)
    
#-------------------------------------------------------------------------
def timed_message(message, timeout_secs, server):
    """"""
    split = message.split('\n')

    for word in split:
        print_to_all(word, server)
        sleep(timeout_secs)
        

##########################################################################
if __name__ == '__main__':
    Main(sys.argv[:])
