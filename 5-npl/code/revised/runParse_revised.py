import Parse_Revised as Parse

Parse.readParserDefinitions("sampleRules.dat")

global sentences
sentences = []

Parse.debug_print = False

def gather(sentence_string):
    global sentences
    sentences.append(sentence_string.rstrip().split(" "))

handle = open("sentences.txt", 'r')
for sentence in handle:
    gather(sentence)
handle.close()

for sentence in sentences:
    print
    Parse.parse(sentence)
