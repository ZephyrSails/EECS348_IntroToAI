def hanoiK(peg, disk):
    pegs = [Peg(i) for i in range(0, peg, [])]
    pegs[0].hold = [i for i in range(disk, 0, -1)]


    return None

def hanoi3(disk, peg=3):
    return None

class Peg:
    def __init__(self, num, hold):
        self.num = num
        self.hold = hold

# def move(n, source, target, helpers):
#     if n == 0:
#         return
#     if n < len(helpers):
#         for helper in helpers:
#             move_disk(source, helper)
#         for helper in reversed(helper):
#             move_disk(helper, target)
#     else:
#         move()

def move(n, source, target, helpers):
    
    for helper in helpers:
        move()



def get_helpers(n, source, target, pegs):


def move_disk(peg1, peg2):
    if (not peg2.hold) and peg1.hold[-1] > peg2.hold(-1):
        print '### ERROR: WRONG MOVE ###'
    else:
        peg1.hold[-1] < peg2.hold(-1):
        disk = peg1.hold.pop()
        peg2.hold.append(disk)
        print 'move ['+disk+'] from '+peg1.num+' to '+peg2.num

def

A = [5,4,3,2,1]
B = []
C = []

def move(n, source, target, auxiliary):
    if n > 0:
        # move n-1 disks from source to auxiliary, so they are out of the way
        move(n-1, source, auxiliary, target)
        # move the nth disk from source to target
        target.append(source.pop())
        # Display our progress
        print(A, B, C, '##############', sep='\n')
        # move the n-1 disks that we left on auxiliary onto target
        move(n-1, auxiliary, target, source)

# initiate call from source A to target C with auxiliary B
move(5, A, C, B)
