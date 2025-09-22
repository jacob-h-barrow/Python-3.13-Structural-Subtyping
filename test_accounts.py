from concurrent.futures import ThreadPoolExecutor
from typing import *

import datetime
import time
import random
import threading

type ATM_Action[**P, Date: datetime.datetime] = typing.Callable[typing.Concatenate[Date, P], bool | int]

class Account:
    reentrant_lock = threading.RLock()
    
    @staticmethod
    def check_account_number(account_number) -> bool:
        return bool(re.fullmatch(r'\d{10}', account_number))
    
    def __init__(self, account_number: str, balance: int = 0):
        if self.check_account_number(account_number):
            self.__account_number = account_number
        else:
            raise ValueError(f'{account_number} is not formatted correctly')
        
        self.__balance = max(balance, 0)
        
    @property
    def account_number(self):
        return self.__account_number
        
    @property
    def balance(self):
        with Account.reentrant_lock:
            return self.__balance
        
    @balance.setter
    def balance(self, new_amount: int):
        with Account.reentrant_lock:
            if new_amount >= 0:
                self.__balance = new_amount
            else:
                raise ValueError("Balance cannot be negative")
                
def out_of_band_atm_use(fxn):
    def inner(*args, **kwargs):
        res = fxn(*args, **kwargs)

        if res and res < 0:
            print(f'You had a successful transaction of {inner}\n\tbut now owe {inner * 0.02} at the door!')

    return inner

@final
class AtmBackend_With_OOB:
    account_numbers_used_today: typing.ClassVar[typing.Dict[str, int]] = {}
    
    @classmethod
    def add_account_number(cls, account_number: str) -> typing.NoReturn:
        cls.account_numbers[account_number] = cls.account_numbers.get(account_number, 0) + 1
        
    @classmethod
    @out_of_band_atm_use
    def act_upon(cls, account: Account, amount: int, timeout: float = 2.5, action: str='deposit') -> bool | int:
        response = False
                
        if cls.check_account(account):
            cls.add_account_number(account.account_number)
        else:
            return response

        if amount > 0:
            try:
                match action:
                    case 'deposit':
                        account.balance += amount
                        response = amount
                    case 'withdraw':
                        account.balance -= amount
                        response = -1 * amount
                    case _:
                        raise Exception(f'Cant use {action} action')
            except:
                return False

        return response
    
    @staticmethod
    def check_account(account: Account) -> typing.TypeIs[Account]:
        return isinstance(account, Account)
        
# Thread Synchronization
atm_semaphore = threading.Semaphore(2)  # Two ATMs available
emergency_stop = threading.Event()

# Dynamic barrier to match the number of transactions
transaction_barrier = threading.Barrier(1) #transaction_count)  

def atm_session(transaction_type, amount, account, atm):
    actions = []

    with atm_semaphore:
        if transaction_type == "withdraw":
            success = atm.withdraw(account, amount)
        elif transaction_type == "deposit":
            success = atm.deposit(account, amount)
        else:
            success = False
        
        print(f"{transaction_type.capitalize()} {amount}: {'Success' if success else 'Failed'}")
        actions.append((threading.current_thread().name, atm.number, account.account_number, amount, transaction_type, success))
        # Synchronization barrier: ensures all transactions reach this point before proceeding
        try:
            transaction_barrier.wait()
        except threading.BrokenBarrierError:
            pass  # Handle barrier error safely

    return actions

# Sample Execution
if __name__ == "__main__":
    atm = AtmBackend(1)
    account = Account("1234567890", 1000)
    
    transactions = [
        ("withdraw", 200, account, atm),
        ("deposit", 500, account, atm),
        ("withdraw", 300, account, atm),
        ("withdraw", 100, account, atm),
        ("deposit", 400, account, atm),
    ]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(atm_session, *args) for args in transactions]

    for f in futures:
        print(f.result())
