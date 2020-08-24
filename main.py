import itertools

def readKB(infile):
    query = []
    KB = []
    with open(infile, 'rt') as fi:
        num_query = int(fi.readline())
        for i in range(num_query):
           query.append(fi.readline().strip().split('\n'))

        num_KB = int(fi.readline())
        for i in range(num_KB):
            clause = fi.readline().strip().split(' OR ')
            KB.append(clause)
    return KB, query
def Resolution(KB, alpha, fo):
    clauses = KB.copy()
    for a in range(len(alpha)):
        if '-' in alpha[a]:
            not_alpha = alpha[a].replace('-', '')
        else:
            not_alpha = '-' + alpha[a]
        clauses.append([not_alpha])
    new = []

    while True:
        countNewClause = 0
        # Tổ hợp chập 2
        for pair_clauses in itertools.combinations(clauses, 2):
            if isComplementaryClause(list(pair_clauses[0] + pair_clauses[1])):
                resolvents = Resolve(pair_clauses)

                if len(resolvents) == 0:
                    countNewClause += 1
                    fo.write(str(countNewClause) + '\n')
                    for i in range(len(new)):
                        for j in range(len(new[i])):
                            if j != len(new[i]) - 1:
                                fo.write(str(new[i][j]) + ' OR ')
                            else:
                                fo.write(new[i][j])
                        fo.write('\n')
                    fo.write('{}\nYES\n')
                    return True

                # Sort resolvents following the alphabetical order.
                resolvents = sorted(resolvents, key=lambda x:x[-1])

                if not(isComplementaryClause(resolvents)) and (resolvents not in clauses) and(resolvents not in new):
                    new.append(resolvents)
                    countNewClause += 1

        if len(new) == 0:
            fo.write("0\nNO\n")
            return False

        # Output txt
        fo.write(str(countNewClause) + '\n')
        for i in range(len(new)):
            for j in range(len(new[i])):
                if j != len(new[i]) - 1:
                    fo.write(new[i][j] + ' OR ')
                else:
                    fo.write(new[i][j])
            fo.write('\n')

        clauses = clauses + new
        new.clear()

def Resolve(pair_clauses):
    clauses_1 = pair_clauses[0].copy()
    clauses_2 = pair_clauses[1].copy()
    complementary_once = False
    for cl1 in pair_clauses[0]:
        for cl2 in pair_clauses[1]:
            if ((cl1 == ('-' + cl2)) or ('-' + cl1 == cl2)) and not(complementary_once):
                clauses_1.remove(cl1)
                clauses_2.remove(cl2)
                complementary_once = True

            if (cl1 == cl2):
                clauses_2.remove(cl2)
                break


    return list(clauses_1 + clauses_2)

def isComplementaryClause(resolvents):
    for i in range(len(resolvents)):
        for j in range(len(resolvents)):
            if (resolvents[i] == ('-' + resolvents[j])) or ('-' + resolvents[i] == resolvents[j]):
                return True
    return False

def checkSubset(a, b):
    count = 0
    for a_ in a:
        for b_ in b:
            if a_ == b_:
                count += 1
                break

    if count == len(a):
        return True
    else:
        return False

if __name__ == '__main__':
    # KB = [['-R', 'U'], ['-U', '-W'], ['R', '-W']]
    # check = Resolution(KB, '-W')

    # KB = [['-A', 'B', 'C'], ['-B', 'A'], ['-C', 'A'], ['-A']]
    # check = Resolution(KB, '-B')

    # KB = [['-A', 'B'], ['B', '-C'], ['A', '-B', 'C'], ['-B']]
    # check = Resolution(KB, ['A'])
    #
    # print(check)
    infile = 'Input.txt'
    outfile = 'Output.txt'
    KB, query = readKB(infile)
    with open(outfile, 'wt') as fo:
        for i in range(len(query)):
            check = Resolution(KB, query[i], fo)





