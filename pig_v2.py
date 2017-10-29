#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Assignment 8, The Game of Pig - with computer player(s) and timer"""

import argparse
import random
import sys

random.seed(0)

class Player(object):
    def __init__(self, name):
        self.score = 0
        self.answer = None
        self.name = name

    def decide(self):
        pass

    def update_score(self, value):
        self.score += value

class HumanPlayer(Player):

    def decide(self, round_score):
        self.answer = raw_input('(r)oll or (h)old?\n'
                                'Type your choice: ')

class ComputerPlayer(Player):

    def decide(self, round_score):
        if round_score < 25:
            self.answer = 'r'
        else:
            self.answer = 'h'

class PlayerFactory():

    def getPlayer(self, name, type):
        if type == 'human':
            return HumanPlayer(name)
        elif type == 'computer':
            return ComputerPlayer(name)

class Die(object):

    def __init__(self):
        self.value = None

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

class Game(object):

    def __init__(self, player1type, player2type):
        self.current_player = 0
        self.round_score = 0
        self.total_score = 0
        self.playerlist = []
        factory = PlayerFactory()
        self.playerlist.append(factory.getPlayer('1', player1type))
        self.playerlist.append(factory.getPlayer('2', player2type))

    def announce_turn(self, current_player):
        print 'It is now Player {}\'s turn'.format(current_player.name)

    def update_round_score(self, value):
        self.round_score += value

    def clear_round_score(self):
        self.round_score = 0


def main():

    # Parses required URL argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", type=str, required=True, help='Specify human or computer')
    parser.add_argument("--player2", type=str, required=True, help='Specify human or computer')
    args = parser.parse_args()
    player1type = args.player1
    player2type = args.player2

    Pig = Game(player1type, player2type)
    Die1 = Die()

    while Pig.total_score < 100:
        # announce which player is playing
        Pig.announce_turn(Pig.playerlist[Pig.current_player])
        # ask player to decide whether to roll or hold
        Pig.playerlist[Pig.current_player].decide(Pig.round_score)

        if Pig.playerlist[Pig.current_player].answer == 'r':
            value = Die1.roll()
            print '-' * 40
            print 'Player {} rolled a {}'.format((Pig.current_player)+1, value)

            if value == 1:
                # subtracts the round score from the player score, to forfeit points
                Pig.playerlist[Pig.current_player].score -= Pig.round_score
                print 'Player {} forfeits points earned this round.'.format(
                    (Pig.current_player)+1
                )
                print 'Player {} score reverts to {}.'.format(
                    (Pig.current_player)+1,
                    Pig.playerlist[Pig.current_player].score)
                print 'Player {} turn is over.\n'.format((Pig.current_player)+1)
                print '-' * 40
                # ends turn and sets other player as active
                Pig.current_player = 1 if Pig.current_player == 0 else 0
                # resets round score to 0
                Pig.clear_round_score()

            if 2 <= value <= 6:
                # updates round score based on dice roll
                Pig.update_round_score(value)
                # updates player score based on dice roll
                Pig.playerlist[Pig.current_player].update_score(value)
                print 'Score for this round is {}'.format(Pig.round_score)
                print 'New score is {}'.format(Pig.playerlist[Pig.current_player].score)
                print '-' * 40
                # updates total game score if player score reaches new high
                if Pig.playerlist[Pig.current_player].score > Pig.total_score:
                    Pig.total_score = Pig.playerlist[Pig.current_player].score

        elif Pig.playerlist[Pig.current_player].answer == 'h':
            print '-' * 40, '\nPlayer {} chose to hold'.format((Pig.current_player)+1)
            print 'Score remains at {}'.format(Pig.playerlist[Pig.current_player].score)
            print 'Turn is now over.\n', '-' * 40
            # updates overall game score if player score reaches new high
            if Pig.playerlist[Pig.current_player].score > Pig.total_score:
                Pig.total_score = Pig.playerlist[Pig.current_player].score
            #  ends turn and sets other player as active
            Pig.current_player = 1 if Pig.current_player == 0 else 0
            # resets round score to 0
            Pig.clear_round_score()

        else:
            # intercepts invalid input and provides direction
            print '-' * 40, '\n Invalid choice, type \'r\' or \'h\'.\n', '-' * 40

    print 'Player {} is the winner!'.format((Pig.current_player)+1)
    print 'Game over.'
    sys.exit()

if __name__ == '__main__':
    main()