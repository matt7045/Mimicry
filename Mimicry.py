#Markov would be proud.

import random
from math import ceil

#Splits a file into a long list of words
def _splitFile( file_name : str ):
    #Save the text in a buffer
    with open(file_name,'r') as f:
        text=f.read()
    #Get all length n word groups, and count how often
    # they occur in our text. Let's assume that punctionation
    # are their own words, too.
    textList=[]
    currentWord=""
    for i in range(len(text)):
        currentChar=text[i]
        #If we have a word in our buffer, and just encountered whitespace,
        # Save that word in our buffer and wipe it
        if (currentChar.isspace()) and (currentWord):
            textList.append(currentWord)
            currentWord=""
        #Otherwise, if we have just encountered punctiation, add that
        # punctuation to our text list
        elif (currentChar in ['?','!',',','.','-']):
            if (currentWord):
                textList.append(currentWord)
            textList.append(currentChar)
            currentWord=""
        #Lastly, if we haven't encountered whitespace, or punctuation,
        # tack on this letter to our current word
        elif not(currentChar.isspace()) and not(currentChar in ['?','!',',','.','-']):
            currentWord+=currentChar
    return(textList)

#Groups all the words in a list, into groups of n. Also counts how frequently that
# group of words appears.
def _groupWords( word_list : list, group_length):
    n = group_length
    textList = word_list
    groups=[]
    groupFrequencies={}
    #For every word in our file...
    for i in range(0,len(textList)-n):
        wordGroup=[]
        #Get the group of words in the slice
        for j in range(n):
            wordGroup.append(textList[i+j])
        #Save the group of words as a tuple, in a list
        groups.append(tuple(wordGroup))
        #Increment our counter for this specific word group
        wordGroup = ' '.join(wordGroup)
        try:
            groupFrequencies[wordGroup]+=1
        except:
            groupFrequencies[wordGroup]=1
    return(groupFrequencies)

#Creates a number of sentences, by "stringing together" groups
def _generateSentences(number_of_sentences : int, group_distribution : dict):
    group_list = []
    #Convert the groupDistribution into two lists; a list of groups/word lists,
    # and a group of how frequently those word lists occur in the text
    groups = []
    counts = []
    [(groups.append(group.split()), counts.append(count)) for group, count in group_distribution.items()]
    #Pick a likely way to start a sentence
    sentence_starter_groups = []
    sentence_starter_counts = []
    [ (sentence_starter_groups.append(group.split()), sentence_starter_counts.append(count) ) for group, count in group_distribution.items() if ( group[0].isupper() or (group[0] in ['.','?','!'] ) ) ]
    group_list.append(random.choices(sentence_starter_groups, weights=sentence_starter_counts)[0])
    #Now, build a beautiful saga, based off that original starting group of words
    length_of_group = len(groups[0])
    overlap   = ceil(length_of_group/2)#Defines how much "overlap" we want between groups. More overlap helps to make things "coherent"
    sentences_constructed = 0
    #Until we have constructed enough sentences...
    while sentences_constructed < number_of_sentences:
        #Get the last half of our most recent word group
        current_tail = group_list[-1][-overlap:]
        #Look for all the groups that START with that sequence of words...
        possible_groups       = []
        possible_group_counts = []
        for group, count in group_distribution.items():
            if group.split()[:overlap] == current_tail:
                possible_groups.append(group.split())
                possible_group_counts.append(count)
        #Pick a random one, but make it more likely depending on it's count
        new_group = random.choices(possible_groups, possible_group_counts)[0]
        group_list.append(new_group)
        #If there's punctuation in the thing we just added, we just finished a sentence :o
        if ('.' in new_group) or ('!' in new_group) or ('?' in new_group):
            sentences_constructed += 0.5
    #Once we have enough sentences, piece them together into one long string
    output_string = ' '.join([' '.join(group[:(overlap-(length_of_group%2))]) for group in group_list])
    #Remove the whitespace that gets "tacked on" to the front of the punctuation...
    punctuation = ['?','!',',','.','-']
    for symbol in punctuation:
        output_string = output_string.replace(" "+symbol, symbol)
    #Chomp off the words that are after out last sentence
    last_index = max(output_string.rfind('.'), output_string.rfind('?'), output_string.rfind('!'))
    output_string = output_string[:(last_index+1)]
    #If our sentence starts with punctuation, undo that oopsie
    if output_string[1] == ' ':
        output_string = output_string[2:]
    #Return our formatted output string
    return(output_string)

#Mimics the pattern of writing present in file_name_to_mimic
def mimic(file_name_to_mimic, number_of_sentences_to_produce, group_length = 5):
    attempts = 0
    while attempts < 10:
        try:
            word_list  = _splitFile(file_name_to_mimic)
            group_list = _groupWords(word_list, group_length)
            output     = _generateSentences(number_of_sentences_to_produce, group_list)
            return(output)
        except IndexError as e:
            print(e)
            attempts += 1
    return('Think for yourself!')
