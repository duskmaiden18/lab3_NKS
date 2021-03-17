import networkx as nx
import matplotlib.pyplot as plt
import itertools
import math

t = 1000
K1 = 1
K2 = 1

if K1 <= 0 or K2 <= 0:
    print("Помилка: кратність повинна бути більше 0")
    raise SystemExit

if t<=0:
    print("Помилка: час повинен бути більше 0")
    raise SystemExit

P = [0, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.92, 0.94 ,0]
len_P = len(P)
for i in P:
    if i<0 or i>1:
        print("Помилка: ймовірності повинні бути в межах від 0 до 1")
        raise SystemExit

matrix_conn = [ [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]

for i in range(len(matrix_conn)):
    if len(matrix_conn) != len(matrix_conn[i]):
        print("Помилка: матриця не квадратна")
        raise SystemExit
if len(matrix_conn) != len_P:
    print("Помилка: розмірність матриці та кількість введених ймовірностей не співпадають")
    raise SystemExit
for i in matrix_conn:
    for j in i:
        if j!=1 and j!=0:
            print("Помилка: значення в таблиці звязків повинні бути 0 або 1")
            raise SystemExit

G = nx.DiGraph()
for i in range(len(matrix_conn)):
    for j in range(len(matrix_conn[0])):
        if matrix_conn[i][j] == 1:
            G.add_edge(i,j)
nx.draw_networkx(G)
plt.show()

def find_paths(G, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not G.has_node(start):
        return []
    paths = []
    for i in G[start]:
        if i not in path:
            paths_new = find_paths(G, i, end, path)
            for path_new in paths_new:
                paths.append(path_new)
    return paths

paths = find_paths(G, 0, len(P) - 1)

# print("Усі можливі шляхи (всього",len(paths),"):")
# for i in paths:
#     print(i[1:len(i)-1])
# print("\n")

def get_working_cond(paths):
    cond = []
    for path in paths:
        tmp = path[1:len(path) - 1]
        cond.append(tmp)
    node_max = max([max(path) for path in cond])
    nodes = list(range(1, node_max + 1))
    cond.append(nodes)
    for i in cond:
        nodes_new = nodes.copy()
        i_nodes = [x for x in nodes_new if x not in i]
        for j in range(1, len(i_nodes)):
            comb_i_nodes = list(itertools.combinations(i_nodes, j))
            for k in comb_i_nodes:
                i_new = i.copy()
                i_new.extend(k)
                i_new.sort()
                if i_new not in cond:
                    cond.append(i_new)
    return sorted(cond,key=len), node_max

cond, node_max = get_working_cond(paths)

def get_P_states(cond, node_max, P):
    nodes = list(range(1, node_max + 1))
    P_states = []
    for i in cond:
        p_tmp = 1
        i_nodes = [x for x in nodes if x not in i]
        for node in i:
            p_tmp *= P[node]
        for node in i_nodes:
            tmp = 1 - P[node]
            p_tmp *= tmp
        P_states.append(round(p_tmp,6))
    return P_states

P_states = get_P_states(cond,node_max,P)
# print("Працездатні стани системи та ймовірності знаходження системи у цьому стані:")
# for i in range(len(cond)):
#     print(cond[i],P_states[i])
# print("\n")

P_sum = round(sum(P_states),6)
print("Ймовірність безвідмовної роботи протягом ",t,"годин Psystem = ",P_sum)

Q = 1 - P_sum
print("Ймовірність відмови протягом ",t,"годин Qsystem = ",Q)

l = -math.log(P_sum)/t
print("Значення ітенсивності відмов λ = ",round(l,6))

T_ndv = 1/l
print("Середній наробіток до відмови Тндв = ", round(T_ndv,6))

def factorial(n):
    res = 1
    for i in range(n):
        res *= i
    return n

Q_reserved_system = 1/factorial(K1+1)*Q
print("\nЙмовірність відмови на час",t,"годин системи з загальним ненавантаженим "
                                     "резервуванням з кратністю",K1, " Qreserved_system = ", round(Q_reserved_system,6))

P_reserved_system = 1 - Q_reserved_system
print("Ймовірність безвідмовної роботи на час",t,"годин системи з загальним ненавантаженим "
                                     "резервуванням з кратністю",K1, " Preserved_system = ", round(P_reserved_system,6))

l2 = -math.log(P_reserved_system)/t
T_ndv2 = 1/l2
print("Середній наробіток до відмови Тндв = ", round(T_ndv2,6))

Gq = Q_reserved_system / Q
print("Виграш надійності протягом часу",t," годин за ймовірністю відмов Gq = ", round(Gq,6))

Gp = P_reserved_system / P_sum
print("Виграш надійності протягом часу",t," годин за ймовірністю безвідмовної роботи Gp = ", round(Gp,6))

Gt = T_ndv2 / T_ndv
print("Виграш надійності за середнім часом безвідмовної роботи Gt = ", round(Gt,6),"\n")

def Q_P_each_element(P,K2):
    Q_new = []
    P_new = []
    for i in P:
        tmp = pow(1 - i, K2 + 1)
        Q_new.append(tmp)
        P_new.append(1 - tmp)
    return Q_new, P_new

Q_reserved, P_reserved = Q_P_each_element(P, K2)
for i in range(1,len(Q_reserved)-1):
    print('Qreserved',i,'=', Q_reserved[i], ", Preserved",i,'=',P_reserved[i])

P_states2 = get_P_states(cond,node_max,P_reserved)

P_reserved_system2 = round(sum(P_states2),6)
print("\nЙмовірність безвідмовної роботи на час",t,"годин системи з роздільним навантаженим "
                                     "резервуванням з кратністю",K2, " Preserved_system = ",round(P_reserved_system2,6))

Q_reserved_system2 = 1 - P_reserved_system2
print("Ймовірність відмови на час",t,"годин системи з роздільним навантаженим "
                                     "резервуванням з кратністю",K2, " Qreserved_system = ", round(Q_reserved_system2,6))

l3 = -math.log(P_reserved_system2)/t
T_ndv3 = 1/l3
print("Середній наробіток до відмови Тндв = ", round(T_ndv3,6))

Gq2 = Q_reserved_system2 / Q
print("Виграш надійності протягом часу",t," годин за ймовірністю відмов Gq = ", round(Gq2,6))

Gp2 = P_reserved_system2 / P_sum
print("Виграш надійності протягом часу",t," годин за ймовірністю безвідмовної роботи Gp = ", round(Gp2,6))

Gt2 = T_ndv3 / T_ndv
print("Виграш надійності за середнім часом безвідмовної роботи Gt = ", round(Gt2,6))

