import threading
import time
from random import randint


class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(3):
            dep = randint(50, 500)
            self.balance += dep
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f'Пополнение: {dep}. Баланс: {self.balance}')
            time.sleep(0.001)

    def take(self):
        for i in range(3):
            take = randint(50, 500)
            print(f'Запрос на {take}')
            if take <= self.balance:
                self.balance -= take
                print(f'Снятие: {take}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                if not self.lock.locked():
                    self.lock.acquire()

bk = Bank(0)

th1 = threading.Thread(target=Bank.deposit, args=(bk, ))
th2 = threading.Thread(target=Bank.take, args=(bk, ))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
