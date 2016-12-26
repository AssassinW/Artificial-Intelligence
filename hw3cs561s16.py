#processing the input file
import sys
import copy
import string
class type_bn:
    var = []
    tables = {}         #dict: keys = variable name; value: table(a list)
    def __init__(self,v,t):
        self.var = copy.copy(v)
        self.tables = copy.copy(t)

def round1(x):
    y = round(x,2)
    z = (x-y)*1000
    z = int(z)
    if z<5:
        return y
    else:
        return y+0.01

def round2(x):
    if x > 0:
        y = int(x)
        z = x-y
        if z < 0.5:
            return y
        else:
            return y+1
    elif x == 0:
        return 0
    else:
        y = int(x)
        z = y-x
        if z<0.5:
            return y
        else:
            return y-1

def generate_key(n,l):
    ret = ''
    e = ''
    for i in range(0,l):
        e = e + '-'
    while n!=0:
        r = n%2
        n = n/2
        if r == 0:
            ret = '-' + ret
        else:
            ret = '+' + ret
    ret = e[0:l-len(ret)]+ret
    return ret

def normalize(Q):
    sum = 0.0
    for k in Q.keys():
        sum = sum + Q[k]
    for k in Q.keys():
        Q[k] = Q[k]/sum

def get_prob(table,sign,e):
    tab = table[0].find('|')
    if tab > -1:
        parent = table[0][tab+2:len(table[0])]
        parent_l = []
        b_tab = parent.find(' ')
        while b_tab != -1:
            parent_l.append(parent[0:b_tab])
            parent = parent[b_tab + 1:len(parent)]
            b_tab = parent.find(' ')
        parent_l.append(parent[0:len(parent)-1])
        match = ''
        for element in parent_l:
            match = match + e[element]
            match = match + ' '
        match = match[0:len(match)-1]
        for i in range(1,len(table)):
            sep = table[i].split(' ',1)
            if sep[1][len(sep[1])-1] == '\n':
                sep[1] = sep[1][0:len(sep[1])-1]
            if match == sep[1][0:len(sep[1])]:
                if sign == '+':
                    return string.atof(sep[0])
                else:
                    return 1.0 - string.atof(sep[0])
    else:
        if table[1][0:8] == 'decision':
            return 1.0
        if sign == '+':
            return string.atof(table[1])
        else:
            return 1.0 - string.atof(table[1])
def get_decision_nodes(sentence):
    ret = []
    f_tab = sentence.find('(')
    t_tab = sentence.find(')')
    t = sentence[f_tab+1:t_tab]
    tab = t.find('|')
    if tab != -1:
        t = t[0:tab-1]
    if sentence[0] == 'E':
        c_tab = t.find(',')
        while c_tab != -1:
            e_tab = t.find('=')
            ret.append(t[0:e_tab-1])
            t = t[c_tab + 2:len(t)]
            c_tab = t.find(',')
        e_tab = t.find('=')
        ret.append(t[0:e_tab-1])
    else:
        c_tab = t.find(',')
        while c_tab != -1:
            ret.append(t[0:c_tab])
            t = t[c_tab + 2:len(t)]
            c_tab = t.find(',')
        ret.append(t)
    return ret
def get_dependency_var(sentence):
    tab = sentence.find('|')
    ret = {}
    if tab == -1:
        return ret
    else:
        t_tab = sentence.find(')')
        t = sentence[tab + 2:t_tab]
        c_tab = t.find(',')
        while c_tab != -1:
            e_tab = t.find('=')
            ret[t[0:e_tab-1]] = t[e_tab+2:e_tab+3]
            t = t[c_tab + 2:len(t)]
            c_tab = t.find(',')
        e_tab = t.find('=')
        ret[t[0:e_tab-1]] = t[e_tab+2:e_tab+3]
        return ret
def get_query_var(bn):
    ret = []
    table = bn.tables['utility']
    t = table[0]
    t = t[0:len(t)-1]
    tab = t.find('|')
    t = t[tab+2:len(t)]
    t = t.strip(' ')
    c_tab = t.find(' ')
    while c_tab != -1:
        ret.append(t[0:c_tab])
        t = t[c_tab+1:len(t)]
        c_tab = t.find(' ')
    ret.append(t)
    return ret
def get_sign(sentence):
    ret = ''
    f_tab = sentence.find('(')
    t_tab = sentence.find(')')
    t = sentence[f_tab+1:t_tab]
    tab = t.find('|')
    if tab != -1:
        t = t[0:tab-1]
    c_tab = t.find(',')
    while c_tab != -1:
        ret = ret + t[c_tab-1:c_tab]
        t = t[c_tab+2:len(t)]
        c_tab = t.find(',')
    ret = ret + t[len(t)-1:len(t)]
    return ret
def get_utility(bn,prob,X,query_known):
    ret = 0
    utility_table = bn.tables['utility']
    line_table={}
    tab = utility_table[0].find('|')
    line = utility_table[0][tab+2:len(utility_table[0])]
    line = line.strip('\n')
    line = line.strip(' ')
    match = line.split(' ')
    for i in range(1,len(utility_table)):
        line = utility_table[i].strip('\n')
        line = line.strip(' ')
        t = line.split(' ')
        l = ''
        for j in range(1,len(t)):
            l = l+t[j]
        line_table[l] = int(t[0])
    for i in range(0,2 ** len(X)):
        sign_line = ''
        x_key = generate_key(i,len(X))
        for element in match:
            for j in range(0,len(X)):
                if X[j] == element:
                    sign_line = sign_line + x_key[j]
            if query_known.has_key(element):
                sign_line = sign_line + query_known[element]
        ret = ret + line_table[sign_line] * prob[x_key]
    return ret

def enumeration_ask(X,e,bn):  #X is a list, e is a dict
    Q = {}  #dict:key:+-+,value: prob
    for i in range(0,2 ** len(X)):
        Q_key = generate_key(i,len(X))
        e_xi = copy.copy(e)
        for j in range(0,len(X)):
            e_xi[X[j]] = Q_key[j]
        Q[Q_key] = enumerate_all(bn,e_xi)
    normalize(Q)
    return Q

def enumerate_all(bn,e_xi):
    if len(bn.var) == 0:
        return 1.0
    Y = bn.var[0]
    temp_dic = copy.copy(bn.tables)
    table_Y = bn.tables[Y]
    del temp_dic[Y]
    r_bn = type_bn(bn.var[1:len(bn.var)],temp_dic)
    if e_xi.has_key(Y):
        p = get_prob(table_Y,e_xi[Y],e_xi)
        return p*enumerate_all(r_bn,e_xi)
    else:
        p1 = get_prob(table_Y,'+',e_xi)
        p2 = get_prob(table_Y,'-',e_xi)
        e_xi_plus = copy.copy(e_xi)
        e_xi_plus[Y] = '+'
        e_xi_minus = copy.copy(e_xi)
        e_xi_minus[Y] = '-'
        return p1*enumerate_all(r_bn,e_xi_plus) + p2*enumerate_all(r_bn,e_xi_minus)
'''

'''
query = []
bayesian_tables=[]
try:
    file_ob = open(sys.argv[2],'r') #to be filled
except:
    print 'cannot open file!'
    sys.exit()
while True:
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if line[0:6] == '******':
        break
    query.append(line)
table = []
while True:
    try:
        line = file_ob.readline()
    except:
        print 'Error in reading file!'
        sys.exit()
    if line == '':
        bayesian_tables.append(table)
        break
    if line[0:3] != '***':
        table.append(line)
    else:
        bayesian_tables.append(table)
        table = []
file_ob.close()

t = {}
var = []
for element in bayesian_tables:
    tab = element[0].find('|')
    if tab == -1:
        var.append(element[0][0:len(element[0])-1])
        t[element[0][0:len(element[0])-1]] = element
    else:
        if element[0][0:tab-1] != 'utility':
            var.append(element[0][0:tab-1])
        t[element[0][0:tab-1]] = element
bn = type_bn(var,t)
try:
    file_ob = open('output.txt','w'); #to be filled
except:
    print 'cannot open file!'
    sys.exit()
for element in query:
    if element[0] == 'P':
        e = {}
        X = []
        sign = ''
        element = element[2:len(element)-2]
        tab = element.find('|')
        if tab == -1:
            c_tab = element.find(',')
            while c_tab != -1:
                sign = sign + element[c_tab-1:c_tab]
                X.append(element[0:c_tab-4])
                element = element[c_tab+2:len(element)]
                c_tab = element.find(',')
            sign = sign + element[len(element)-1:len(element)]
            X.append(element[0:len(element)-4])
        else:
            query_part = element[0:tab-1]
            evidence_part = element[tab+2:len(element)]
            c_tab = query_part.find(',')
            while c_tab != -1:
                sign = sign + query_part[c_tab-1:c_tab]
                X.append(query_part[0:c_tab-4])
                query_part = query_part[c_tab+2:len(query_part)]
                c_tab = query_part.find(',')
            sign = sign + query_part[len(query_part)-1:len(query_part)]
            X.append(query_part[0:len(query_part)-4])
            c_tab = evidence_part.find(',')
            while c_tab != -1:
                e[evidence_part[0:c_tab-4]] = evidence_part[c_tab-1:c_tab]
                evidence_part = evidence_part[c_tab+2:len(evidence_part)]
                c_tab = query_part.find(',')
            e[evidence_part[0:len(evidence_part)-4]] = evidence_part[len(evidence_part)-1:len(evidence_part)]
        ans = enumeration_ask(X,e,bn)
        file_ob.write('%.2f\n'%round1(ans[sign]))
    else:
        U = {}  #key '+-+'  value:utility
        e = {}
        X = []
        query_known = {}
        decision_nodes = get_decision_nodes(element)
        dependency_var = get_dependency_var(element)
        e = dependency_var
        X = get_query_var(bn)
        for i in range(0,len(X)):
            if e.has_key(X[i]) == True:
                query_known[X[i]] = e[X[i]]
                del X[i]
        for i in range(0,2 ** len(decision_nodes)):
            d_key = generate_key(i,len(decision_nodes))
            for j in range(0,len(decision_nodes)):
                e[decision_nodes[j]] = d_key[j]
            X_d = copy.copy(X)
            for i in range(0,len(X_d)):
                if e.has_key(X_d[i]) == True:
                    query_known[X_d[i]] = e[X_d[i]]
                    del X_d[i]
            prob = enumeration_ask(X_d,e,bn)
            U[d_key]=get_utility(bn,prob,X_d,query_known)
        if element[0] == 'E':
            sign = get_sign(element)
            file_ob.write('%d\n'%round2(U[sign]))
        else:
            max_utility = float('-inf')
            max_key = ''
            print_key = ''
            for key in U:
                if U[key]>max_utility:
                    max_utility = U[key]
                    max_key = key
            print_key = ''
            for i in range(0,len(max_key)-1):
                print_key = print_key + max_key[i]
                print_key = print_key + ' '
            print_key = print_key + max_key[len(max_key)-1]
            file_ob.write('%s '%print_key)
            file_ob.write('%d\n'%round2(max_utility))
file_ob.close()
