## Michael Bachman
## CIT592
## expectedBullets
## Due: Thursday, 15 Oct 2015

import math
import random
import itertools
import sys
import matplotlib.pyplot as plt
from pprint import pprint

def mix(n):
## shuffles any list
    random.shuffle(n)
    return n

def compare(a, b):
#compares list indices. order matters
    y = sum(i == j for i, j in zip(a,b))
    return y


def yesHandler(answer):
# solicits user's desire to play again
# yes/ no code from Stackoverflow: http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input--from Douglas Adams
    if answer and answer[0].lower() != 'y':
        print('Thanks for checking your hats with us. The new owners surely love them!')
        exit(1)
    else:
        return True

def expectedVal(d, div):
#calculate expected value
    s = 0
    for k, v in d.items():
        s = s + (k * (v/ div))
    return float(s)


def theoreticalEV(lim, tries):
#Optional code to test theoretical Expected Value
    n = 1
    e = math.e
    a = []
    for n in range(1, lim + 1):
        a.append((tries / ((math.factorial(n)*e))/tries))
        n += 1
    return a
        

def main():
    print("Welcome to the Hat check.")

    y_or_n = True
    while y_or_n: 
        partyMembers = int(input("How many people are in your party? "))
        iterate = int(input("How many times would you like to run through this simulation? "))

        ## Variables
        keys = list(range(1, (partyMembers + 1)))
        values = list(range(1, (partyMembers +1)))
        shuffledValues = list(range(1, (partyMembers +1)))
        indexCounter = [0] * partyMembers 
        baseDict = dict(zip(keys,indexCounter))
        newList = []
        y_or_n =""
        eVal = float(0.0)
        
        ## compares the original hat distribution to each iterative distribution
        i=1
        for x in range(1, (iterate + 1)):
            hatsReturned = mix(shuffledValues)
            distribution = compare(hatsReturned, values)
            
            #updates the value of the corresponding key
            baseDict[distribution] = baseDict.get(distribution,0) + 1
            
            newList.append(distribution)
            i += 1
        ## Validate distribution frequency
        print(baseDict)
        
        eVal = expectedVal(baseDict, iterate)
        print("Expected number of correctly returned hats = ", eVal)
        print("")

        ## Probability Distribution for qty of hats being returned to their
        ## rightful owner
        
        prob = (theoreticalEV(partyMembers, iterate))
        
        lastDict = dict(zip(keys, prob))
        pprint(lastDict)


        print("to continue, please close the graph that appears on your screen.")
        
            
    

        ## Labeling Graph
            ## http://matplotlib.org/users/text_intro.html
        fig = plt.figure()
        fig.suptitle('HW 5: Hats', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)
        ax.set_title('Derangement and the Deranged Hat-Checker')

        ax.set_xlabel('Number of owners to whom the Checker delivers the correct hat')
        ax.set_ylabel('Agg. Dist. of #times Checker returns hats to right owner(s)')

        ax.text(0.95, 0.8, 'Tries = %d' %iterate,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='green', fontsize=15)

        ax.text(0.95, 0.75, 'Party Members = %d' %partyMembers,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='red', fontsize=10)

        ax.text(0.95, 0.7, 'Expected correctly returned hats = %f' %eVal,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='black', fontsize=10)

        ## Histogram (credit to StackOverflow for how-to on plotting histogram from dictionary)
        plt.bar(range(len(baseDict)), baseDict.values(), align = 'center')
        plt.xticks(range(len(baseDict)), list(baseDict.keys()))
        plt.show()

        y_or_n = input("would you like to check hats with me? [y/n]").lower().strip()
        yesHandler(y_or_n)
        

if __name__ == "__main__":
    main()
