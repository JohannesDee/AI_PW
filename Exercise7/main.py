import json
import random
import numpy as np


def show_blanket(parent, relations):
    print("If you want to enter the Markov Blanked, enter the number of the node starting with 0. Otherwise enter x.")
    sel = []
    sel = input()

    if sel == 'x' or sel == 'X':
       # print("No Markov Blanked wished")
        return
    sel = int(sel)
    if sel > len(nodes)-1:
        print("selected node not existing")
        show_blanket()
        return

    child = ""

    print("The node is: ", nodes[sel])
    if nodes[sel] in parent:
        child = nodes[parent.index(nodes[sel])]

    #TODO: add parents of children!
    parchild = ""
    if relations.get(child):
        parchild = relations.get(child).get("parents")
   # for i in range(len(child)):


 #x       relations.get(child[i]).get()
    #print("Parents: ", parent[:])
    print("The parents are: ", parent[sel])
    print("The children are: ", child)
    print("Parents of the children are: ", parchild)

def give_evidence(table, table_index):
    print("Press 1 if you want to give evidence, otherwise 0")
    table_index = []
    while int(input()):
        print("For which node do you want to give evidence?")
        sel = []
        sel = input()

        if sel == 'x' or sel == 'X':
            return
        sel = int(sel)
        if sel > len(nodes)-1:
            print("selected node not existing")
            give_evidence()
            return
        print("What shall the new value be? 0 or 1")
        table[-1][sel] = int(input())
        table_index.append(sel)
        print("Press 1 for more evidence, 0 if all evidence is given.")

    return table, table_index


def check_net(prob):
    print("Check if probabilities of Bayesian Network are reasonable.")
    print(len(prob[0]), type(prob[0]))

    if (0.99 < prob[0].get('T') + prob[0].get('F') < 1.01 ) and (0.99 < prob[1].get('F,F') + prob[1].get('F,T') <1.01) and ( 0.99 < prob[1].get('T,F') + prob[1].get('T,T') <1.01) :
        print("net okay")
    else:
        print("Network is not okay. Restart program with different data")
        exit()


def check_net2(prob, nodes):
    print("Check if probabilities of Bayesian Network are reasonable.")
    for q in range(len(nodes)):
        if len(prob[q]) == 2:
            if not prob[q].get('T') + prob[q].get('F') == 1:
                print("Network not okay ")
                exit()
        elif len(prob[q]) == 4:
            if not (prob[q].get('F,F') + prob[q].get('F,T') == 1) and \
                    (prob[q].get('T,F') + prob[q].get('T,T') == 1):
                print("network is not okay")
                exit()
        elif len(prob[q]) == 8:
            if not (prob[q].get('F,F,F') + prob[q].get('F,F,T') == 1) and \
                    (prob[q].get('F,T,F') + prob[q].get('F,T,T') == 1) and \
                    (prob[q].get('T,F,F') + prob[q].get('T, F, T') == 1) and \
                    (prob[q].get('T,T,F') + prob[q].get('T,T,T') == 1):
                print("network is not okay")
                exit()
    print("Loaded network is okay.")


def MCMC(table, table_change):
    if len(table_change) == 0:
        return np.vstack((table, table[-1][:]))

    sel = random.randrange(0, len(table_change))
    sel = table_change[sel]
    table = np.vstack((table, table[-1][:]))
    #print("Changed column is: ", sel)
    if sel == 0:    # Change Flu
        if table[-1][1] == 0:   # Fever is false
            if random.uniform(0, 1) < prob[1].get('T,F') * prob[0].get('T') / (prob[1].get('T,F') * prob[0].get('T') + prob[1].get('F,F') * prob[0].get('F')):
                table[-1][0] = 1
            else:
                table[-1][0] = 0
        if table[-1][1] == 1:   # Fever is true
            if random.uniform(0, 1) < prob[1].get('T,T') * prob[0].get('T') / (prob[1].get('T,T') * prob[0].get('T') + prob[1].get('F,T') * prob[0].get('F')):
                table[-1][0] = 1
                #print("set 1")
            else:
                table[-1][0] = 0
    if sel == 1:    # Change Fever
        if table[-1][0] == 0:   # Flu is false
            if random.uniform(0, 1) < prob[1].get('F,F'):
                table[-1][1] = 0
            else:
                table[-1][1] = 1
        if table[-1][0] == 1:   # Flu is true
            if random.uniform(0, 1) < prob[1].get('T,F'):
                table[-1][1] = 0
            else:
                table[-1][1] = 1

    return table


if __name__ == '__main__':
    with open('flu.json') as json_file:
        data = json.load(json_file)
        print(data)

    nodes = data.get("nodes")
    print(nodes)
    relations = data.get("relations")
    parent = []
    prob = []
    nodes_ = []

    for i in range(len(nodes)):
      parent_ = relations.get(nodes[i]).get("parents")
      if len(parent_) == 1:
        parent.append(parent_[0])
      else:
        parent.append("")

    for i in range(len(nodes)):
        prob.append(relations.get(nodes[i]).get("probabilities"))
    prob2 = np.zeros((2, 2, 2))
    print(type(prob[0]))

    prob2[0][0] = prob[0].get('F')
    prob2[0][1] = prob[0].get('T')
    prob2[1][0][0] = prob[1].get('F,F')
    prob2[1][0][1] = prob[1].get('F,T')
    prob2[1][1][0] = prob[1].get('T,F')
    prob2[1][1][1] = prob[1].get('T,T')

    #check_net(prob)
    check_net2(prob, nodes)

    show_blanket(parent, relations)
    iterations = 10000
    print("How many iterations shall MCMC use?")
    iterations = int(input())

    table = np.zeros((1, len(nodes)))
    table_fixed = []
    table_change = []

    if random.uniform(0, 1) > prob2[0][0][0]:
        table[0][0] = 1
    temp = int(table[0][0])
    print(type(temp))
    if random.uniform(0, 1) > prob2[1][temp][0]:
        table[0][1] = 1
    table, table_fixed = give_evidence(table, table_fixed)

    for k in range(len(nodes)):
        if k not in table_fixed:
            table_change.append(k)

    for _ in range(iterations):
        table = MCMC(table, table_change)

    summe = np.sum(table, axis = 0)
    prob_flu = summe[0] / (iterations+1)
    prob_fever = summe[1] / (iterations+1)
    print("Probability of ", nodes[0], prob_flu, "Prob of ", nodes[1], prob_fever)
