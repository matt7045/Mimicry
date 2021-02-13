import Mimicry

#Get some useful input from the user
filename            = input('File to Learn From (located in text_dumps folder): ')
number_of_sentences = int(input('Number of sentences to produce:' ))
group_length        = 5
#Make sure our file ends in .txt
if filename[-4:] != '.txt':
    filename=filename+'.txt'
directory_and_filename  = "text_dumps/"+filename
#Create our fake sentences!
sentences = Mimicry.mimic(directory_and_filename, number_of_sentences, group_length)
#Print them out a reasonable amount at a time
for i in range(0, len(sentences), 320):
    print(sentences[i:(i+320)])
    if (len(sentences)-i)>320:
        input('Press ENTER to see more...')
