input: language
----

output: language
----

0. preset data
    1. rule
1. integrate language -> kb
    1. assert
    2. ask [multiple statement]
        1. ((on ?x ?y) (color ?x red))
    3. inference
    4. rule
    5. retract
2. planner
    1. action
        1. precondition
        2. action
            1. precondition
            2. add
            3. retract
        3. goal
3. hook the planner to language
    1. read the language -> to expressions
4. generating language from statement
    1. read the expression -> transfer to language
