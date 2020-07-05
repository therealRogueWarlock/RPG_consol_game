
def innkeeper():
    line_1 = 'Innkeeper: '
    line_2 = 'Hallo there my friend, what can i do for you?'
    for x in line_1:
        sys.stdout.write(x)
        sys.stdout.flush()
        sleep(0.0)
    for x in line_2:
        sys.stdout.write(x)
        sys.stdout.flush()
        sleep(0.0)
    action = input('\n (sell, buy, talk, bye) > ').lower()
    acceptable_actions = ['sell','buy','talk','bye']
    while action not in acceptable_actions:
        print('unknown command, try another action or go to help.')
        action = input('> ').lower()
    if action == 'bye':
        print('Innkeeper: Bye bye, hope to see you soon')
        main_game_loop()
    elif action == 'sell':
        pass #define sell
    elif action == 'buy':
        pass  # define buy
    elif action == 'talk':
        pass #define talk
    main_game_loop()
