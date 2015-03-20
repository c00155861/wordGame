import random, re, contains, datetime, time
from flask import Flask, render_template, url_for, request, redirect, Markup, flash, session
from threading import Thread
import sys
import logging
#from operator import itemgetter
app = Flask (__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == "__main__":
    app.run(debug = True)

guessWords = []

realWords=[]
badWords=[]
duplicateWords=[]



@app.route('/')
def displayHome():
    return render_template("home.html",
                           the_title = "Welcome to my word game",
                           web_game = url_for( "startGame"),
                           score_board = url_for("printScoreBoard"))

###########################GUESS THE WORDS#########################################################################################################################################


@app.route('/wordGame')
def startGame():
    session["startTime"] = time.time()
    randomWord = [line.strip() for line in open('7_or_more_words.txt')]
    session['sourceWord'] = random.choice(randomWord)
    session['submission'] = False

    return render_template("wordGame.html",
                           the_title="Good Luck!",
                           source_word = session.get("sourceWord"),
                           get_words = url_for( "gameResults"))


###########################GETS THE WORDS#########################################################################################################################################


@app.route('/gameResult',methods =["POST"])
def gameResults():
    guessWords=[]
    #realWords=[]
    #badWords=[]
    #duplicateWords=[]
    session['submission'] = False
    
    guessWords.append(request.form['guess1'])
    guessWords.append(request.form['guess2'])
    guessWords.append(request.form['guess3'])
    guessWords.append(request.form['guess4'])
    guessWords.append(request.form['guess5'])
    guessWords.append(request.form['guess6'])
    guessWords.append(request.form['guess7'])

    checker = open('3_or_more_words.txt','r')

    #for word in guessWords:
    #    check(word,checker)
    #    checker.seek(0)
    resultList = check(guessWords, checker)
    session["endTime"] = time.time()
    session["yourTime"] = session.get("endTime") - session.get("startTime")
    if len(resultList[0]) == 7:
        return render_template("winResults.html",
                               the_title="You Win!!!",
                               the_time = round(session.get("yourTime"),2),
                               good_words = resultList[0],
                               set_winners = url_for("scoreBoard"))



    else:  
        return render_template("loseResults.html",
                               the_title="You Lost!!!",
                               bad_words = resultList[1],
                               duplicate_words = resultList[2],
                               home = url_for("displayHome"),
                               new_game = url_for("startGame"))
    
        
        
    


#########################CHECK THE WORD###########################################################################################################################################


def check(guessWords,checker):
    realWords=[]
    badWords=[]
    duplicateWords=[]
    

    for guess in guessWords:
        realWordFound = False;
        for line in checker:
            line = line.strip()
            line = line.lower()
            sourceWord = session.get("sourceWord").lower()

            if guess in line and len(guess) == len(line) and contains.contains(sourceWord,guess) and guess != sourceWord:

                if guess not in realWords:
                    realWords.append(guess)
                    realWordFound = True;
                    break
                
                else:
                    duplicateWords.append(guess)
                    realWordFound = True;
                    break
                
                    
            elif guess in line and len(guess) == len(line) and guess not in badWords and not contains.contains(sourceWord,guess):
                badWords.append(guess)
                realWordFound = True;
                break
                
        checker.seek(0)
        if realWordFound == False and guess != sourceWord:
            badWords.append(guess + " is not a real word")
        if len(guess) < 3:
            badWords.append(guess+" is the less than 3 characters so it does not count")
        if guess == sourceWord:
            badWords.append(guess+" is the source word so it does not count")

    return [realWords, badWords, duplicateWords]
    
        

##########################HIGH SCORE##########################################################################################################################################
#REF: http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(scringList): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(scringList, key = alphanum_key)
	
	
@app.route('/scores',methods =["POST"])
def scoreBoard():
    

    if session.get('submission')==False:
        t = Thread(target=update_log, args=(session.get("yourTime"),request.form['name']))
        t.start()
        t.join()
        session['submission'] = True

    scoresList = [line.strip() for line in open('highScore.log','r')]
    scoresList = natural_sort(scoresList)


    
    ranking = scoresList.index(str(round(session.get("yourTime"),2)) + " " + request.form['name'])+1
    
    return render_template("scoreBoard.html",
                           the_title="Score Board",
                           new_game = url_for("startGame"),
                           scores = scoresList[0:10],
                           home = url_for("displayHome"),
                           position = ranking)




@app.route('/scoreBoard')
def printScoreBoard():

    scoresList = [line.strip() for line in open('highScore.log','r')]
    scoresList = natural_sort(scoresList)
    
    return render_template("highScore.html",
                           the_title="Score Board",
                           new_game = url_for("startGame"),
                           home = url_for("displayHome"),
                           scores = scoresList[0:10],)

##########################UPDATE HIGH SCORE FILE####################################################################################################################################

def update_log(score, name):
    #time.sleep(5)
    with open('highScore.log', 'a') as log:
        print(round(score,2),name, file=log)
        


app.config['SECRET_KEY'] = 'thisismysecrectkey'

