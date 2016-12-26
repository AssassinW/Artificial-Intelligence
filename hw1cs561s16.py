import sys
import string
import Queue
import copy
def termi_check(state):
    for i in range(0,5):
        for j in range(0,5):
            if state[i][j] == '*':
                return False
    return True
def show(a):
    if a == float('inf'):
        return 'Infinity'
    elif a == float('-inf'):
        return '-Infinity'
    else:
        return str(a)
def flip_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'
def MiniMax(init_state,grid_v,cutoff,player,print_list,traverse_ob):
    if cutoff == 0:
        print_line = 'root,0,%d\n'%(get_value(init_state,grid_v,player))
        traverse_ob.write(print_line)     #
        return [init_state,get_value(init_state,grid_v,player),print_list+print_line]
    value = float('-inf')
    ret = [[[0 for col in range(6)] for row in range(5)],value,print_list]
    print_line = 'root,0,-Infinity\n'
    traverse_ob.write(print_line)
    ret[2] = ret[2] + print_line
    if termi_check(init_state) == True:
        return [init_state,get_value(init_state,grid_v,player),ret[2]]
    for i in range(0,5):
        for j in range(0,5):
            if init_state[i][j] == '*':
                tmp_state = copy.deepcopy(init_state)
                tmp_state[i][j] = player
                if(i>0 and init_state[i-1][j] == player) or (j>0 and init_state[i][j-1] == player) or (i<4 and init_state[i+1][j] == player) or (j<4 and init_state[i][j+1] == player):
                    if(i>0 and init_state[i-1][j] != player and init_state[i-1][j] != "*"):
                        tmp_state[i-1][j] = player
                    if(j>0 and init_state[i][j-1] != player and init_state[i][j-1] != "*"):
                        tmp_state[i][j-1] = player
                    if(i<4 and init_state[i+1][j] != player and init_state[i+1][j] != "*"):
                        tmp_state[i+1][j] = player
                    if(j<4 and init_state[i][j+1] != player and init_state[i][j+1] != "*"):
                        tmp_state[i][j+1] = player
                t=MinValue(tmp_state,grid_v,cutoff-1,player,i,j,cutoff,ret[2],traverse_ob)
                #print t
                #print ret[1]
                if t[0]>ret[1]:
                    ret = [tmp_state,t[0],t[1]]
                print_line = 'root,0,%d\n'%(ret[1])
                traverse_ob.write(print_line)
                ret[2] = ret[2] + print_line
    return ret
def MinValue(state,grid_v,level,player,row,col,cutoff,print_list,traverse_ob):
    if level == 0:
        print_line = '%c%d,%d,%d\n'%(chr(col+65),row+1,cutoff-level,get_value(state,grid_v,player))
        traverse_ob.write(print_line)
        return [get_value(state,grid_v,player),print_list + print_line]
    ret = [float('inf'),print_list]
    print_line = '%c%d,%d,Infinity\n'%(chr(col+65),row+1,cutoff-level)
    traverse_ob.write(print_line)
    ret[1] = ret[1] + print_line
    oppo = flip_player(player)
    if termi_check(state) == True:
        print 'terminated'
        return [get_value(state,grid_v,player),ret[1]]
    for i in range(0,5):
        for j in range(0,5):
            if state[i][j] == '*':
                tmp_state = copy.deepcopy(state)
                tmp_state[i][j] = oppo
                if(i>0 and state[i-1][j] == oppo) or (j>0 and state[i][j-1] == oppo) or (i<4 and state[i+1][j] == oppo) or (j<4 and state[i][j+1] == oppo):
                    if(i>0 and state[i-1][j] != oppo and state[i-1][j] != "*"):
                        tmp_state[i-1][j] = oppo
                    if(j>0 and state[i][j-1] != oppo and state[i][j-1] != "*"):
                        tmp_state[i][j-1] = oppo
                    if(i<4 and state[i+1][j] != oppo and state[i+1][j] != "*"):
                        tmp_state[i+1][j] = oppo
                    if(j<4 and state[i][j+1] != oppo and state[i][j+1] != "*"):
                        tmp_state[i][j+1] = oppo
                t=MaxValue(tmp_state,grid_v,level-1,player,i,j,cutoff,ret[1],traverse_ob)
                if t[0]<ret[0]:
                    ret = t
                else:
                    ret = [ret[0],t[1]]
                if ret[0] == float('inf'):
                    print_line = '%c%d,%d,Infinity\n'%(chr(col+65),row+1,cutoff-level)
                else:
                    print_line = '%c%d,%d,%d\n'%(chr(col+65),row+1,cutoff-level,ret[0])
                ret[1] = ret[1] + print_line
                traverse_ob.write(print_line)
    return ret
def MaxValue(state,grid_v,level,player,row,col,cutoff,print_list,traverse_ob):
    if level == 0:
        print_line = '%c%d,%d,%d\n'%(chr(col+65),row+1,cutoff-level,get_value(state,grid_v,player))
        traverse_ob.write(print_line)
        return [get_value(state,grid_v,player),print_list + print_line]
    ret = [float('-inf'),print_list]
    print_line = '%c%d,%d,-Infinity\n'%(chr(col+65),row+1,cutoff-level)
    traverse_ob.write(print_line)
    ret[1] = ret[1] + print_line
    if termi_check(state) == True:
        return [get_value(state,grid_v,player),ret[1]]
    for i in range(0,5):
        for j in range(0,5):
            if state[i][j] == '*':
                tmp_state = copy.deepcopy(state)
                tmp_state[i][j] = player
                if(i>0 and state[i-1][j] == player) or (j>0 and state[i][j-1] == player) or (i<4 and state[i+1][j] == player) or (j<4 and state[i][j+1] == player):
                    if(i>0 and state[i-1][j] != player and state[i-1][j] != "*"):
                        tmp_state[i-1][j] = player
                    if(j>0 and state[i][j-1] != player and state[i][j-1] != "*"):
                        tmp_state[i][j-1] = player
                    if(i<4 and state[i+1][j] != player and state[i+1][j] != "*"):
                        tmp_state[i+1][j] = player
                    if(j<4 and state[i][j+1] != player and state[i][j+1] != "*"):
                        tmp_state[i][j+1] = player
                t=MinValue(tmp_state,grid_v,level-1,player,i,j,cutoff,ret[1],traverse_ob)
                if t[0]>ret[0]:
                    ret = t
                else:
                    ret = [ret[0],t[1]]
                if ret[0] == float('-inf'):
                    print_line = '%c%d,%d,Infinity\n'%(chr(col+65),row+1,cutoff-level)
                else:
                    print_line = '%c%d,%d,%d\n'%(chr(col+65),row+1,cutoff-level,ret[0])
                ret[1] = ret[1] + print_line
                traverse_ob.write(print_line)
    return ret

def Alpha_Beta(init_state,grid_v,cutoff,player,print_list,traverse_ob):
    if cutoff == 0:
        print_line = 'root,0,%d,-Infinity,infinity\n'%(get_value(init_state,grid_v,player))
        traverse_ob.write(print_line)
        return [init_state,get_value(init_state,grid_v,player),print_list+print_line]
    value = float('-inf')
    Alpha = float('-inf')
    Beta = float('inf')
    ret = [[[0 for col in range(6)] for row in range(5)],value,print_list]
    print_line = 'root,0,-Infinity,-Infinity,Infinity\n'
    traverse_ob.write(print_line)
    ret[2] = ret[2] + print_line
    if termi_check(init_state) == True:
        return [init_state,get_value(init_state,grid_v,player),ret[2]]
    for i in range(0,5):
        for j in range(0,5):
            if init_state[i][j] == '*':
                tmp_state = copy.deepcopy(init_state)
                tmp_state[i][j] = player
                if(i>0 and init_state[i-1][j] == player) or (j>0 and init_state[i][j-1] == player) or (i<4 and init_state[i+1][j] == player) or (j<4 and init_state[i][j+1] == player):
                    if(i>0 and init_state[i-1][j] != player and init_state[i-1][j] != "*"):
                        tmp_state[i-1][j] = player
                    if(j>0 and init_state[i][j-1] != player and init_state[i][j-1] != "*"):
                        tmp_state[i][j-1] = player
                    if(i<4 and init_state[i+1][j] != player and init_state[i+1][j] != "*"):
                        tmp_state[i+1][j] = player
                    if(j<4 and init_state[i][j+1] != player and init_state[i][j+1] != "*"):
                        tmp_state[i][j+1] = player
                t=ABMin(tmp_state,grid_v,cutoff-1,player,i,j,cutoff,ret[2],Alpha,Beta,traverse_ob)
                if t[0]>Alpha:
                    if t[0]<Beta:
                        Alpha = t[0]
                #print t
                #print ret[1]
                if t[0]>Beta:
                    return ret
                if t[0]>ret[1]:
                    ret = [tmp_state,t[0],t[1]]
                    Alpha = t[0]
                print_line = 'root,0,%d,%s,%s\n'%(ret[1],show(Alpha),show(Beta))
                traverse_ob.write(print_line)
                ret[2] = ret[2] + print_line
    return ret
def ABMin(state,grid_v,level,player,row,col,cutoff,print_list,Alpha,Beta,traverse_ob):
    if level == 0:
        print_line = '%c%d,%d,%d,%s,%s\n'%(chr(col+65),row+1,cutoff-level,get_value(state,grid_v,player,show(Alpha),show(Beta)))
        traverse_ob.write(print_line)
        return [get_value(state,grid_v,player),print_list + print_line]
    ret = [float('inf'),print_list]
    print_line = '%c%d,%d,Infinity,%s,%s\n'%(chr(col+65),row+1,cutoff-level,show(Alpha),show(Beta))
    traverse_ob.write(print_line)
    ret[1] = ret[1] + print_line
    oppo = flip_player(player)
    if termi_check(state) == True:
        return [get_value(state,grid_v,player),ret[1]]
    for i in range(0,5):
        for j in range(0,5):
            if state[i][j] == '*':
                tmp_state = copy.deepcopy(state)
                tmp_state[i][j] = oppo
                if(i>0 and state[i-1][j] == oppo) or (j>0 and state[i][j-1] == oppo) or (i<4 and state[i+1][j] == oppo) or (j<4 and state[i][j+1] == oppo):
                    if(i>0 and state[i-1][j] != oppo and state[i-1][j] != "*"):
                        tmp_state[i-1][j] = oppo
                    if(j>0 and state[i][j-1] != oppo and state[i][j-1] != "*"):
                        tmp_state[i][j-1] = oppo
                    if(i<4 and state[i+1][j] != oppo and state[i+1][j] != "*"):
                        tmp_state[i+1][j] = oppo
                    if(j<4 and state[i][j+1] != oppo and state[i][j+1] != "*"):
                        tmp_state[i][j+1] = oppo
                t=ABMax(tmp_state,grid_v,level-1,player,i,j,cutoff,ret[1],Alpha,Beta,traverse_ob)
                if t[0]<ret[0]:
                    ret = t
                else:
                    ret = [ret[0],t[1]]
                if t[0]<Beta:
                    if t[0]>Alpha:
                        Beta = t[0]
                if t[0]<=Alpha:
                    if ret[0] == float('inf'):
                        print_line = '%c%d,%d,Infinity,%s,%s\n'%(chr(col+65),row+1,cutoff-level,show(Alpha),show(Beta))
                    else:
                        print_line = '%c%d,%d,%d,%s,%s\n'%(chr(col+65),row+1,cutoff-level,ret[0],show(Alpha),show(Beta))
                    traverse_ob.write(print_line)
                    return ret
                if ret[0] == float('inf'):
                    print_line = '%c%d,%d,Infinity,%s,%s\n'%(chr(col+65),row+1,cutoff-level,show(Alpha),show(Beta))
                else:
                    print_line = '%c%d,%d,%d,%s,%s\n'%(chr(col+65),row+1,cutoff-level,ret[0],show(Alpha),show(Beta))
                traverse_ob.write(print_line)
                ret[1] = ret[1] + print_line

    return ret
def ABMax(state,grid_v,level,player,row,col,cutoff,print_list,Alpha,Beta,traverse_ob):
    if level == 0:
        print_line = '%c%d,%d,%d,%s,%s\n'%(chr(col+65),row+1,cutoff-level,get_value(state,grid_v,player),show(Alpha),show(Beta))
        traverse_ob.write(print_line)
        return [get_value(state,grid_v,player),print_list + print_line]
    ret = [float('-inf'),print_list]
    print_line = '%c%d,%d,-Infinity,%s,%s\n'%(chr(col+65),row+1,cutoff-level,show(Alpha),show(Beta))
    traverse_ob.write(print_line)
    ret[1] = ret[1] + print_line
    if termi_check(state) == True:
        return [get_value(state,grid_v,player),ret[1]]
    for i in range(0,5):
        for j in range(0,5):
            if state[i][j] == '*':
                tmp_state = copy.deepcopy(state)
                tmp_state[i][j] = player
                if(i>0 and state[i-1][j] == player) or (j>0 and state[i][j-1] == player) or (i<4 and state[i+1][j] == player) or (j<4 and state[i][j+1] == player):
                    if(i>0 and state[i-1][j] != player and state[i-1][j] != "*"):
                        tmp_state[i-1][j] = player
                    if(j>0 and state[i][j-1] != player and state[i][j-1] != "*"):
                        tmp_state[i][j-1] = player
                    if(i<4 and state[i+1][j] != player and state[i+1][j] != "*"):
                        tmp_state[i+1][j] = player
                    if(j<4 and state[i][j+1] != player and state[i][j+1] != "*"):
                        tmp_state[i][j+1] = player
                t=ABMin(tmp_state,grid_v,level-1,player,i,j,cutoff,ret[1],Alpha,Beta,traverse_ob)
                if t[0]>ret[0]:
                    ret = t
                else:
                    ret = [ret[0],t[1]]
                if t[0]>Alpha:
                    if t[0]<Beta:
                        Alpha = t[0]
                if t[0]>=Beta:
                    if ret[0] == float('inf'):
                        print_line = '%c%d,%d,Infinity,%s,%s\n'%(chr(col+65),row+1,cutoff-level,show(Alpha),show(Beta))
                    else:
                        print_line = '%c%d,%d,%d,%s,%s\n'%(chr(col+65),row+1,cutoff-level,ret[0],show(Alpha),show(Beta))
                    traverse_ob.write(print_line)
                    return ret
                if ret[0] == float('-inf'):
                    print_line = '%c%d,%d,Infinity\n'%(chr(col+65),row+1,cutoff-level)
                else:
                    print_line = '%c%d,%d,%d\n'%(chr(col+65),row+1,cutoff-level,ret[0])
                traverse_ob.write(print_line)
                ret[1] = ret[1] + print_line

    return ret

def get_value(init_state,grid_v,player):
    init_value = 0
    for i in range(0,5):
        for j in range(0,5):
            if(init_state[i][j] == player):
                init_value = init_value + grid_v[i][j]
            elif(init_state[i][j] == "*"):
                init_value = init_value
            else:
                init_value = init_value - grid_v[i][j]
    return init_value
def best_first(init_state,player,grid_v):
    ret = init_state
    init_value = get_value(init_state,grid_v,player)
    max_v = init_value
    index_change = Queue.Queue()
    for i in range(0,5):
        for j in range(0,5):
            if(init_state[i][j] == "*"):
                t = init_value + grid_v[i][j]
                if(i>0 and init_state[i-1][j] == player) or (j>0 and init_state[i][j-1] == player) or (i<4 and init_state[i+1][j] == player) or (j<4 and init_state[i][j+1] == player):
                    if(i>0 and init_state[i-1][j] != player and init_state[i-1][j] != "*"):
                        t = t + 2*grid_v[i-1][j]
                    if(j>0 and init_state[i][j-1] != player and init_state[i][j-1] != "*"):
                        t = t + 2*grid_v[i][j-1]
                    if(i<4 and init_state[i+1][j] != player and init_state[i+1][j] != "*"):
                        t = t + 2*grid_v[i+1][j]
                    if(j<4 and init_state[i][j+1] != player and init_state[i][j+1] != "*"):
                        t = t + 2*grid_v[i][j+1]
                if t > max_v:
                    max_v = t
                    while index_change.empty()!=True:
                        index_change.get()
                    index_change.put([i,j])
                    if(i>0 and init_state[i-1][j] == player) or (j>0 and init_state[i][j-1] == player) or (i<4 and init_state[i+1][j] == player) or (j<4 and init_state[i][j+1] == player):
                        if(i>0 and init_state[i-1][j] != player and init_state[i-1][j] != "*"):
                            index_change.put([i-1,j])
                        if(j>0 and init_state[i][j-1] != player and init_state[i][j-1] != "*"):
                            index_change.put([i,j-1])
                        if(i<4 and init_state[i+1][j] != player and init_state[i+1][j] != "*"):
                            index_change.put([i+1,j])
                        if(j<4 and init_state[i][j+1] != player and init_state[i][j+1] != "*"):
                            index_change.put([i,j+1])

    if index_change.empty()!=True:
        while index_change.empty()!=True:
            get_index = index_change.get()
            ret[get_index[0]][get_index[1]] = player
    return ret


grid_v = [[0 for col in range(5)] for row in range(5)]      #grid value
init_state = [[0 for col in range(6)] for row in range(5)]      #grid initial occupation
Total_Value_Player = 0      #my points
Total_Value_Opponent = 0    #opponent's points


try:
    file_ob = open(sys.argv[2],'r'); #to be filled
except:
    print 'cannot open file!'
    sys.exit()
try:
    line = file_ob.readline()
except:
    print 'Error in reading file!'
    sys.exit()
task = string.atoi(line)

if task == 1 or task == 2 or task == 3:
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if cmp(line,'X') == True:
        my_player = 'X'       #player side, X or O
    elif cmp(line,'O') == True:
        my_player = 'O'
    else:
        print 'Input error!'
        sys.exit()
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    cutoff = int(line)
    for i in range(0,5):
        try:
            line = file_ob.readline()
        except:
            print 'Error in reading file!'
            sys.exit()
        l = line.split()
        for j in range(0,5):
            t = string.atoi(l[j])
            grid_v[i][j] = t

    for i in range(0,5):
        try:
            line = file_ob.readline()
        except:
            print 'Error in reading file!'
            sys.exit()
        for j in range(0,5):
            init_state[i][j] = line[j]
        init_state[i][5] = '\n'

elif task == 4:
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if cmp(line,'X') == True:
        player_1 = 'X'       #player side, X or O
    elif cmp(line,'O') == True:
        player_1 = 'O'
    else:
        print 'Input error!'
        sys.exit()
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if  int(line) == 1:
        player_1_task = 1
    elif int(line) == 2:
        player_1_task = 2
    elif int(line) == 3:
        player_1_task = 3
    else:
        print 'Input Error!'
        sys.exit()
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    player_1_cutoff = int(line)
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if cmp(line,'X') == True:
        player_2 = 'X'       #player side, X or O
    elif cmp(line,'O') == True:
        player_2 = 'O'
    else:
        print 'Input error!'
        sys.exit()
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if  int(line) == 1:
        player_2_task = 1
    elif int(line) == 2:
        player_2_task = 2
    elif int(line) == 3:
        player_2_task = 3
    else:
        print 'Input error!'
        sys.exit()
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    player_2_cutoff = int(line)
    for i in range(0,5):
        try:
            line = file_ob.readline()
        except:
            print 'Error in reading file!'
            sys.exit()
        l = line.split()
        for j in range(0,5):
            t = string.atoi(l[j])
            grid_v[i][j] = t

    for i in range(0,5):
        try:
            line = file_ob.readline()
        except:
            print 'Error in reading file!'
            sys.exit()
        for j in range(0,5):
            init_state[i][j] = line[j]
        init_state[i][5] = '\n'

else:
    print 'Input Error!'
    sys.exit()
file_ob.close()

if task == 1:
    ret = best_first(init_state,my_player,grid_v)
    try:
        file_ob = open('next_state.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    for i in range(0,5):
        for j in range(0,6):
            try:
                file_ob.write(ret[i][j])
            except:
                print 'Failed to write'
                sys.exit()
    file_ob.close()

elif task == 2:
    try:
        traverse_ob = open('traverse_log.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    traverse_ob.write('Node,Depth,Value\n')
    print_list = ''
    ret = MiniMax(init_state,grid_v,cutoff,my_player,print_list,traverse_ob)
    #traverse_ob.write(ret[2])
    #print print_list
    traverse_ob.close()
    try:
        file_ob = open('next_state.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    for i in range(0,5):
        for j in range(0,6):
            try:
                file_ob.write(ret[0][i][j])
            except:
                print 'Failed to write'
                sys.exit()
    file_ob.close()
elif task == 3:
    try:
        traverse_ob = open('traverse_log.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    traverse_ob.write('Node,Depth,Value,Alpha,Beta\n')
    print_list = ''
    ret = Alpha_Beta(init_state,grid_v,cutoff,my_player,print_list,traverse_ob)
    #traverse_ob.write(ret[2])
    #print print_list
    traverse_ob.close()
    try:
        file_ob = open('next_state.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    for i in range(0,5):
        for j in range(0,6):
            try:
                file_ob.write(ret[0][i][j])
            except:
                print 'Failed to write'
                sys.exit()
    file_ob.close()
else:
    try:
        traverse_ob = open('traverse_log.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    state = init_state
    try:
        trace_ob = open('trace_state.txt','w'); #to be filled
    except:
        print 'cannot open file!'
        sys.exit()
    while True:
        if termi_check(state) == True:
            break
        if player_1_task == 1:
            state = best_first(state,player_1,grid_v)
        elif player_1_task == 2:
            ret = MiniMax(state,grid_v,player_1_cutoff,player_1,'',traverse_ob)
            state = ret[0]
        elif player_1_task == 3:
            ret = Alpha_Beta(state,grid_v,player_1_cutoff,player_1,'',traverse_ob)
            state = ret[0]
        for i in range(0,5):
            for j in range(0,6):
                try:
                    trace_ob.write(state[i][j])
                except:
                    print 'Failed to write'
                    sys.exit()
        if termi_check(state) == True:
            break
        if player_2_task == 1:
            state = best_first(state,player_2,grid_v)
        elif player_2_task == 2:
            ret = MiniMax(state,grid_v,player_2_cutoff,player_2,'',traverse_ob)
            state = ret[0]
        elif player_2_task == 3:
            ret = Alpha_Beta(state,grid_v,player_2_cutoff,player_2,'',traverse_ob)
            state = ret[0]
        for i in range(0,5):
            for j in range(0,6):
                try:
                    trace_ob.write(state[i][j])
                except:
                    print 'Failed to write'
                    sys.exit()
    trace_ob.close()
    traverse_ob.close()
