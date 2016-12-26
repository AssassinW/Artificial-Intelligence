import sys
import string
import copy
global standard_count
standard_count = 0
def Unify_op(x,y,theta): #(string, string, list)
    x_argument = argument(x)
    y_argument = argument(y)
    return Unify(x_argument,y_argument,theta)

def Unify(x,y,theta): #(list, list, list)
    if theta == None:
        return None
    elif x == y:
        return theta
    elif len(x) == 1 and len(y) == 1:
        if Variable(x[0]) == True:
            return Unify_var(x[0],y[0],theta)
        elif Variable(y[0]) == True:
            return Unify_var(y[0],x[0],theta)
        else:
            return None
    elif len(x)>1 and len(y)>1:
        return Unify(x[1:len(x)],y[1:len(y)],Unify(x[0:1],y[0:1],theta))
    else:
        return None
def Unify_var(var,x,theta): #(string, string, list)
    ret = copy.deepcopy(theta)
    val = Exists(var,theta)
    if val != -1:
        return Unify(val,x,theta)
    val = Exists(x,theta)
    if val != -1:
        return Unify(var,val,theta)
    else:
        ret.append([var,x])
    return ret
def argument(x):    #string
    start = x.find('(')
    end = x.find(')')
    t = x[start+1:end]
    ret = t.split(', ')
    return ret
def Exists(x,theta):    #(list,list)
    if theta == None:
        return -1
    val = x
    for element in theta:
        if element[0] == x:
            val = element[1]
            return val
    return -1

def Variable(x):    #list
    for element in x:
        if element >= 'A' and element <= 'Z':
            return False
    return True

def print_format(query):
    find_start = query.find('(')
    find_end = query.find(')')
    ret = query[0:find_start+1]
    var = query[find_start+1:find_end].split(', ')
    for one_var in var:
        if Variable(one_var) == True:
            one_var = '_'
        ret = ret + one_var +', '
    ret = ret[0:len(ret)-2]+')'
    return ret
def SUBST(theta,first):
    if theta == None:
        return first
    if len(theta) == 0:
        return first
    find_start = first.find('(')
    find_end = first.find(')')
    ret = first[0:find_start+1]
    var = first[find_start+1:find_end].split(', ')
    for one_var in var:
        for sub in theta:
            if sub[0] == one_var:
                one_var = sub[1]
        ret = ret + one_var + ', '
    ret = ret[0:len(ret)-2]+')'
    return ret

def FOL_BC_ASK(KB,query,output_list):
    theta = []
    for ret in FOL_BC_OR(KB,query,theta,output_list):
        return ret

def FOL_BC_OR(KB,goal,theta,output_list):

    if theta == None:
        return
    answered = 0
    for rule in Fetch_Rules_For_Goal(KB,goal):
        rule = Standardize_Variables(rule)
        thetaNew = Unify_op(rule[1],goal,theta)
        query_sentence = 'Ask: '+print_format(goal)
        if len(output_list) == 0:
            output_list.append(query_sentence)
        else:
            if output_list[len(output_list)-1] != query_sentence:
                output_list.append(query_sentence)
        '''if len(rule[0]) == 0:
            if asked == 0:
                output_list.append('Ask: '+print_format(goal))
                asked = 1
        else:
            output_list.append('Ask: '+print_format(goal))'''

        for theta_prime in FOL_BC_AND(KB,rule[0],thetaNew,output_list):
            output_list.append('True: '+print_format(SUBST(theta_prime,goal)))
            answered = 1
            yield theta_prime
    if answered == 0:
        output_list.append('False: '+ print_format(SUBST(thetaNew,goal)))
        answered = 1
    #if goal == 'Parent(Peter, Shelly)':
        #print theta

def FOL_BC_AND(KB,goals,theta,output_list):
    thetaNew = theta
    if theta == None:
        return
    elif len(goals) == 0:
        yield theta
    else:
        first = goals[0]
        if len(goals) == 1:
            rest = []
        else:
            rest = goals[1:len(goals)]
        for theta_prime in FOL_BC_OR(KB, SUBST(theta,first),thetaNew,output_list):
            #print thetaNew
            #print theta_prime
            for theta_prime_2 in FOL_BC_AND(KB,rest,theta_prime,output_list):
                yield theta_prime_2


def Fetch_Rules_For_Goal(KB,goal):
    for element in KB:
        rule = []
        start = element.find('=>')
        if start == -1:
            find_comma = element.find('(')
            if goal.find(element[0:find_comma]) != -1:
                rhs = element
                lhs = []
                rule = [lhs,rhs]
        else:
            rhs = element[start+3:len(element)]
            find_and = rhs.find('(')
            if goal.find(rhs[0:find_and]) != -1:
                lhs = []
                find_and = element.find('&&')
                while find_and != -1:
                    lhs.append(element[0:find_and-1])
                    element = element[find_and+3:start+1]
                    find_and = element.find('&&')
                start = element.find('=>')
                lhs.append(element[0:start-1])
                rule=[lhs,rhs]
        if len(rule) != 0:
            yield rule

def variable_check(line):
    start = line.find('(')
    end = line.find(')')
    op_line = line[start+1:end]
    ret = []
    comma_find = op_line.find(',')
    while comma_find != -1:
        var = op_line[0:comma_find]
        ret.append(var)
        op_line = op_line[comma_find+2:len(op_line)]
        comma_find = op_line.find(',')
    ret.append(op_line)
    return ret
def change_to_chr(n):
    ret =''
    while n/10 != 0:
        r = n%10
        n = n/10
        ret = chr(r+48) + ret
    ret = chr(n+48) + ret
    return ret
def Standardize_Variables(rule):
    global standard_count
    standard_count = standard_count + 1
    l = []
    for element in rule[0]:
        l.append(element)
    l.append(rule[1])
    for i in range(0,len(l)):
        var = variable_check(l[i])
        l[i] = l[i][0:l[i].find('(')+1]
        for one_var in var:
            if Variable(one_var):
                one_var = one_var + change_to_chr(standard_count)
            l[i] = l[i] + one_var + ', '
        l[i] = l[i][0:len(l[i])-2] + ')'
    lhs = []
    for i in range(0,len(l)-1):
        lhs.append(l[i])
    rhs = l[len(l)-1]
    return [lhs,rhs]

KB = []
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
query = line[0:len(line)-1]
try:
    line = file_ob.readline()
except:
    print 'Error in reading file!'
    sys.exit()
num_kb = string.atoi(line)
for i in range(0,num_kb):
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    KB.append(line[0:len(line)-1])
try:
    output_ob = open('output.txt','w'); #to be filled
except:
    print 'cannot open file!'
    sys.exit()


sub_goal = []
find_and = query.find('&&')
fail_mark = 0
output_list = []
if find_and != -1:
    while find_and != -1:
        sub_goal.append(query[0:find_and-1])
        query = query[find_and+3:len(query)]
        find_and = query.find('&&')
    sub_goal.append(query)
    for i in range(0,len(sub_goal)):
        if FOL_BC_ASK(KB,sub_goal[i],output_list) == None:
            fail_mark = 1
            output_list.append('False')
            break
    if fail_mark == 0:
        output_list.append('True')
else:
    if FOL_BC_ASK(KB,query,output_list) == None:
        output_list.append('False')
    else:
        output_list.append('True')
    #do query
print_file = ''
for i in range(0,len(output_list)):
    if output_list[i][0:3] == 'Ask':
        match = 0
        find_comma = output_list[i].find('(')
        for j in range(i+1,len(output_list)):
            if output_list[j].find(output_list[i][5:find_comma]) != -1:
                if output_list[j][0:3] != 'Ask':
                    match = 1
                    break
        if match == 0:
            continue
        else:
            print_file = print_file + output_list[i] + '\r\n'
            match = 0
    else:
        print_file = print_file + output_list[i] + '\r\n'
print_file = print_file[0:len(print_file)-2]
output_ob.write(print_file)
output_ob.close()
