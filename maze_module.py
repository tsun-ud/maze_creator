def new_size():
    choice_x = input("\n input maze size - vertical ")
    choice_y = input("\n input maze size - horizontal ")
    return (int(choice_x), int(choice_y))

def save_maze(arr):
    saver = open("mazes_test.txt", "a")
    saver.write(str(arr))
    saver.write("\n\n\n")
    saver.close()

def print_maze(arr, ind):

    for item in range(len(arr[0])): print("+-", end = "")
    print ("+")
    for item in arr:
        print("|", end = "")
        for pole in item:
            if pole[0] == 1:
                if ind == 1 or pole[2] in ("S", "E"): print(pole[2]+" ", end = "")
                elif ind == 2 and pole[2] in ("S", "E", "x"): print(pole[2]+" ", end = "")
                else: print(" "+" ", end = "")
            else: 
                if ind ==1 or pole[2] in ("S", "E"): print(pole[2]+"|", end = "")
                elif ind ==2 and pole[2] in ("S", "E", "x"): print(pole[2]+"|", end = "")
                else: print(" "+"|", end = "")
        print (" ")
        print ("+", end = "")
        for pole in item:
            if pole[1] == 1: print(" +", end = "")
            else: print("-+", end = "")   
        print (" ")
    print("\n")

def make_path (arr, n, start, end): # n = dlugosc sciezki
    
    def get_dist(curr, end, bigused): #new - lets make end an array - for one element no changes, for more doing all in one BFS

        def travel(pos, n):        
            if pos in local_used: return 0
            if pos in bigused: return 0
            if pos in to_find.keys():
                found[0] +=1
                end[to_find[pos]][2] = n
                if found[0] == len(end): return 0
            

            if pos[0] < 0 or pos[0] >= len(arr) or pos[1] < 0 or pos[1] >= len(arr[0]): return 0
            local_used.add(pos)
            targets = [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]
            for item in targets:
                if item not in local_used and item not in bigused: que.append((item[0],item[1],n+1))
            return 0

        #if curr in end: return 0
        found = [0]
        to_find = {(x[0],x[1]):i for (i,x) in enumerate(end)}
        for item in to_find.keys():
            if item == curr: end[to_find[item]][2] = 0
        local_used = set([curr])
        que = [(curr[0],curr[1]+1,1), (curr[0],curr[1]-1,1), (curr[0]+1,curr[1],1), (curr[0]-1,curr[1],1)]
        while que:
            travel((que[0][0],que[0][1]),que[0][2])
            if found[0] == len(end): return end
            que.pop(0)
        return end

        ''' # old working (but slow) get_dist stored here
        def get_dist(curr, end, bigused):

        def travel(pos, n):
            if pos in local_used: return 0
            if pos in bigused: return 0
            if pos == end: return n
            if pos[0] < 0 or pos[0] >= len(arr) or pos[1] < 0 or pos[1] >= len(arr[0]): return 0
            local_used.add(pos)
            targets = [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]
            for item in targets:
                if item not in local_used and item not in bigused: que.append((item[0],item[1],n+1))
            return 0

        if curr == end: return 0
        local_used = set([curr])
        que = [(curr[0],curr[1]+1,1), (curr[0],curr[1]-1,1), (curr[0]+1,curr[1],1), (curr[0]-1,curr[1],1)]
        while que:
            x = travel((que[0][0],que[0][1]),que[0][2])
            if x != 0: return x
            que.pop(0)
        return -1
        '''
            
    
    #import copy
    #fake = copy.deepcopy(arr)
    dist = abs(start[0]-end[0])+abs(start[1]-end[1])
    if n < dist:
        print("points too far apart for current n!")
        n = dist
    '''
    if n > sizex[0]*sizex[1]:
        print("n too large for curent maze!")
        return arr
    '''

    used = set([start])
    #print("get_dist test 1: ", get_dist((0,0), [(11,11)], used))
    #print("get_dist test 2: ", get_dist((0,0), [](21,11)], used))
    #print("get_dist test 3: ", get_dist((0,0), [(11,21)], used))
    #print("get_dist test 4: ", get_dist(start, [end], set()))

    path = [start]
    pathZ = []
    curr = start
    currlen = 0
    while path[-1] != end:
        #currdist = get_dist(curr,end,used)
        targets = [[curr[0],curr[1]+1,-1, "R"], [curr[0],curr[1]-1,-1, "L"], [curr[0]+1,curr[1],-1, "D"], [curr[0]-1,curr[1],-1, "U"]]
        #for item in targets:
        #    if tuple([item[0],item[1]]) not in used and 0 <= item[0] <= len(arr) and 0 <= item[1] <= len(arr[0]): item[2] = get_dist((item[0],item[1]),end, used)      
        ii = 0
        while ii < len(targets):
            if tuple([targets[ii][0],targets[ii][1]]) in used or 0 > targets[ii][0] or targets[ii][0] >= len(arr) or 0 > targets[ii][1] or targets[ii][1] >= len(arr[0]): targets.pop(ii)
            else: ii +=1
        targets = get_dist(end,targets,used)
        #teraz mamy 4 targety i dla kazdego policzony distance do konca jesli go wybierzemy, jesli target invalid dist = -1
        #time to make a decision, random with % chance shifting depending on distance #sweet
        targets.sort(key=lambda x: x[2], reverse = True)
        #print("targets: ", targets)     
        while targets[-1][2] == -1:
            targets.pop(-1)
            if not targets:
                print("error while making the path, no viable targets")
                return
        
        #if (currlen + currdist)/n >= 1: selection = targets[-1]
        #if (currlen + currdist)/n >= 1:
        #    while targets[0][2] > targets[-1][2]: targets.pop(0)
        #    dice = randint(0,len(targets)-1)
        #    selection = targets[dice]
        #else:

        dice = randint(1,100)/100 #idea - zrobic 3 predzialy 1) oddalam sie 2) random 3) zblizam sie
        if dice < (n-currlen)/(30*n):
            #if len(targets) > 2 and targets[-2][2] == targets[-1][2]: targets = targets[:-2]
            if len(targets) > 1: targets.pop(-1)
        elif dice < currlen/(1.5*n):
            #while targets[0][2] > targets[-1][2]: targets.pop(0)
            if len(targets) > 1: targets.pop(0)

        if len(path)>4 and pathZ[-1] == pathZ[-2] == pathZ[-3] and len(targets)>1:
            ii = 0
            while ii < len(targets):
                if targets[ii][3] == pathZ[-1]:
                    targets.pop(ii)
                else: ii+=1

        dice = randint(0,len(targets)-1)
        selection = targets[dice]
        '''
        if dice < currlen/n*0.8 or (currlen + currdist)/n >= 1.2:
            while targets[0][2] > targets[-1][2]: targets.pop(0)
            dice = randint(0,len(targets)-1)
            #if targets[dice] == end and currlen < n: dice -=1
            selection = targets[dice]
        else:
            dice = randint(0,len(targets)-1)
            if targets[dice] == end: dice -=1
            selection = targets[dice]
        '''
           
        '''
            dice = randint(0,100)/100 # targets: avoid long straight lines and going away >> random >> in
            if dice > (currlen + currdist)/n/2: selection = targets[0] #tutaj mozna jakos parametryzowac, ewentualnie zmienic zeby nie wybieral tylko pierwszy lub ostatni
            else: selection = targets[-1]
        '''
        curr = (selection[0],selection[1])
        path.append(curr)
        if path[-2][0] == path[-1][0]:
            pathZ.append("R") if path[-2][1] < path[-1][1] else pathZ.append("L")
        else:
            pathZ.append("D") if path[-2][0] < path[-1][0] else pathZ.append("U")

        '''
        if path[-2][0] == path[-1][0]:
            if path[-2][1] < path[-1][1]: pathZ.append("U")
            else: pathZ.append("D")
        else:
            if path[-2][0] < path[-1][0]: pathZ.append("L")
            else: pathZ.append("R")
        '''

        currlen +=1
        used.add(curr)
        #print(path)


    #print(path)
    #print(pathZ)
    print("length of the correct path: ",len(path))
    return path

def branching(arr, path, factor): #factor = how often on average is new branching sprouted

    def develop(pos, n):
        #used.add(pos)
        targets = [(pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1)]
        i = 0
        while i<len(targets):
            if targets[i] in used or targets[i][0] < 0 or targets[i][0] >= len(arr) or  0 > targets[i][1] or targets[i][1] >= len(arr[0]): targets.pop(i)
            else: i+=1
        if len(targets) == 0: return
        if len (targets) > 1:
            dice = randint(1,100)
            if dice < 100/factor: que.append((pos, n+1))

        x = targets[randint(0,len(targets)-1)]
        que.append((x, n))
        used.add(x)

        arr[x[0]][x[1]][2] = str(n%10)
        if pos[0] == x[0]:
            if pos[1] < x[1]: arr[pos[0]][pos[1]][0] = 1
            else: arr[x[0]][x[1]][0] = 1
        elif pos[1] == x[1]:
            if pos[0] < x[0]: arr[pos[0]][pos[1]][1] = 1
            else: arr[x[0]][x[1]][1] = 1

    def find_sprout(pos):
        targets = [(pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1)]
        i = 0
        while i<len(targets):
            if targets[i][0] < 0 or targets[i][0] >= len(arr) or  0 > targets[i][1] or targets[i][1] >= len(arr[0]): targets.pop(i)
            elif arr[targets[i][0]][targets[i][1]][2] in (" ", "E", "S"): targets.pop(i)
            else: i+=1
        if len(targets) == 0: return 
        else: return targets[0]

    que = []
    used = set(path)
    x = int((len(path)-2)/factor)
    for i in range(x-1):
        dice = randint(factor*i, factor*i+factor)
        que.append((path[dice], i))
        used.add(path[dice])
    while que:
        develop(que[0][0], que[0][1])
        que.pop(0)
    #print("before todo:")
    #print_maze (maze, 1)
    #print_maze (maze, 0)

    todo = []
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if arr[row][col][2] == " ": todo.append((row,col))

    i = 0
    while todo:
        x = find_sprout(todo[0])
        if x:
            que.append((x,i))
            i+=1
        else: todo = todo[1:]+[todo[0]] #cos tutaj nie dziala.... panie tutaj jest while 1 gdzies... :/
        while que:
            develop(que[0][0], que[0][1])
            #if (que[0][0],que[0][1]) in todo: todo.remove((que[0][0],que[0][1]))
            que.pop(0)
        while arr[todo[0][0]][todo[0][1]][2] != " ":
            todo.pop(0)
            if not todo: break
    print("developing finished")
    #print("empty squares: ", len(todo))
    #print("after todo:")
    print_maze (arr, 1)
    print_maze (arr, 2)
    print_maze (arr, 0)

def get_maze(sizex):
    path = 30 #in % how much of the maze will the correct path take
    maze = [[[0,0," "] for x in range(int(sizex[1]))] for x in range(int(sizex[0]))]
    start = (randint(0,sizex[0]-1), randint(0,int(sizex[1]/4-1)))
    end = (randint(0,sizex[0]-1), randint(int(sizex[1]*3/4),sizex[1]-1))
    maze[start[0]][start[1]][2] = "S"
    maze[end[0]][end[1]][2] = "E"
    #print_maze (maze, 1)
    #print(start,end)
    st = time.time()
    path = make_path(maze, int(sizex[0]*sizex[1]/5),start,end)

    for i,item in enumerate(path[:-1]):
        x = maze[path[i][0]][path[i][1]]
        x2 = maze[path[i+1][0]][path[i+1][1]]
        if x[2] != "S" and x[2] != "E": x[2] = "x"
        if path[i][1] == path[i+1][1]:
             if path[i][0] < path[i+1][0]: x[1] = 1
             else: x2[1] = 1
        elif path[i][0] == path[i+1][0]:
             if path[i][1] < path[i+1][1]: x[0] = 1
             else: x2[0] = 1

    branching(maze,path,int(log(sizex[0]*sizex[1],4)))
    et = time.time()
    eltime2 = et-st
    print('\n Execution time:', eltime2, 'seconds\n')
    return maze

def render_maze(maze):
    pass

    

    


def print_menu():
    print(" Select action:\n 1. Get maze\n 2. Change size\n 3. Save maze as txt\n 4. Save maze as .jpg\n 0. Exit")
    choice = input("    ")
    return choice


from math import log
from random import randint
import time
'''
print("default size: 10x10")
sizex = (10,10)
maze = []
while (1):
    select = print_menu()
    if select == "0": break
    if select == "1": maze = get_maze(sizex)
    if select == "2": sizex = new_size()
    if select == "3": save_maze(maze)
    if select == "4": render_maze(maze)
'''

'''
from math import log
from random import randint
import time
sizex = new_size()
#sizex = (13,40)
path = 30 #in % how much of the maze will the correct path take
maze = [[[0,0," "] for x in range(int(sizex[1]))] for x in range(int(sizex[0]))]

#start = (randint(0,int(sizex[0]/4)-1), randint(0,int(sizex[1]/4)-1))
start = (randint(0,sizex[0]-1), randint(0,int(sizex[1]/4-1)))
#end = (randint(int(sizex[0]/4*3),sizex[0]-1), randint(int(sizex[1]/4*3),sizex[1]-1))Z
end = (randint(0,sizex[0]-1), randint(int(sizex[1]*3/4),sizex[1]-1))
maze[start[0]][start[1]][2] = "S"
maze[end[0]][end[1]][2] = "E"
print_maze (maze, 1)
print(start,end)
st = time.time()
path = make_path(maze, int(sizex[0]*sizex[1]/5),start,end)
#path = make_path(maze, 100,start,end)

for i,item in enumerate(path[:-1]):
    x = maze[path[i][0]][path[i][1]]
    x2 = maze[path[i+1][0]][path[i+1][1]]
    if x[2] != "S" and x[2] != "E": x[2] = "x"
    if path[i][1] == path[i+1][1]:
         if path[i][0] < path[i+1][0]: x[1] = 1
         else: x2[1] = 1
    elif path[i][0] == path[i+1][0]:
         if path[i][1] < path[i+1][1]: x[0] = 1
         else: x2[0] = 1

print_maze (maze, 1)

branching(maze,path,int(log(sizex[0]*sizex[1],4)))
#print_maze (maze, 1)
#print_maze (maze, 0)
et = time.time()
eltime2 = et-st
print('\n Execution time:', eltime2, 'seconds')

'''







