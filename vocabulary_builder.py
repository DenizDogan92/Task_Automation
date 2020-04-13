## Get vocabulary word of the day using wordsapi ##

import requests, os, argparse, random, json
from tkinter import *

jsonFile = "english_vocabulary.json"

# get word from wordsapi.com
def get_definition_from_web(word):
    url = "https://wordsapiv1.p.rapidapi.com/words"
    url = os.path.join(url, word)

    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"
    }

    response = requests.request("GET", url, headers=headers).json()

    results = response["results"]

    wordInfo = "Definitions:"

    defNo = 1
    for result in results:
        if ("definition" in result):
            definition = result["definition"]

            wordInfo += "\n%d. %s\n" % (defNo, definition)

            if("synonyms" in result):
                synonyms = result["synonyms"]
                synonyms = ", ".join(synonyms)
                wordInfo += "Synonyms: %s\n" % (synonyms)

            if("examples" in result):
                examples = result["examples"]
                exampleNo = random.randint(0, len(examples)-1)
                example = examples[exampleNo]
                wordInfo += "Ex: %s\n" % (example)

            defNo += 1

    add_word_to_file(word, wordInfo)

    return wordInfo

# get word from "english_vocabulary.json" file
def get_definition_from_file(word):
    if(word):
        if(os.path.isfile(jsonFile) and os.path.getsize(jsonFile)):
            with open(jsonFile) as jFile:
                data = json.load(jFile)
                if(word in data):
                    wordInfo = data[word]
                else:
                    print("Word '%s' does not exist in file %s" % (word, jsonFile))
                    wordInfo = ""
    else:
        wordInfo = ""
        if(os.path.isfile(jsonFile) and os.path.getsize(jsonFile)):
            with open(jsonFile) as jFile:
                data = json.load(jFile)
                wordId = random.randint(0,len(data)-1)
                word = list(data)[wordId]
                wordInfo = data[word]

    return word, wordInfo

# add word to "english_vocabulary.json" file
def add_word_to_file(word, wordInfo):
    # write word to json file for the first time
    if(not os.path.isfile(jsonFile) or not os.path.getsize(jsonFile)):
        data = {}
        data[word] = wordInfo
        with open(jsonFile, mode='w') as jFile:
            jFile.write(json.dumps(data, indent=2))
    # append word to existing json file
    else:
        with open(jsonFile) as jFile:
            data = json.load(jFile)
        data.update({word: wordInfo})
        with open(jsonFile, mode='w') as jFile:
            jFile.write(json.dumps(data, indent=2))

# delete word in "english_vocabulary.json" file
def delete_word_from_file(word):
    with open(jsonFile) as jFile:
        data = json.load(jFile)
        if(word in data):
            print("Deleting word '%s' in %s\n" % (word, jsonFile))
            del data[word]
            with open(jsonFile, "w") as jFile:
                jFile.write(json.dumps(data))
        else:
            print("Word '%s' not exist in %s\n" % (word, jsonFile))

# list words in "english_vocabulary.json" file
def list_words_in_file():
    print("Vocabulary Words:\n")
    with open(jsonFile) as jFile:
        data = json.load(jFile)
        words = data.keys()
        for word in words:
            print(word)
    print("")

def how_to_use():
    scriptName = __file__.split("/")[-1]
    usage = "python %s" % (scriptName + " [WORD] -o [OPTIONS]\n\n"
                                 "If no argument is given, it shows a random WORD from your dictionary\n"
                                 "If WORD argument is given, it shows the definition of the WORD and saves to your dictionary if not exist\n\n"
                                 "OPTIONS:\n"
                                 "  list : list WORDS in your dictionary" + "\n"
                                 "  delete" + " WORD : deletes the WORD from your dictionary\n"
                                 "  gui : show a random WORD from your dictionary in GUI")
    return usage

def main():
    parser = argparse.ArgumentParser(description="word definition", usage=how_to_use())
    parser.add_argument("-o", "--option", choices=["list", "delete", "gui"], help=argparse.SUPPRESS)
    parser.add_argument("word", nargs="*", help=argparse.SUPPRESS)

    args = parser.parse_args()
    word = args.word
    word = " ".join(word)
    option = args.option

    wordInfo = ""

    # if word exist in the vocabulary file retrieve from file else retrieve from wordsapi.com
    if(option == None):
        if(word):
            data = ""
            if(os.path.isfile(jsonFile) and os.path.getsize(jsonFile)):
                with open(jsonFile) as jFile:
                    data = json.load(jFile)
            if(word in data): # If word exist in the dictionary, retrieve from the file
                word, wordInfo = get_definition_from_file(word)
            else: # If dictionary does not contain the word, retrieve from web
                wordInfo = get_definition_from_web(word)
        else: # retrieve random word from file
            word, wordInfo = get_definition_from_file("")

    # list the vocabulary words in file
    elif(option == "list"):
        list_words_in_file()

    # delete the existing vocabulary word from file
    elif(option == "delete"):
        delete_word_from_file(word)
        list_words_in_file()

    # show random vocabulary word from file in a dialog box and ask the user if (s)he wants to keep/delete
    elif(option == "gui"):

        word, wordInfo = get_definition_from_file("")

        def keepButtonClicked():
            window.destroy()

        def deleteButtonClicked():
            delete_word_from_file(word)
            window.destroy()


        bgColors = ["#fce77d", "#292826", "#3d155f", "#4831d4", "#f0a07c", "#3c1a5b", "#fbeaeb", "#1d1b1b", "#243665", "#ec8b5e", "#8aaae5", "#ffe67c", "#161b21", "#080a52"]
        fgColors = ["#f96167", "#f9d342", "#df678c", "#ccf381", "#4a274f", "#fff748", "#2f3c7e", "#ec4d37", "#8bd8bd", "#141a46", "#ffffff", "#295f2d", "#f4a950", "#eb2188"]

        colorId = random.randint(0, len(bgColors)-1)
        bgColor = bgColors[colorId]
        fgColor = fgColors[colorId]

        window = Tk()
        window.resizable(False, False)
        window["bg"] = bgColor
        window.title("Vocabulary Time")

        definitionLabel = Label(window, text="Word: " + word + "\n\n" + wordInfo, bg=bgColor, fg=fgColor, font=("Helvetica", 16), justify=LEFT)
        definitionLabel.pack(side=TOP)

        keepButton = Button(window, text="Keep", bg=bgColor, fg=fgColor, font=("Helvetica", 12), command=keepButtonClicked)
        keepButton.pack(side=LEFT)

        deleteButton = Button(window, text="Delete", bg=bgColor, fg=fgColor, font=("Helvetica", 12), command=deleteButtonClicked)
        deleteButton.pack(side=RIGHT)

        window.mainloop()


    if(wordInfo and option != "gui"):
        print("Word: %s" % word)
        print("")

        print(wordInfo)

if(__name__ == "__main__"):
    main()