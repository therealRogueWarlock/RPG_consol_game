# My first text RPG game
import random
import pygame
import cmd
import textwrap
import sys
import os
import time
from time import sleep
import shutil
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes
pygame.init()

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)


def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)


def print_talk(text, inputspeed=0.05):
    line_1 = text + '\n'
    for x in line_1:
        sys.stdout.write(x)
        sys.stdout.flush()
        if x == ' ':
            speed = 0.0
        if x != ' ':
            speed = inputspeed
        sleep(speed)


class Player:
    def __init__(self):
        self.name = 'Default'
        self.char = 'rogue'
        self.health_points = 100
        self.damage_taken = 0
        self.mana_points = 50
        self.mana_points_use = 0
        self.power = 1
        self.power_increase = 0
        self.armor = 10
        self.armor_damage = 0
        self.energi_points = 50
        self.energi_points_use = 0
        self.status_effects = []
        self.inventory = []
        self.inventory_food = ['bread', 'water']
        self.gold = 10
        self.equipment = []
        self.location = 'city inn'
        self.game_won = False
        self.game_started = False
        self.in_combat = False
        self.player_attack_move = True

    def player_info(self):
        print(f'\n{myPlayer.name} the {myPlayer.char}\n '
            f'Healt points=', myPlayer.health_points, '/', myPlayer.health_points - myPlayer.damage_taken, '\n '
              f'Mana points =', myPlayer.mana_points, '/', myPlayer.mana_points - myPlayer.mana_points_use, '\n '
              f'Energi =', myPlayer.energi_points, '/', myPlayer.energi_points - myPlayer.energi_points_use, '\n '
              f'Armor = {myPlayer.armor}\n '
              f'Inventory = {myPlayer.inventory}\n '
              f'Food inventory :\n', myPlayer.inventory_food.count('bread'), 'x bread \n',
              myPlayer.inventory_food.count('water'), 'x water \n '
              f'Gold = {myPlayer.gold}')

    def hp_mp_info(self):
        print(f'\n{myPlayer.name} the {myPlayer.char}\n '
              f'Healt points=', myPlayer.health_points, '/', myPlayer.health_points - myPlayer.damage_taken, '\n '
              f'Mana points =', myPlayer.mana_points, '/', myPlayer.mana_points - myPlayer.mana_points_use, '\n '
              f'Energi =', myPlayer.energi_points, '/', myPlayer.energi_points - myPlayer.energi_points_use, '\n ')

    def melee_attack(self):
        attack_hit = random.randint(0, 100)
        if attack_hit < 90:
            print(f'\n{self.name} attack with a melee attack\n')
            damage = round((30 * self.power)*((100 - the_enemy.armor)/100))
            the_enemy.damage_taken += damage
            print_talk(f'{self.name} deal {damage} damage to {the_enemy.name}\n')
            myPlayer.player_attack_move = False
            combat()
        else:
            print_talk(f'\n{self.name} missed his melee attack\n')
            myPlayer.player_attack_move = False
            combat()
        myPlayer.player_attack_move = False
        combat()

    def use_ability(self):
        if self.char == 'warrior' and myPlayer.energi_points - myPlayer.energi_points_use >= 10:
            print(f'\n{self.name} uses SLAM!\n')
            self.energi_points_use = 10
            damage = round((60 * self.power) * ((100 - the_enemy.armor) / 100))
            the_enemy.damage_taken += damage
            print_talk(f'{self.name} deal {damage} damage to {the_enemy.name} with slam\n')
            myPlayer.player_attack_move = False
            combat()
        elif self.char == 'mage' and myPlayer.mana_points - myPlayer.mana_points_use >= 50:
            print(f'\n{self.name} uses fireball\n')
            self.mana_points_use = 50
            damage = round((65 * self.power) * ((100 - the_enemy.armor) / 100))
            the_enemy.damage_taken += damage
            print_talk(f'{self.name} deal {damage} damage to {the_enemy.name}\n')
            myPlayer.player_attack_move = False
            combat()
        elif self.char == 'rogue' and myPlayer.energi_points - myPlayer.energi_points_use >= 35:
            print(f'\n{self.name} uses fast strike\n')
            self.energi_points_use = 35
            damage = round((45 * self.power) * ((100 - the_enemy.armor) / 100))
            the_enemy.damage_taken += damage
            print_talk(f'{self.name} deal {damage} damage to {the_enemy.name}\n')
            print_talk('The enemy is stunned.')
            combat()
        myPlayer.player_attack_move = False
        combat()

    def attempt_run(self):
        print('Your attempt to run away')
        myPlayer.player_attack_move = True
        myPlayer.in_combat = False
        the_enemy.damage_taken = 0
        main_game_loop()


class Enemy:
    def __init__(self, name, enemytype, health_points, mana_points, power, armor, attacktype):
        self.name = name
        self.enemytype = enemytype
        self.health_points = health_points
        self.damage_taken = 0
        self.mana_points = mana_points
        self.mana_points_use = 0
        self.power = power
        self.armor = armor
        self.attacktype = attacktype
        self.inventory = []


    def enemy_stats(self):
        print(f'\n{self.name} the {self.enemytype}\n '
            f'Healt points=', self.health_points, '/', self.health_points - self.damage_taken, '\n '
              f'Mana points =', self.mana_points, '/', self.mana_points - self.mana_points_use, '\n '
              f'Armor = {self.armor}\n ')

    def enemy_loot(self):
        print(f'\n{self.name} the {self.enemytype}\n '
              f'Inventory =', self.inventory, '\n')


    def enemy_attack(self):
        attack_hit = random.randint(0, 100)
        if attack_hit < 75:
            print(f'\n{self.name} attack you with a {self.attacktype} attack\n')
            damage = round((10 * self.power)*((100-myPlayer.armor)/100))
            myPlayer.damage_taken += damage
            print_talk(f'{self.name} deal {damage} damage to {myPlayer.name}\n')
            myPlayer.player_attack_move = True
            combat()
        else:
            print_talk(f'\n{self.name} missed his {self.attacktype} attack\n')
            myPlayer.player_attack_move = True
            combat()


myPlayer = Player()
the_enemy = Enemy('default', 'default', 10, 10, 1, 50, 'default')

DESCRIPTION = 'description'
INFO = 'info'
INTERACTION = 'enteraction'
HIDDENITEM = 'hidden'
ITEMINFO = 'iteminfo'
ITEM = 'item'
NPC = 'npc'
NPC_FIGHT = 'npc_fight'
ENEMY_NPC = 'enemy_npc'
ENEMY_NPC_INFO = 'npcinfo'
NPCS = 'npcs'
ENTERACTION = 'enteraction'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east',
WEST = 'west',


quests = {'lost jewelry': False, 'the woodoo doll':False}



world = {
    'city entrance': {
        DESCRIPTION: "Your at the entrance of the city.",
        INFO: " It looks old.\n The tall wooden walls filled with scratch marks"
              "\n hints that there has been attacks. What kind of animal does that?\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'city road',
        WEST: 'city market',
    },
    'city market': {
        DESCRIPTION: "Your at the city market, the sound of sheeps, cows and people talking, "
                     "makes it almoste impossible to hear your own thoughts.",
        INFO: "Your look around, you see a blacksmith, he might have some usefull stuff.\n",
        INTERACTION: True,
        HIDDENITEM: True,
        ITEMINFO: " you look down at the ground. "
                  "Between the feet of the crowd  you get a glems of some red fabric on the ground. "
                  "you move close to see what it is\n Its a ",
        ITEM: "Doll in a red dress",
        NPC: True,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: 'You walk up to the Blacksmith.\n',
        NPCS: 'Blacksmith',
        ENTERACTION: "",
        NORTH: 'city inn',
        SOUTH: 'Dead end',
        EAST: 'city entrance',
        WEST: 'city hall',
    },
    'city hall': {
        DESCRIPTION: "You find yourself standing in the great city hall.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "The bird intimidatingly asks:\nI fly without wings. I see without eyes. I move without legs.\nI conjure more love than any lover and more fear than any beast.\nI am cunning, ruthless, and tall; in the end, I rule all.'\n'What am I?'",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'city market',
        WEST: 'Dead end',
    },
    'city road': {
        DESCRIPTION: "You find yourself standing normally on clouds, strangely.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "The bird intimidatingly asks:\nI fly without wings. I see without eyes. I move without legs.\nI conjure more love than any lover and more fear than any beast.\nI am cunning, ruthless, and tall; in the end, I rule all.'\n'What am I?'",
        ITEM: "Golden necklace",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'forest edge',
        SOUTH: 'Dead end',
        EAST: 'Dead end',
        WEST: 'city entrance',
    },
    'forest edge': {
        DESCRIPTION: "You find yourself standing normally on clouds, strangely.",
        INFO: "Info about this area/room\n",
        INTERACTION: True,
        HIDDENITEM: False,
        ITEMINFO: "Info about item\n",
        ITEM: "",
        NPC: True,
        NPC_FIGHT: True,
        ENEMY_NPC: {
                    'NAME': 'OGRE',
                    'ENEMYTYPE': 'ogre',
                    'HEALTH': 50,
                    'MANA': 0,
                    'POWER': 1,
                    'ARMOR': 45,
                    'INVENTORY': 'A brown pouch',
                    'ATTACKTYPE': 'melee',
                    'blocking': 'forest road',
                    'dead': False,
                    'looted': False},
        ENEMY_NPC_INFO: 'An ogre sits on a stone close to the entrance of the forest.',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'city road',
        EAST: 'forest road',
        WEST: 'Dead end',
    },
    'forest road': {
        DESCRIPTION: "You find yourself standing normally on clouds, strangely.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "The bird intimidatingly asks:\nI fly without wings. I see without eyes. I move without legs.\nI conjure more love than any lover and more fear than any beast.\nI am cunning, ruthless, and tall; in the end, I rule all.'\n'What am I?'",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'forest opening',
        WEST: 'forest edge',
    },
    'forest opening': {
        DESCRIPTION: "You find yourself standing normally on clouds, strangely.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "Info about item",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'mountain road',
        WEST: 'forest road',
    },
    'mountain road': {
        DESCRIPTION: "You find yourself standing normally on clouds, strangely.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "Info about item",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: '',
        NPCS: '',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'Dead end',
        WEST: 'forest opening',
    },
    'city inn': {
        DESCRIPTION: "You are at the city inn.",
        INFO: "Its an old inn, but its cosy.\n"
              "The inkeeper is standing behind the counter",
        INTERACTION: True,
        HIDDENITEM: False,
        ITEMINFO: 'info about item',
        NPC: True,
        NPC_FIGHT: False,
        ENEMY_NPC_INFO: "\nYou walk up to the counter.\n",
        NPCS: 'Innkeeper',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'city market',
        EAST: 'Dead end',
        WEST: 'Dead end',
    },
    'default': {
        DESCRIPTION: "Descrips the location",
        INFO: "Info about this area/room\n",
        INTERACTION: False,
        HIDDENITEM: False,
        ITEMINFO: "Info about item\n",
        ITEM: "",
        NPC: False,
        NPC_FIGHT: False,
        ENEMY_NPC: {
                    'NAME': 'Default',
                    'ENEMYTYPE': 'Default',
                    'HEALTH': 0,
                    'MANA': 0,
                    'POWER': 0,
                    'ARMOR': 0,
                    'INVENTORY': '',
                    'ATTACKTYPE': 'default',
                    'blocking': 'forest road',
                    'dead': True,
                    'looted': True},
        ENEMY_NPC_INFO: 'Info about the NPC.',
        NPCS: 'what npc(vendors at this location)',
        ENTERACTION: "",
        NORTH: 'Dead end',
        SOUTH: 'Dead end',
        EAST: 'Dead end',
        WEST: 'Dead end',
    },
}

# Game Menu/startscreen
def title_screen_options():
    # Allows the player to select the menu options, case-insensitive.
    option = input("> ").strip().lower()
    if option == "play":
        setup_game()
    elif option == "quit":
        sys.exit()
    elif option == "help":
        help_menu()
    elif option == "combat help":
        combat_help()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Invalid command, please try again.".center(cols))
        title_screen_options()


def title_screen_selections():
    option = input('> ').lower().strip().center(cols)
    if option == 'play':
        setup_game()
    elif option == 'help':
        help_menu()
    elif option == 'quit':
        sys.exit()
    else:
        print('please enter a valid command.'.center(cols))



def title_screen():
    # Clears the terminal of prior code for a properly formatted title screen.
    os.system('cls')
    # Prints the pretty title.
    print(('#' * 45).center(cols))
    print('#     Welcome to this text-based RPG        #'.center(cols))
    print("#          Sander Kirchert Project!         #".center(cols))
    print(('#' * 45).center(cols))
    print("                 .: Play :.                  ".center(cols))
    print("                 .: Help :.                  ".center(cols))
    print("                 .: Quit :.                  ".center(cols))
    title_screen_options()


def in_game_help_options():
    # Allows the player to select the menu options, case-insensitive.
    option = input("> ").strip().lower().center(cols)
    if option == "continue" or '':
        os.system('cls')
        main_game_loop()
    elif option == "quit":
        sys.exit()
    elif option == "combat help":
        combat_help()
    while option.lower() not in ['continue', 'combat help', 'quit', '']:
        print("Invalid command, please try again.".center(cols))
        in_game_help_options()


def help_menu():
    if myPlayer.game_started is False:
        os.system('cls')
        print("".center(cols))
        print(('#' * 45).center(cols))
        print("Written by Sander Kirchert".center(cols))
        print("Version Final (1.0.0a)".center(cols))
        print(("~" * 45).center(cols))
        print("Type a command such as 'move' then 'North'".center(cols))
        print("to navigate the map of the world.\n".center(cols))
        print("Inputs such as 'look' or 'examine' will".center(cols))
        print("let you interact with items or puzzles in rooms.\n".center(cols))
        print("Puzzles will require various input ".center(cols))
        print(('#' * 45).center(cols))
        print("\n".center(cols))
        print(('#' * 45).center(cols))
        print("    Please select an option to continue.     ".center(cols))
        print(('#' * 45))
        print("                 .: Play :.                  ".center(cols))
        print("                 .: Combat help :.           ".center(cols))
        print("                 .: Quit :.                  ".center(cols))
        title_screen_options()
    if myPlayer.game_started is True:
        os.system('cls')
        print(("~" * 45).center(cols))
        print("Written by Sander Kirchert".center(cols))
        print("Version Final (1.0.0a)".center(cols))
        print(("~" * 45).center(cols))
        print("Type a command such as 'move' then 'North'".center(cols))
        print("to navigate the map of the world.\n".center(cols))
        print("Inputs such as 'look' or 'examine' will".center(cols))
        print("let you interact with items or puzzles in rooms.\n".center(cols))
        print("Puzzles will require various input ".center(cols))
        print("'clear' clears the consol.\n"
              "'stats' shows your stats.".center(cols))
        print(('#' * 45).center(cols))
        print("\n".center(cols))
        print(('#' * 45).center(cols))
        print("    Please select an option to continue.     ".center(cols))
        print("                 .: Continue  :.             ".center(cols))
        print("                 .: Combat help :.           ".center(cols))
        print("                 .: Quit :.                  ".center(cols))
        print(('#' * 45).center(cols))
        in_game_help_options()


def combat_help():
    os.system('cls')
    print(("~" * 45).center(cols))
    print("In combat you have thees commands:".center(cols))
    print("'Melee attack': Swings at you opponent with a melee attack".center(cols))
    print("'Ability': Uses your class ability".center(cols))
    print("'stats' shows your stats.".center(cols))
    print("'Run': you attempt to run away".center(cols))
    print(('#' * 45).center(cols))
    print("\n".center(cols))
    print(('#' * 45).center(cols))
    input('#          hit enter to continue            #')
    os.system('cls')
    if myPlayer.game_started is True:
        if myPlayer.in_combat is True:
            combat()
            pass
        else:
            main_game_loop()
    else:
        title_screen()
        title_screen_options()


# game interactivity
def print_location():
    os.system('cls')
    print(('*' * (45 + len(myPlayer.location))).center(cols))
    print(('*'+(21*' ') + myPlayer.location.upper()+(21*' ') + ' *').center(cols))
    print_talk((world[myPlayer.location][DESCRIPTION]).center(cols))
    if world[myPlayer.location][NPC_FIGHT] and not world[myPlayer.location][ENEMY_NPC]['dead']:
        print_talk(world[myPlayer.location][ENEMY_NPC_INFO].center(cols))
    print(('*' * (45 + len(myPlayer.location))).center(cols))


# takes actions from the player
def promt():
    print(('=' * (11 + len(myPlayer.location))).center(cols))
    print(('* At the ' + myPlayer.location.upper() + ' *').center(cols))
    print(('=' * (11 + len(myPlayer.location))).center(cols))
    print('\nWhat would you like to do?\n')
    print(['move', 'go', 'travel', 'walk', 'talk', 'examine', 'inspect',
                          'look', 'use', 'dig', 'quit', 'help', 'clear', 'stats', 'fight', 'eat',  'drink', 'loot'])
    action = input('> ').lower().strip()
    acceptable_actions = ['move'
                          '', 'go', 'travel', 'walk', 'talk', 'examine', 'inspect',
                          'look', 'use', 'dig', 'quit', 'help', 'clear', 'stats', 'fight', 'eat',  'drink', 'loot']
    while action not in acceptable_actions:
        print('unknown command, try another action or go to help.'.center(cols))
        action = input('> ').lower().strip()
    if action == 'quit':
        sys.exit()
    elif action in ['move', 'go', 'travel', 'walk']:
        player_move(action)
    elif action in ['examine', 'inspect', 'look']:
        player_explore(action)
    elif action in ['talk']:
        player_talk()
    elif action in ['use', 'dig']:
        player_interaction()
    elif action in ['eat']:
        eat_bread()
    elif action in ['drink']:
        drink_water()
    elif action == 'fight':
        fight_fidner()
    elif action == 'loot':
        looter()
    elif action == 'help':
        help_menu()
    elif action == 'clear':
        os.system('cls')
        main_game_loop()
    elif action == 'stats':
        myPlayer.player_info()
        main_game_loop()


# movement/enteraction
def movement_handler(destination):
    try:
        if world[myPlayer.location][ENEMY_NPC]['dead'] is False \
        and world[myPlayer.location][ENEMY_NPC]['blocking'] == destination:
            print_talk('An enemy is blocking the path, defeat him to move past')
            main_game_loop()
    except:
        pass
    if destination == 'Dead end':
        print('\n its a dead end')
        main_game_loop()
    else:
        print('\nYou have moved to the ' + destination + '.')
        myPlayer.location = destination
        print_location()


def player_move(action):
    ask = "where would you like to go?\n>"
    print('\n' + ('=' * (4 + len(myPlayer.location))).center(cols))
    print(('* '+myPlayer.location.upper() + ' *').center(cols))
    print(('=' * (4 + len(myPlayer.location))).center(cols))
    print(('Go north: ' + world[myPlayer.location][NORTH]).center(cols))
    print(('Go south: ' + world[myPlayer.location][SOUTH]).center(cols))
    print(('Go east: ' + world[myPlayer.location][EAST]).center(cols))
    print(('Go west: ' + world[myPlayer.location][WEST]).center(cols))
    dest = input(ask).lower().strip()
    if dest in ['up', 'forward', 'north']:
        destination = world[myPlayer.location][NORTH]
        movement_handler(destination)
    elif dest in ['down', 'back', 'south']:
        destination = world[myPlayer.location][SOUTH]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = world[myPlayer.location][EAST]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = world[myPlayer.location][WEST]
        movement_handler(destination)
    else:
        print("Invalid direction command, try using up, down, left, or right.\n")
        player_move(action)


def player_explore(action):
    if action == 'look':
        print_talk(world[myPlayer.location][INFO], 0.05)
    elif action == 'examine' and world[myPlayer.location][HIDDENITEM] is True:
            print_talk(world[myPlayer.location][ITEMINFO], 0.05)
            print_talk(world[myPlayer.location][ITEM], 0.05)
            yesno = input('\npick up? (y/n)> ').lower().strip()
            if yesno == 'y':
                myPlayer.inventory.append(world[myPlayer.location][ITEM])
                print('\nyou have picked up a '+world[myPlayer.location][ITEM])
                world[myPlayer.location][HIDDENITEM] = False
                main_game_loop()
            elif yesno == 'n':
                main_game_loop()
    else:
        print("\nThere is nothing more for you to see here.\n")
        main_game_loop()


def player_talk():
    if world[myPlayer.location][NPC] is True:
        print(world[myPlayer.location][ENEMY_NPC_INFO])
        talk = input('Talk to ' + world[myPlayer.location][NPCS] + '(y/n)> ').lower().strip()
        if talk == 'y':
            npcname = world[myPlayer.location][NPCS]
            npc_finder(npcname)
        elif talk == 'n':
            main_game_loop()
    else:
        print('\nNo one to talk to here...')
        main_game_loop()


def player_interaction():
    if world[myPlayer.location][ENTERACTION] is True:
        print('\n' + (world[myPlayer.location][INFO]))
    else:
        print('Nothing more to do here.')


# NPCs
def innkeeper():
    print('\nInnkeeper:')
    print_talk('Hallo there my friend, what can i do for you?', 0.05)
    action = input('\n(buy, talk, leave)\n> ').lower().strip()
    acceptable_actions = ['buy', 'talk', 'leave']
    while action not in acceptable_actions:
        print('unknown command, try another action.')
        action = input('> ').lower().strip()
    if action == 'leave':
        print('Innkeeper: Bye bye, hope to see you soon')
        main_game_loop()
    elif action == 'buy':
        food_vendor()
    elif action == 'talk':
        lost_jewelry()




def blacksmith():
    print('Blacksmith:')
    print_talk('Hallo there, what can i do for you?', 0.05)

    main_game_loop()


def npc_finder(npcname):
    if npcname == 'Innkeeper':
        innkeeper()
    elif npcname == 'Blacksmith':
        blacksmith()
    else:
        pass


# shops
def food_vendor():
    print(f'\n Gold = {myPlayer.gold}')
    print(f'Food inventory :\n', myPlayer.inventory_food.count('bread'), 'x bread \n',
          myPlayer.inventory_food.count('water'), 'x water \n')
    print(f'\n {world[myPlayer.location][NPCS]}:')
    print_talk(' I sell bread and water for 5 gold each.', 0.03)
    while True:
        purchase = input('\n What would you like to buy?(bread/water/leave)> ').lower().strip()
        if purchase == 'bread' and myPlayer.gold >= 5:
            myPlayer.inventory_food.append('bread')
            myPlayer.gold -= 5
            print(f'\n Gold = {myPlayer.gold}')
            print(f'Food inventory :\n', myPlayer.inventory_food.count('bread'), 'x bread \n',
                  myPlayer.inventory_food.count('water'), 'x water \n')
        elif purchase == 'water' and myPlayer.gold >= 5:
            myPlayer.inventory_food.append('water')
            myPlayer.gold -= 5
            print(f'\n Gold = {myPlayer.gold}')
            print(f'Food inventory :\n', myPlayer.inventory_food.count('bread'), 'x bread \n',
                  myPlayer.inventory_food.count('water'), 'x water \n')
        elif purchase == 'leave':
            print(f'\n {world[myPlayer.location][NPCS]}:')
            print_talk(' Bye, hope to see you soon.', 0.03)
            main_game_loop()
        elif myPlayer.gold < 5:
            print(f'\n {world[myPlayer.location][NPCS]}:')
            print_talk('Im sorry, but you dont have that kind of money', 0.03)
        else:
            print('Invalid command')


# consumables
def eat_bread():
    if myPlayer.damage_taken > 0:
        heal = round(5+myPlayer.health_points * 0.25)
        myPlayer.damage_taken -= heal
        if myPlayer.damage_taken < 0:
            myPlayer.damage_taken -= myPlayer.damage_taken
        myPlayer.inventory_food.remove('bread')
        print('\nYou ate some bread and healed for '+str(heal))
        myPlayer.hp_mp_info()
        main_game_loop()
    else:
        print('\n You fell healthy')
        main_game_loop()


def drink_water():
    if myPlayer.mana_points_use > 0:
        replenish = round(5+myPlayer.mana_points * 0.25)
        myPlayer.mana_points_use -= replenish
        if myPlayer.mana_points_use < 0:
            myPlayer.mana_points_use -= myPlayer.mana_points_use
        myPlayer.inventory_food.remove('water')
        myPlayer.hp_mp_info()
        main_game_loop()
    else:
        print('\n You fell replenished')
        main_game_loop()


def fight_fidner():
    if world[myPlayer.location][NPC_FIGHT] and not world[myPlayer.location][ENEMY_NPC]['dead']:
        the_enemy.name = world[myPlayer.location][ENEMY_NPC]['NAME']
        the_enemy.enemytype = world[myPlayer.location][ENEMY_NPC]['ENEMYTYPE']
        the_enemy.health_points = world[myPlayer.location][ENEMY_NPC]['HEALTH']
        the_enemy.mana_points = world[myPlayer.location][ENEMY_NPC]['MANA']
        the_enemy.power = world[myPlayer.location][ENEMY_NPC]['POWER']
        the_enemy.armor = world[myPlayer.location][ENEMY_NPC]['ARMOR']
        the_enemy.attacktype = world[myPlayer.location][ENEMY_NPC]['ATTACKTYPE']
        fight_stats()
    else:
        print('No one to fight here')
        main_game_loop()





# gives info about the fight before it starts
def fight_stats():
    the_enemy.enemy_stats()
    while myPlayer.in_combat == False:
        yesno = input('Do you want to attack(y/n)?> ')
        if yesno == 'y':
            myPlayer.in_combat = True
            os.system('cls')
            combat()
        if yesno == 'n':
            main_game_loop()
        else:
            print('Invalid command')
            main_game_loop()


# When in combat
def combat():
    if the_enemy.health_points - the_enemy.damage_taken > 0:
        while myPlayer.player_attack_move == True:
            print('Combat: Your Move')
            print('Enemy stats:')
            fight_stats()
            print('your stats:')
            myPlayer.hp_mp_info()
            print('you are in combat, you got following options: "melee attack", "ability", "run", "help"'.center(cols))
            acceptable_actions_move = input('>').strip()
            if acceptable_actions_move == 'melee attack':
                myPlayer.melee_attack()
            elif acceptable_actions_move == 'ability':
                myPlayer.use_ability()
            elif acceptable_actions_move == 'run':
                myPlayer.attempt_run()
            elif acceptable_actions_move == 'help':
                combat_help()
            else:
                print('Invalid command\n')
                fumble = random.randint(0, 100)
                if fumble > 80:
                    print_talk('You fumble your move...')
                    myPlayer.player_attack_move = False
                    combat()
        else:
            print_talk('Enemy move')
            the_enemy.enemy_attack()
    else:
        print_talk('You have killed the enemy!')
        myPlayer.energi_points_use = 0
        world[myPlayer.location][ENEMY_NPC]['dead'] = True
        looter()


def looter():
    try:
        if not world[myPlayer.location][ENEMY_NPC]['looted'] and world[myPlayer.location][ENEMY_NPC]['dead']:
            the_enemy.inventory.append(world[myPlayer.location][ENEMY_NPC]['INVENTORY'])
            the_enemy.enemy_loot()
            print_talk('Do you want to loot the corpse?(y/n)\n')
            while not world[myPlayer.location][ENEMY_NPC]['looted']:
                yesno =input('>').lower().strip()
                if yesno == 'y':
                    myPlayer.inventory.append(world[myPlayer.location][ENEMY_NPC]['INVENTORY'])
                    the_enemy.inventory.remove(world[myPlayer.location][ENEMY_NPC]['INVENTORY'])
                    world[myPlayer.location][ENEMY_NPC]['looted'] = True
                    main_game_loop()
                elif yesno == 'n':
                    the_enemy.inventory.remove(world[myPlayer.location][ENEMY_NPC]['INVENTORY'])
                    main_game_loop()
                else:
                    print('Invalid action')
        else:
            print_talk('Nothing to loot \n')
    except:
        print_talk('Nothing to loot \n')
        pass


#Quesets
def lost_jewelry():
    if quests['lost jewelry'] is False:
        if 'A brown pouch' in myPlayer.inventory:
            print('innkeeper:\n')
            print_talk('WOW you got it!!  70 gold pieces for you my friend', 0.05)
            myPlayer.gold += 70
            myPlayer.inventory.remove('A brown pouch')
            quests['lost jewelry'] = True
        else:
            print(f'\n{myPlayer.name.upper()}:')
            print_talk('Hallo, how are you doing?', 0.05)
            print('\nInnkeeper:')
            print_talk('Im actually not doing very great...', 0.05)
            print_talk('Oh well, let me tell you what happend....\n'
                       'On monthly visit at the great city beyond the dark mountain, '
                       'shopping for inventory for my inn.\n'
                       'i was approached my a strange guy...', 0.07)
            print_talk('He held a small brown pouch. '
                       'He offered me a great amount of gold if i would bring the pouch with me back to my inn.\n'
                       'I could not resist the offer so i said yes.\n '
                       'He then told me that if i looked in the bag, i would be killed.\n i have never had problems '
                       'controlling my curiosity, and the amount of gold i would earn was to great to turn down.\n'
                       'He told me i would get payed when i got back to my inn', 0.07)
            print_talk('But on my way back, at the edge of the forest i was attacked my an ogre... '
                       'I had to flee as fast as i could, and i droped some of my inventory... '
                       'including the brown pouch...... \nThe ogre took th pouch... '
                       'You look like a man for the job, can you get the pouch for me? Ill pay you a good sum', 0.07)
            print(f'\n{myPlayer.name.upper()}:')
            print_talk('Im sad to hear what happened. Ill take care of the ogre..', 0.05)
    else:
        print(f'\n{myPlayer.name.upper()}:')
        print_talk('Hallo, how are you doing?\n', 0.05)
        print('\nInnkeeper:')
        print_talk('Im doing great\n', 0.07)
        print_talk('Thank you so much for finding the necklace of the.. '
                   'ehm i mean my precious necklace!\n', 0.06)
        print(f'\n{myPlayer.name.upper()}:')
        print_talk('your welcome! The necklace of?.\n', 0.05)
        print('\nInnkeeper starts serving another costumer:')
        print_talk('Hallo there traveler, would you like a pint!\n', 0.07)
        print(f'\n{myPlayer.name.upper()} thinking:')
        print_talk('Whats up with that guy?\n', 0.05)
        main_game_loop()


# handle if game is solved boss defeat etc
def main_game_loop():
    while myPlayer.game_won is False:
        promt()
    else:
        print('YOU WON!')


def setup_game():
    os.system('cls')
    print_talk('This is a game of quest and magic.'.center(cols), 0.05)
    print_talk('Before we move on, you gotta choose you character: Mage, Warrior, Rogue, Warlock.'.center(cols), 0.05)
    print_talk('If you what to know more about the characters write:'.center(cols), 0.05)
    print_talk('Info Mage , Info Warrior, Info Rogue, or Info Warlock'.center(cols), 0.05)
    print_talk('Go to Character selection type: select character'.center(cols), 0.05)
    # Character info
    while True:
        char_info = input('\n> ').lower().strip()
        if char_info == 'info mage':
            print("""
            Mage:
                Pysical stats: 

                Health points = 100
                Mana points = 400
                Armor = 10
                Energi = 50
                
                Ability:
                fireball, summon a big ball of flames that burns up to three close targets
                Damage = 65 , Mana use = 50""".center(cols))
        elif char_info == 'info warrior':
            print("""
            Warrior:
                Pysical stats:

                Health point = 500
                Mana points = 10
                Energi = 100
                armor = 60

                Ability:
                Slam, deals a high amount of damage.

            """.center(cols))
        elif char_info == 'info rogue':
            print("""

                Rogue:
                hp = 350
                mp = 10
                Energi = 300 
                Armor = 45

                Ability:
                Fast strike, a quick attack that stuns the enemy for one move:
                Energi cost = 50

            """.center(cols))
        elif char_info == 'info warlock':
            print("""

            hp = 250
            mp = 300
            armor = 25
            Energi = 50

            Ability:
                can summon a small demon to fight by your side.
           """.center(cols))
        elif char_info == 'select character':
            break
        else:
            print("Sorry, i dont understand that")
    # Character selection
    print('To choose a character write: Choose Mage , Choose Warrior, Choose Rogue, or Choose Warlock'.center(cols))
    while True:
        select_char = input('> ').lower().strip()
        if select_char == 'choose mage':
            myPlayer.char = 'Mage'
            myPlayer.health_points = 100
            myPlayer.mana_points = 400
            myPlayer.armor = 10
            myPlayer.energi_points = 50
            print('You have chosen the Mage.')
            break
        elif select_char == 'choose warrior':
            myPlayer.char = 'warrior'
            myPlayer.health_points = 500
            myPlayer.mana_points = 10
            myPlayer.armor = 60
            myPlayer.energi_points = 100
            print('You have chosen the Warrior.')
            break
        elif select_char == 'choose rogue':
            myPlayer.char = 'rogue'
            myPlayer.health_points = 350
            myPlayer.mana_points = 10
            myPlayer.armor = 45
            myPlayer.energi_points = 300
            print('You have chosen the Rogue.')
            break
        elif select_char == 'choose warlock':
            myPlayer.char = 'Warlock'
            myPlayer.health_points = 250
            myPlayer.mana_points = 200
            myPlayer.armor = 25
            myPlayer.energi_points = 50
            print('You have chosen the Warlock.')
            break
        else:
            print("Sorry, i dont understand that")
    myPlayer.name = input('Character name: ').strip()
    myPlayer.player_info()
    input('Hit Enter to continue> ')
    myPlayer.game_started = True

    # Introduction
    os.system('cls')
    print_talk('You have traveled far and wide, late night you arrived at a city. '
               'you stayed at the inn over night.\n'.center(cols), 0.01)
    print_talk('You overheard an argument between a clocked guy and the innkeeper early in the morning.\n'
               'you wake up, and walk out of your room.'.center(cols), 0.01)
    main_game_loop()


maximize_console()
cols, rows = shutil.get_terminal_size()
if myPlayer.game_started:
    main_game_loop()
else:
    title_screen()


