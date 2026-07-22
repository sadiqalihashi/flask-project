# class Person:
#     def __init__(self,name,age,gender):
#         self.name = name
#         self.age = age
#         self.gender = gender

#     def talks(self,words):
#         print(f"{self.name} talks and says {words}")



# person1 = Person("James",29,"Male")
# print(type(person1))
# print(person1.name)
# print(person1.age)
# print(person1.gender)
# person1.talks("Hello, this is OOP ")


# person2 = Person("Jane",25,"Female")
# print(type(person2))
# print(person2.name)
# print(person2.age)
# print(person2.gender)
# person2.talks("Hi, this is Python")

class Bankaccount:
    def __init__(self,account_number,balance,owner,name,date_opened):
         self.account_number = account_number
         self.balance = balance
         self.owner = owner
         self.name = name
         self.date_opened = date_opened
    
    def deposit(self,amount):
        print(f"{self.name} added amount is {amount}")
    def withdraw(self, amount):
        print(f"{self.name} amount withdrawn is{amount} ")
    def display_info(self):
        print(f"{self.name}this is your balance{self.balance}this is the date_opened{self.date_opened} ")


account1 = Bankaccount("123456", 1000, "John Doe", "John's Savings", "2026-01-01")
account2 = Bankaccount("789012", 500, "Jane Smith", "Jane's Checking", "2026-02-15")

account1.deposit(400)
account1.withdraw(300)
account1.display_info()

account2.deposit(200)
account2.withdraw(100)
account2.display_info()





