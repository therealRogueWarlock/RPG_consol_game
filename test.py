

def title_screen_selections():
    option = input('> ').lower().strip()
    if option == 'play':
        print('setup_game()')
    elif option == 'help':
        print('help_menu()')
    elif option == 'quit':
        print('sys.exit()')
    else:
        print('please enter a valid command.')





