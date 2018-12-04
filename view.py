import os
import time



def header():
    os.system('clear')
    print('\n_________________________________________')
    print('\n  ********** Welcome to HEAVEN *******   ')
    print('\n_________________________________________')
    choice = input('\n\nSelect your wish:****\n\n[C]reate account****\n[L]ogin****\n[E]xit****\n\n').upper()
    return choice

def login_account(username):
    os.system('clear')
    print('\n_________________________________________')
    print('\n  ********** Welcome to {} *********   '.format(username))
    print('\n_________________________________________')
    select = input('\n\nSelect your wish:****\n\n1.Balance****\n2.Add Balance\n3.Trades****\n4.Positions\n5.Buy****\n' +
                        '6.Sell****\n7.Logout****\n\n')
    return select


