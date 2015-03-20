#Name: James Heneghan
#SID:  C00155861
#date: 13/11/14
#Lecturer: Paul Barry
#Assignment 1


#This python code takes in the words from the words file in the dict folder
#seperates them into two files one with three and more characters and one
#with seven or more characters for the base of the word game.



import re

#Putting words file into variable dictionary.
dictionary = '/usr/share/dict/words'

with open (dictionary) as words:
    for line in words:

#Then the new lines and 's and other special characters are removed.        
        line = line.strip()
        line = line.strip("'")
        if re.match("^[a-zA-Z0-9_]*$", line):

#Three words or more are placed into a file called 3 or more words.txt.        
            if len(line)>=3:
                with open('3_or_more_words.txt', 'a')as threewords:
                    print(line,file=threewords)

#Seven words or more are placed into a file called 7 or more words.txt.
            if len(line)>=7:
                with open('7_or_more_words.txt', 'a')as sevenwords:
                    print(line,file=sevenwords)
            
