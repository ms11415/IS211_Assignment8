#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Assignment 8, The Game of Pig - with computer player(s) and timer"""

import argparse
import random
import sys
import time

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
        if round_score == 0:
            self.answer = 'r'
        elif (100-self.score > 25 and round_score < 25):
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
        self.die = Die()
        self.current_player = 0
        self.round_score = 0
        self.total_score = 0
        self.winner = None
        self.start = time.time()
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

    def get_winner(self):

        if self.playerlist[0].score > self.playerlist[1].score:
            self.winner = 'Player 1'
        elif self.playerlist[1].score > self.playerlist[0].score:
            self.winner = 'Player 2'
        else:
            self.winner = 'TIED GAME'
        return self.winner

    def game_logic(self):
        # announce which player is playing
        self.announce_turn(self.playerlist[self.current_player])
        # ask player to decide whether to roll or hold
        self.playerlist[self.current_player].decide(self.round_score)

        if self.playerlist[self.current_player].answer == 'r':
            value = self.die.roll()
            print '-' * 40
            print 'Player {} rolled a {}'.format((self.current_player) + 1,
                                                 value)

            if value == 1:
                # subtracts the round score from the player score, to forfeit points
                self.playerlist[self.current_player].score -= self.round_score
                print 'Player {} forfeits points earned this round.'.format(
                    (self.current_player) + 1
                )
                print 'Player {} score reverts to {}.'.format(
                    (self.current_player) + 1,
                    self.playerlist[self.current_player].score)
                print 'Player {} turn is over.\n'.format(
                    (self.current_player) + 1)
                print '-' * 40
                # ends turn and sets other player as active
                self.current_player = 1 if self.current_player == 0 else 0
                # resets round score to 0
                self.clear_round_score()

            if 2 <= value <= 6:
                # updates round score based on dice roll
                self.update_round_score(value)
                # updates player score based on dice roll
                self.playerlist[self.current_player].update_score(value)
                print 'Score for this round is {}'.format(self.round_score)
                print 'New score is {}'.format(
                    self.playerlist[self.current_player].score)
                print '-' * 40
                # updates total game score if player score reaches new high
                if self.playerlist[
                    self.current_player].score > self.total_score:
                    self.total_score = self.playerlist[
                        self.current_player].score

        elif self.playerlist[self.current_player].answer == 'h':
            print '-' * 40, '\nPlayer {} chose to hold'.format(
                (self.current_player) + 1)
            print 'Score remains at {}'.format(
                self.playerlist[self.current_player].score)
            print 'Turn is now over.\n', '-' * 40
            # updates overall game score if player score reaches new high
            if self.playerlist[self.current_player].score > self.total_score:
                self.total_score = self.playerlist[self.current_player].score
            # ends turn and sets other player as active
            self.current_player = 1 if self.current_player == 0 else 0
            # resets round score to 0
            self.clear_round_score()

        else:
            # intercepts invalid input and provides direction
            print '-' * 40, '\n Invalid choice, type \'r\' or \'h\'.\n', '-' * 40

    def end_game(self):

        self.get_winner()
        print 'The winner is {}!'.format(self.winner)
        print 'Game over.'
        sys.exit()

    def play_game(self):

        while self.total_score < 100:
            self.game_logic()
        self.end_game()

class TimedGameProxy(Game):

    def play_game(self):

        while self.total_score < 100 and ((time.time() - self.start) < 60):
            print 'Time remaining: {} seconds'.format(60-(time.time() - self.start))
            self.game_logic()
        print 'Time is up!'
        self.end_game()

def main():

    # Parses required URL argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", type=str, required=True, help='Specify human or computer')
    parser.add_argument("--player2", type=str, required=True, help='Specify human or computer')
    parser.add_argument("--timed", action="store_true", help='Runs a 60 second timed game')
    args = parser.parse_args()
    player1type = args.player1
    player2type = args.player2
    timed = args.timed

    if timed:
        Pig = TimedGameProxy(player1type, player2type)
    else:
        Pig = Game(player1type, player2type)

    Pig.play_game()

if __name__ == '__main__':
    main()