from facts_and_rules import *
from read import *
import copy


class KB(object):
    def __init__(self, file_name, verbose=False):
        tokenized_facts, tokenized_rules = read_tokenize(file_name)
        # print tokenized_facts, tokenized_rules
        self.KB = []
        self.RB = []
        self.verbose = verbose

        for f in tokenized_facts:
            if self.verbose: print f
            self.AssertFact(Statement(f))

        for r in tokenized_rules:
            if self.verbose: print r
            self.AssertRule(Rule(r[0], r[1]))


    def printFacts(self):
        """
        print all the fact
        """
        for f in self.KB:
            if self.verbose: print f.pretty()
            # print '\t %s, %s' % (str([l.pretty() for l in f.facts]), str([l.pretty() for l in f.rules]))


    def printRules(self):
        """
        print all the rule
        """
        for r in self.RB:
            if self.verbose: print r.pretty()
            # print '\t %s, %s' % (str([l.pretty() for l in r.facts]), str([l.pretty() for l in r.rules]))


    def AssertFact(self, fact):
        """
        Assert a fact, and infer new info from this
        """
        self.KB.append(fact)
        self.inferFromFact(fact)


    def inferFromFact(self, fact):
        """
        Reasoning new fact from existing fact
        """
        for r in self.RB:
            bindings = match(r.lhs[0], fact)
            if bindings != False:
                if len(r.lhs) == 1:
                    if r.type == 'Assert':
                        newStatement = Statement(instantiate(r.rhs.full, bindings))
                        fact.add_fact(newStatement)
                        self.AssertFact(newStatement)
                    else:
                        # N is used to indicate how is this fact is added,
                        # used mainly in retracting
                        newStatement = Statement(instantiate(r.rhs.full, bindings), 'N')
                        fact.add_fact(newStatement)
                        self.Retract(newStatement.full)
                else:
                    tests = map(lambda x: instantiate(x.full, bindings), r.lhs[1:])
                    rhs = instantiate(fact.full, bindings)
                    newRule = Rule(tests, rhs)
                    fact.add_rule(newRule)
                    if r.type == 'Assert':
                        self.AssertRule(newRule)
                    else:
                        self.Retract(newRule.full)


    def AssertRule(self, rule):
        """
        Assert new rule
        """
        self.RB.append(rule)
        self.inferFromRule(rule)


    def inferFromRule(self, rule):
        """
        infer new things from rules
        """
        for f in self.KB:
            bindings = match(rule.lhs[0], f)
            if bindings != False:
                if len(rule.lhs) == 1:
                    if rule.type == 'Assert':
                        newStatement = Statement(instantiate(rule.rhs.full, bindings))
                        f.add_fact(newStatement)
                        self.AssertFact(newStatement)
                    else:
                        newStatement = Statement(instantiate(rule.rhs.full, bindings), 'N')
                        f.add_fact(newStatement)
                        self.Retract(newStatement.full)
                else:
                    tests = map(lambda x: instantiate(x.full, bindings), rule.lhs[1:])
                    rhs = instantiate(rule.rhs.full, bindings)
                    newRule = Rule(tests, rhs)
                    f.add_rule(newRule)
                    if rule.type == 'Assert':
                        self.AssertRule(newRule)
                    else:
                        self.Retract(newRule.full)


    def Retract(self, stat):
        """
        Retract from fact.
        """
        for fact in self.KB:
            # print '~~~~~~%s, %s' % (str(stat), str(fact))
            if pattern_match(stat, fact) != False:
                self.removeFactAndSupport(fact)


    def removeFactAndSupport(self, fact):
        """
        Remove the fact and rules related to the retracted fact
        """
        if fact in self.KB:
            if self.verbose: print 'Removing: ' + fact.pretty()
            for f in fact.facts:
                self.removeSupport(f)
            for r in fact.rules:
                self.removeRule(r)

            self.KB.remove(fact)


    def removeRule(self, rule):
        """
        Remove Rules, and related fact
        """
        self.removeSupport(rule.rhs)

        if rule in self.RB:
            self.RB.remove(rule)


    def removeSupport(self, fact):
        """
        Remove the fact that related to retracted fact,
        """
        if fact.type == 'P':
            self.Retract(fact.full)
        else: #
            fact.type = 'P'
            self.AssertFact(fact)


    def Ask(self, patterns, blist):
        """
        Try to find the blists which can be inferred from knowledgebase
        """
        # for pat in patterns:
        if not patterns:
            return [blist]
        blists = []
        for fact in self.KB:
            bl = match_args(patterns[0], fact.full, blist.copy())
            if bl != False:
                blists += self.Ask(patterns[1:], bl)
        return blists


    # def bc(self, querys, blists):
    #     if blists:
    #         if querys:
    #             return self.bc(querys[0], ask(querys[0], querys[1:], blists))
    #         else:
    #             return blists
    #     else:
    #         return []


    # def reason(self, blists):
    #     # ans
    #     for bl in blists:
    #         for patterns in self.tokenized_rules:
    #             self.ask(patterns, bl)


def testAssertRetract():
    kb = KB("statements1.txt")
    # print kb.ask([['color', '?x', '?y']], {})
    kb.printFacts()
    kb.printRules()

    def askQuestion(question):
        print 'ask: %s' % str(question)
        print '\tans: %s' % str(kb.Ask(question, {}))

    # def assertFact(fact):
    #     print 'assert: %s' % str(fact)
    #     print '\tans: %s' % str(kb.assertFact(fact))

    # def retractFact(fact):
    #     return

    askQuestion([['inst', '?x', 'cube']])
    askQuestion([['inst', '?x', 'cube'], ['on', 'cube2', '?x']])

    kb.Retract(['on', 'cube1', 'cube2'])
    #
    kb.printFacts()
    kb.printRules()

def testAsk():
    kb = KB("statements.txt")
    kb.printFacts()
    kb.printRules()
    # print kb.tokenized_rules[2]
    def askQuestion(question):
        print 'ask: %s' % str(question)
        print '\tans: %s' % str(kb.Ask(question, {}))

    askQuestion([['color', 'pyramid1', '?x']])
    askQuestion([['size', 'pyramid3', '?x']])
    askQuestion([['inst', 'pyramid2', '?x']])
    askQuestion([['inst', '?x', 'pyramid'], ['size', '?x', 'big']])
    askQuestion([['inst', '?x', 'pyramid'], ['size', '?x', 'big'], ['color', '?x', 'red']])
    askQuestion([['color', '?x', 'red'], ['color', '?x', 'green']])
    askQuestion([['on', 'cube2', '?x']])
    askQuestion([['on', 'cube2', 'cube4']])
    askQuestion([['under', 'cube2', '?x']])
    askQuestion([['on', '?x', '?y'], ['bigger', '?x', '?y']])

def unitTest(KBFileName):
    kb = KB(KBFileName)
    def askQuestion(question):
        print 'ask: %s' % str(question)
        print '\tblist: %s' % str(kb.Ask(question, {}))

    askQuestion([['inst', 'pyramid1', '?x']])
    kb.AssertFact(Statement(['inst', 'pyramid1', 'pyramid']))
    askQuestion([['inst', 'pyramid1', '?x']])
    kb.AssertFact(Statement(['inst', 'pyramid2', 'pyramid']))
    kb.AssertFact(Statement(['on', 'pyramid1', 'table']))
    kb.AssertFact(Statement(['on', 'pyramid2', 'table']))
    askQuestion([['inst', '?x', 'pyramid'], ['on', '?x', 'table']])
    kb.Retract(['on', 'pyramid2', 'table'])
    askQuestion([['on', '?x', 'table']])
    # askQuestion([['inst', '?x', 'pyramid'], ['on', '?x', 'table']])


if __name__ == '__main__':
    # kb = KB("statements.txt")
    # testAssertRetract()
    # testAsk()
    # KBFileName = "statements.txt"
    KBFileName = "rules.txt"
    unitTest(KBFileName)
    # kb = KB("statements.txt")
    # print retracter.ask([['color', '?x', '?y']], {})
    # retracter.ask('')
