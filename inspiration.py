import random
import cmd
import textwrap
import sys
import os
import time

screen_width = 100

# player setup
class player:
    def _init_(self):
        self.name = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'start_zone'

my_player = player()

# title screen
def title_screen_selections():
    option = input('> ').lower()
    if option == 'play':
        start_game()
    elif option == 'help':
        help_menu()
    elif option == 'quit':
        sys.exit()
    else:
        print('please enter a valid command.')

def title_screen():
    os.system('clear')
    print('# * 10')
    print('# Welcome to the tect RPG! #')
    print('# * 10')
    print('           - Play-          ')
    print('           - Help-          ')
    print('           - Quit-          ')
    title_screen_selections()

def help_menu():
    print('# * 10')
    print('# Welcome to the tect RPG! #        ')
    print('# * 10')
    print(' type your commands to do them      ')
    print(' Use up, down, left , right to move ')
    print('     use " look" to inspect         ')
    title_screen_selections()



## game functionality
def start_game():


# map

ZONENAME = ''
DESCRIPTION ='discription'
EXAMINATION ='examine'
SOLVED = False
up = 'up'
down = 'down'
left = 'left'
right = 'right'

solved_places = {'a1': False, 'a2': False,'a3': False, 'a4': False,
                 'b1': False, 'b2': False,'b3': False, 'b4': False,
                 'c1': False, 'c2': False,'c3': False, 'c4': False,
                 'd1': False, 'd2': False,'d3': False, 'd4': False,}

zonemap = {
    'a1':{
        ZONE: "",


    }

}

## Game interactivity
def print_location():
    print(\n'')