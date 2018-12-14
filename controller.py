import model
import os
import time
import sqlite3
import view
from model import Account, Trade
#from model import set_hashed_password


while True:
        choice  = view.header()
        if choice == 'C':
            username = input('Username: ')
            firstname = input('Firstname: ')
            lastname = input('Lastname: ')
            account_type = input('Account type - Admin or User - : ')
            password = input('Password: ')
            confirm_password = input('Confirm Password: ')
            if password == confirm_password:
                account = Account()
                account.username = username
                account.firstname = firstname
                account.lastname = lastname
                account.account_type = account_type
                account.set_hashed_password(password)
                account.set_new_id
                account.save()
                print("account added")
                time.sleep(1)
                #view.login_account(account.username)
            else:
                print('Try again!!')
                time.sleep(1)
        elif choice == 'L':
            username = input('Username: ')
            password = input('Password: ') 
            account = Account(username = username, password = password)
            _user = account.user_admin()
            if account:
                if _user:
                    while account:
                        select = view.login_admin(username)
                        if select == '1':
                            print('Your balance is {}'.format(round(account.balance,2)))
                            input()
                        elif select =='2':
                            amount = float(input('Amount: '))
                            account.balance += amount
                            account.save()
                            print('Success!!!')
                            input()
                        elif select == '3':
                            trades = account.get_trades()
                            for i in range(0,len(trades)):
                                print(trades[i])
                            input()
                        elif select == '4':
                            positions = account.get_positions()
                            for i in range(0,len(positions)):
                                print(positions[i])
                            input()
                        elif select == '5':
                            share = input('What share you want to buy?: ')
                            amount = int(input('Amount to wish buy?: '))
                            try:
                                account.buy(share, amount)
                                print('You bought {} of {} shares'.format(amount,share))
                            except ValueError:
                                print("No Such a Stock")
                            except TypeError:
                                print('Invalid Input')
                            input()
                        elif select == '6':
                            share = input('What share you want to sell?: ')
                            amount = int(input('Amount to wish sell?: '))
                            try:
                                account.sell(share, amount)
                                print('You sell {} of {} shares'.format(amount,share))
                            except ValueError:
                                print("No Such a Stock")
                            except TypeError:
                                print('Invalid Input')
                            input()
                        elif select == '7':
                            result = account.get_accounts()
                            #print(result)
                            #user = [x[1] for x in result]
                            #balance = [x[-1] for x in result]
                            #print(user)
                            #print(balance)
                            for i in range(0,len(result)):
                                print('Username {} and Balance is {}.'.format(result[i][1], result[i][-1]))
                            input()
                        elif select == '8':
                            account = False
                            print('Thank you!!! log out successful.')
                            time.sleep(2)
                            break
                        else:
                            print('Please choose from 1 to 7')
                            input()     
                else: 
                    while account:
                        select = view.login_account(username)
                        if select == '1':
                            print('Your balance is {}'.format(round(account.balance,2)))
                            input()
                        elif select =='2':
                            amount = float(input('Amount: '))
                            account.balance += amount
                            account.save()
                            print('Success!!!')
                            input()
                        elif select == '3':
                            trades = account.get_trades()
                            for i in range(0,len(trades)):
                                print(trades[i])
                            input()
                        elif select == '4':
                            positions = account.get_positions()
                            for i in range(0,len(positions)):
                                print(positions[i])
                            input()
                        elif select == '5':
                            share = input('What share you want to buy?: ')
                            amount = int(input('Amount to wish buy?: '))
                            try:
                                account.buy(share, amount)
                                print('You bought {} of {} shares'.format(amount,share))
                            except ValueError:
                                print("No Such a Stock")
                            except TypeError:
                                print('Invalid Input')
                            input()
                        elif select == '6':
                            share = input('What share you want to sell?: ')
                            amount = int(input('Amount to wish sell?: '))
                            try:
                                account.sell(share, amount)
                                print('You sell {} of {} shares'.format(amount,share))
                            except ValueError:
                                print("No Such a Stock")
                            except TypeError:
                                print('Invalid Input')
                            input()
                        elif select == '7':
                            account = False
                            print('Thank you!!! log out successful.')
                            time.sleep(2)
                            break
                        else:
                            print('Please choose from 1 to 7')
                            input()
            else:
                print('Bad credentials.Try again')
                time.sleep(2)

        elif choice == 'E':
            exit()
        else:
            print('Please choose one of them: C,L,E') 
            time.sleep(1)



          


