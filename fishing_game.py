from random import randint
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Rolls_Dice():
    def __init__(self,d4,d6,d8,d10,d12,name):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12
        self.name = name

    def dice(self,number:int,sides:int)->str:
        result = []
        for _ in range(number):
            result.append(randint(1,sides))
        print(f"    {number}d{sides} rolled. {result} for a total of {sum(result)}")
        return sum(result)

    def roll(self,bonus=0,push=False):
        total = 0
        push_die = 0
        if push:
            push_die = 1
        if not self.d12 == 0:
            total += self.dice(self.d12+push_die,12)
            if push_die > 0: push_die -= 1
        if not self.d10 == 0:
            total += self.dice(self.d10+push_die,10)
            if push_die > 0: push_die -= 1
        if not self.d8 == 0:
            total += self.dice(self.d8+push_die,8)
            if push_die > 0: push_die -= 1
        if not self.d6 == 0:
            total += self.dice(self.d6+push_die,6)
            if push_die > 0: push_die -= 1
        if not self.d4 == 0:
            total += self.dice(self.d4+push_die,4)
            if push_die > 0: push_die -= 1
        total += bonus
        if not bonus == 0:  
            print(f"    {self.name} rolled for turn for total of {total}({total-bonus} + {bonus})")
        else:
            print(f"    {self.name} rolled for turn for total of {total}")
        return total    




class Fish(Rolls_Dice):
    def __init__(self,name:str, successes:int, failures:int, d4=0, d6=0, d8=0, d10=0, d12=0):
        self.name = name
        self.successes = successes
        self.failures = failures
        super().__init__(d4,d6,d8,d10,d12,self.name)


class Rod():
    def __init__(self,d4=0, d6=0, d8=0, d10=0, d12=0):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12

class Line():
    def __init__(self,pulls=0,d4=0, d6=0, d8=0, d10=0, d12=0):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12
        self.pulls = pulls

class Player(Rolls_Dice):

    def __init__(self,name:str,rod:Rod,line:Line):
        self.line_pull = line.pulls
        self.rod = rod
        self.line = line
        self.name = name
        d4 = self.rod.d4 + self.line.d4
        d6 = self.rod.d6 + self.line.d6
        d8 = self.rod.d8 + self.line.d8
        d10 = self.rod.d10 + self.line.d10
        d12 = self.rod.d12 + self.line.d12
        super().__init__(d4,d6,d8,d10,d12,self.name)


def fishing_battle(player:Player,fish:Fish):
    current_successes = 0
    current_failures = 0
    rounds = 0
    while current_successes < fish.successes and current_failures < fish.failures:
        rounds += 1
        print(f"ROUND {rounds}")
        fish_result = fish.roll()
        determination = 0
        push = False
        if current_failures >= 5:
            determination = current_failures - 4 #TO ADD BOUNUS EQUAL TO ROUNDS, ADD 'rounds' INSIDE 'player_roll()' FUNCTION
        if current_failures == fish.failures - 1 and not player.line_pull == 0:
            push = True
            player.line_pull -= 1
            print(f"{bcolors.WARNING}LINE PULL USED FOR EXTRA DIE. {player.line_pull} LINE PULLS REMAIN{bcolors.ENDC}")
        player_result = player.roll(determination,push)   
        if player_result >= fish_result:
            print(f"{bcolors.OKGREEN}    {player.name} wins round{bcolors.ENDC}")
            current_failures = 0
            current_successes += 1
        else:
            current_successes = 0
            current_failures += 1
            print(f"{bcolors.FAIL}    {fish.name} wins round{bcolors.ENDC}")

    print("FIGHT COMPLETE")
    if current_failures == fish.failures:
        print( f"{fish.name} WINS")
    else: 
        print(f"Player {player.name} WINS")
    print(f"TOTAL ROUNDS: {rounds}")

shitty_rod = Rod(d4=1)
basic_rod = Rod(d6=1)
super_rod = Rod(d10=1)
basic_line = Line(pulls=3)
fancy_line = Line(pulls=1,d4=1)

sun_fish = Fish("Sun Fish",2,5,2)
stergin = Fish("Sturgin",3,4,0,1,1)
northern = Fish("Northern",5,10,d12=2)
matt = Player("Matt",super_rod,basic_line)

fishing_battle(matt,stergin)