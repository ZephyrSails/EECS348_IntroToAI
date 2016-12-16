question = ['What', 'is', 'on', 'block17']
expecting = '(on ?x block17)'

class Rule:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern



RB = []
simpleRule = Rule('sentence1', ['What', 'is', '<relationship>', '<name>'])
RB.append(simpleRule)
simpleRule = Rule('relationship', ['on'])
RB.append(simpleRule)
simpleRule = Rule('name', ['block17'])
RB.append(simpleRule)

def invokeParser(question):
    for rule in RB:
        result = applyPattern(question, rule.pattern)
        if result:
            return result

    return False

def applyPattern(question, pattern):
    print question, pattern

    if not question or not pattern:
        # print 'failed'
        return not question and not pattern

    if goodToGo(question[0], pattern[0]):
        if pattern[1][0] == '<':
            pattern[1] = pattern[1][1:-1]
            for r in RB:
                if r.name == pattern[1]:
                    pattern[1] = r.pattern[0]
                    pattern = r.pattern + pattern[1:]
        else:
            pattern = pattern[1:]

        return applyPattern(question[1:], pattern)

def goodToGo(ele1, ele2):
    # print ele1, ele2
    if ele2 and ele2[0] == '<':
        ele2 = ele2[1:-1]
        for r in RB:
            if r.name == ele2:
                ele2 = r.pattern[0]

    return ele1 == ele2

print invokeParser(question)


# if __name__ == '__main__':
#     invokeParser(question)
