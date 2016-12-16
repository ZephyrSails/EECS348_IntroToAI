# This reads in a file of parse rules, builds up the knowledge base and then uses them to
# parse questions into patterns that can be used to "Ask" questions.

# We need a structure for Rules.  They need a name, a pattern and a query output. A rule can
# be defined just by its name
import re

class Rule:

    def __init__(self, name, pattern = [], action = "", value = "" ):
        self.name = name
        self.pattern = pattern
        self.action = action
        self.value = value

    def show(self):
        print "\n" + self.name + ":",
        print self.pattern

    def __str__(self):
        return '<Rule, name: %s, pattern: %s, action: %s, value: %s' %(self.name, self.pattern, self.action, self.value)

class Disjunct:

    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return '<Disjunct %s>' % self.elements

# a A couple of globals, including one that allows us random access to rules by name.

global RB
RB = []
global index_RB
index_RB = {}


# Reading in a file of rule definitions, building the rule and replacing in any internal
# patterns with new rules.

# readParseRules reads in a set of rule definitions, tokenizes everything and then hands the
# configuration elements (name, pattern, action, and arguments) to the parse rule builder

def readParseRules(file):
    file_handle = open(file, "r")
    line = file_handle.readline()
    while line != "":
        rule = {}
        while ":" in line:
            label, value = line.split(":")
            # print label, value
            rule[label] = value.rstrip("\n").strip(" ")
            # print value.rstrip("\n").strip(" ")
            line = file_handle.readline()

        if len(rule.keys()) >= 5:
            buildParseRule(rule["Name"], rule["Pattern"], rule["Type"], rule["Action"], rule["Value"])
        line = file_handle.readline()
    file_handle.close()


# buildParseRule constructs a new parse rule and adds it to the rule base. If there is a
# a pattern embedded in the top level pattern, it replaces the reference to the pattern with
# the actual parse rule.  If there is a reference to a rule that has not been built yet, it
# builds an empty version of the rule so that when it is defined it will already be embedded in
# the elements that reference it.

# It also checks to see if an earlier rule built a stub of it.  If so, the pattern is added to
# the existing stub. If not, it builds the new rule from scratch.

def buildParseRule(name, pattern, type, action, value):
    print "\nBuilding new rule: " + name
    print "Pattern :",
    print pattern
    pattern = map(lambda x: buildOrFindRuleFromName(x), pattern.split(" "))
    if index_RB.get(name, False):
        print "Found stubbed out rule: " + index_RB[name].name
        # print index_RB[name]
        # print "Adding pattern:",
        print pattern
        index_RB[name].pattern = pattern
        index_RB[name].action = action
        index_RB[name].value = value
        print "Now it becomes"
        print index_RB[name]
        # print "Found stubbed out rule: " + index_RB[name].name
    else:
        new_rule = Rule(name, pattern, action, value)
        if type == "Sentence":
            RB.append(new_rule)
        index_RB[name] = new_rule
        print "Adding pattern:",
        print pattern


 # buildOrFindRuleFromName tests to see if an element is a reference (i.e., it is in brackets)
 # and if it is, it checks to see if the rule referenced already exists. If it does, it returns
 # it.  If it is a reference to a rule that does not exist yet, it builds out a stub for it.
 # Otherwise, it just returns the element directly.

def buildOrFindRuleFromName(element):
    if "|" in element:
        return Disjunct(map(lambda x: buildOrFindRuleFromName(x), element.split("|")))
    if element[0] != "<":
        return element
    elif index_RB.get(element[1:-1], False):
        return index_RB[element[1:-1]]
    else:
        print "Stubbing out rule: " + element[1:-1].capitalize()
        new_rule = Rule(element[1:-1])
        index_RB[element[1:-1]] = new_rule
        return new_rule


# parse takes a question and returns the representation of the query that you need to run
# to answer it

def parse(question):
    global output
    output = []

    print "Parsing "+ " ".join(question)
    for rule in RB:
        result = checkPattern(question, rule.pattern)

        print 'result: %s' % str(result)
        if result:
            output.append(rule.value)
            for x in output:

                res = []
                for statements in x[1:-1].split('] ['):
                    stat = []
                    for statement in statements[1:-1].split(') ('):
                        # print represent
                        stat.append(replaceValues(statement.split(), result))
                    res.append(stat)

            print res
            return res
    return False



# Check pattern takes a question (or other sentence) and a pattern and checks to see if
# there is a match between the two.  It iterates through the two lists until one or the other
# is exhausted.  If both are done, there is a match.  If one one is done, there is not.

# If an elements fail to match, then there is a failure as well.

# Before testing, checkPattern calls expandPattern to expands the first element of the
# pattern to see if it is a rule, a disjunct of possibilities or just a string. No matter
# expandPattern will return a list of patterns that will then be iterated through.

def checkPattern(question, pattern):

    global output

    if len(question) == 0 or len(pattern) == 0:
        if len(question) == 0 and len(pattern) == 0:
            return {}
        else:
            return False
    print "\nChecking: " + " ".join(question)
    print "Against: ",
    print pattern
    name, patterns = expandPattern(pattern)

    # print name, patterns
    for pat in patterns:
        # print "\tMatching: " + question[0] + "/" + pat[0],
        if isinstance(pat[0], Rule) or question[0] == pat[0]:

            if isinstance(pat[0], Rule):

                result = checkPattern(question[0:], pat[0:])
            else:
                result = checkPattern(question[1:], pat[1:])

            if result != False:
                if name != "NoOp":
                    result[name] = question[0]
                    print name.capitalize() + " is " + question[0]

                    if index_RB[name].action == "Ask":
                        output.append(index_RB[name].value)
                    elif index_RB[name].action == "AddBinding":
                        value = index_RB[name].value[1:-1].split()
                        result[value[0][1:-1]] = value[1]

                return result
        else:
            print "...no match"
    return False

# Expand pattern expands the leading edge of a pattern (the first element) and always returns
# a list of possibilities.  This means that the first element of an expanded pattern is always
# a literal that can be matched against a literal in the the question.

def expandPattern(pattern):
    name = "NoOp"
    if isinstance(pattern[0], Rule):
        name = pattern[0].name
        if len(pattern) > 1:
            expansions = [pattern[0].pattern + pattern[1:]]
        else:
             expansions = [pattern[0].pattern]
    elif isinstance(pattern[0], Disjunct):
        # expansions = map(lambda x: [x] + pattern[1:], pattern[0].elements)
        if len(pattern) > 1:
            expansions = map(lambda x: [x] + pattern[1:], pattern[0].elements)
        else:
            expansions = map(lambda x: [x], pattern[0].elements)
            return name, expansions
    else:
        return name, [pattern]
    final_list = []

    for pattern in expansions:
        if len(pattern) != 0:
            binding, full_list = expandPattern(pattern)
            final_list = full_list + final_list
    return name, final_list


def replaceValues(thing, bindings):

    if isinstance(thing, str):
        return bindings.get(thing[1:-1], thing)
    else:
        return map(lambda x: replaceValues(x, bindings), thing)
