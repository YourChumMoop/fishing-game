
from random import randint


class bcolors:
    """
    Allows the addition of colors to print statements. Be sure for each code used, to end it with the ENDC
        
    Example: ```print(f"{bcolors.HEADER}This is a test{bcolors.ENDC}")```
    """
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
    """
    Interface for dice-rolling functionality for other classes.
    Args:
        d4,d6,d8,d10,d12: number or each respective dice
        name: name passed down for logs
    """
    def __init__(self,d4:int,d6:int,d8:int,d10:int,d12:int,name:str):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12
        self.name = name

    def dice(self,number:int,sides:int)->int:
        """
        Method for rolling dice. Returns a sum of dice rolled.
        Args:
            number: The number of dice to roll
            sides: The number of sides on each die
        """
        result = []
        for _ in range(number):
            result.append(randint(1,sides))
        print(f"    {number}d{sides} rolled. {result} for a total of {sum(result)}")
        return sum(result)

    def roll(self,bonus=0,push=False):
        """
        Method for rolling die for each type and number of dice of the parent class.
        Args:
            bonus: bonus to add to rolls.
            push: If a roll is pushed, it rolls an extra of the highest die rolled.
        """
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
    """
    # Fish
    creates a fish for fishing battle. 
    
    Extends ```Rolls_dice()``` for dice capabilities
    Args:
        name: name of fish
        successes: number of successful rounds of 
        
            dice rolls needed to catch the fish
        failures: number of failures allowed by the 
            
            player before the fish is no longer catchable
        d4,d6,d8,d10,d12: number of each dice that this fish will roll when trying to catch
    """
    def __init__(self,name:str, successes:int, failures:int, d4=0, d6=0, d8=0, d10=0, d12=0):
        self.name = name
        self.successes = successes
        self.failures = failures
        super().__init__(d4,d6,d8,d10,d12,self.name)


class Rod():
    """
    # Rod
    creates a rod item for augmenting the Player.
    Args:
        d4,d6,d8,d10,d12: used to pass dice bonuses for Player rolls.
    """
    def __init__(self,d4=0, d6=0, d8=0, d10=0, d12=0):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12

class Line():
    """
    # Line
    creates a fishing line for augmenting the Player. 
    
    Fishing lines also allow for pulls, which let you 
    
    add a bonus dice to a role, with limited uses per fishing battle.
    Args:
        pulls: number of times you can add one additional 
        
            die to your roll in an attempt to succeed.
            
        d4,d6,d8,d10,d12: used to pass dice bonuses for Player rolls.
    """
    def __init__(self,pulls=0,d4=0, d6=0, d8=0, d10=0, d12=0):
        self.d4 = d4
        self.d6 = d6
        self.d8 = d8
        self.d10 = d10
        self.d12 = d12
        self.pulls = pulls

class Player(Rolls_Dice):
    """
    # Player
    creates a Player, who uses equipment to augment dice rolls for 
    
    catching fish. Extends ```Rolls_Dice``` method for dice rolling capabilities.
    Args:
        name: name of player
        rod: Fishing rod player has equipped
        line: Fishing line player has equipped
    """
    def __init__(self,name:str,rod:Rod,line:Line):
        """
        On init, we populate d4-d12 with values made from the dice 
        
        values of the fishing rod and line. we also get the number 
        
        for pulls from the fishing line, and pass the player name 
        
        to ```Rolls_Dice()``` methods
        """
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
    """
    # Fishing Battle
    Function for having a player attempt to catch a fish.

    This function loops through comparing a Player's

    Dice roll vs a fish's dice roll until a number

    of successes or failures, determined by the fish,

    are met.

    Args:
        player: the Player class player
        fish: the Fish class fish
    """

    # Set up current failures and successes to compare later to the fish's
    current_successes = 0
    current_failures = 0
    rounds = 0

    # Loop until current_successes equals fish successes, or current_failures equals fish.failures
    while current_successes < fish.successes and current_failures < fish.failures:
        rounds += 1
        print(f"ROUND {rounds}")
        # Have the fish roll it's dice, and store the result.
        fish_result = fish.roll()

        # Set default values for augmenting the player roll later
        determination = 0
        push = False

        # Here we have logic to trigger at certain points in the battle
        # If the player is losing too many times in a row, they get a bonus to their roll equal to an excess of 4 failures
        if current_failures >= 5:
            determination = current_failures - 4 

        # If we get to a point where there is only one more failure before losing, and the player hasn't used all their
        # line pulls, have the next player roll be pushed, so they roll an additional die
        if current_failures == fish.failures - 1 and not player.line_pull == 0:
            push = True
            player.line_pull -= 1
            print(f"{bcolors.WARNING}LINE PULL USED FOR EXTRA DIE. {player.line_pull} LINE PULLS REMAIN{bcolors.ENDC}")
        
        # If neither, one, or both of the the conditions trigger above, they all use the same player roll, and store the
        # result to compare later.
        player_result = player.roll(determination,push)

        # Compare the results, and determine who the winner is   
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