import Parse

Parse.readParseRules("parseRules.dat")

print '------- Rule Base -------'
for key in Parse.index_RB:
    print Parse.index_RB[key]
# print Parse.index_RB
print '------- Rule Base End -------'
print Parse.index_RB['colorValue'].pattern[0]
print Parse.index_RB['attributeValue'].pattern[0]

questions = [
    "Block1 is blue",

    "What is the color of Block1",
    "What is the shape of Block1",
    "What is the size of Block1",
    "What is Block1",

    "What color is Block1",

    "What blocks are blue",
    "What spheres are blue",

    "What blocks is blue",
    "What spheres is blue",

    "What is on Block1",
    "What is over Block2",
    "What is bigger than Block2",

    "Where is Block1"]

results = []
for question in questions:
    results.append(Parse.parse(question.split()))

print '------- Result -------'
for i, result in enumerate(results):
    print '%s -> %s' % (questions[i], result)
    # print result

# ask question
# put order
#



# Parse.parse(question_5)
