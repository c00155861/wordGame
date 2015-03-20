#Name: James Heneghan
#SID:  C00155861
#date: 13/11/14
#Lecturer: Paul Barry
#Assignment 1

import random, re, contains
realWords=[]
badWords=[]
duplicateWords=[]

def check(guess,sourceWord,checker):

    for line in checker:
        line = line.strip()
        line = line.lower()
        sourceWord = sourceWord.lower()

        if guess in line and len(guess) == len(line) and contains.contains(sourceWord,guess) and guess != sourceWord:

            if guess not in realWords:
                realWords.append(guess)
                break
            
            else:
                duplicateWords.append(guess)
        elif guess in line and len(guess) == len(line) and guess not in badWords and not contains.contains(sourceWord,guess):
            #print("Bad word - adding to list")
            badWords.append(guess)
            #print(guess)
            #print(badWords)
         
    if guess == sourceWord:
        print("You typed in the source word so it does not count")
    
###########################################################################################################################################################


#http://stackoverflow.com/questions/1456617/return-a-random-word-from-a-word-list-in-python
#Selects a random word from the file and prints it to the screen
randomWord = [line.strip() for line in open('7_or_more_words.txt')]
sourceWord = random.choice(randomWord)


print('Your source word is: ',sourceWord)

print('\nMake 7 words from the source word\n')
guess1 = input('First guess: ')
guess2 = input('Second guess: ')
guess3 = input('Third guess: ')
guess4 = input('Fourth guess: ')
#guess5 = input('Fifth guess: ')
#guess6 = input('Sixth guess: ')
#guess7 = input('Seventh guess: ')


checker = open('3_or_more_words.txt','r')
check(guess1,sourceWord,checker)
checker.seek(0)

check(guess2,sourceWord,checker)
checker.seek(0)

check(guess3,sourceWord,checker)
checker.seek(0)

check(guess4,sourceWord,checker)
checker.close()
##check(guess5,sourceWord,checker)
#check(guess6,sourceWord,checker)
#check(guess7,sourceWord,checker)


print("REAL WORDS > >",realWords,"\n")
print("BAD WORDS > >",badWords,"\n")
print("DUPLICATE WORDS > >",duplicateWords,"\n")
