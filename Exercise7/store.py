if table[-1][1] == 0:  # Fever is false
    if random.uniform(0, 1) < prob[1].get('T,F') * prob[0].get('F') / (
            prob[1].get('T,T') * prob[0].get('T') + prob[1].get('F,F') * prob[0].get('F')):
        table[-1][0] = 1
    else:
        table[-1][0] = 0
if table[-1][1] == 1:  # Fever is true
    if random.uniform(0, 1) < prob[1].get('T,T') * prob[0].get('T') / (
            prob[1].get('T,T') * prob[0].get('T') + prob[1].get('F,T') * prob[0].get('F')):
        table[-1][0] = 1
        # print("set 1")
    else:
        table[-1][0] = 0
if sel == 1:  # Change Fever
    if table[-1][0] == 0:  # Flu is false
        if random.uniform(0, 1) < prob[1].get('F,F'):
            table[-1][1] = 0
        else:
            table[-1][1] = 1
    if table[-1][0] == 1:  # Flu is true
        if random.uniform(0, 1) < prob[1].get('T,F'):
            table[-1][1] = 0
        else:
            table[-1][1] = 1
