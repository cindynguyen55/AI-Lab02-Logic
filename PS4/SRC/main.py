import os


def negavtive_literal(literal):
    if (literal[0] == '-'):
        return literal[1]
    else:
        return '-'+literal[0]


class Clause:
    def __init__(self, literals):
        self.literal_list = literals

        if (len(literals) == 0):
            self.count = 0
        elif (len(literals) == 1):
            if (literals[0] == r'{}'):
                self.count = -1
            else:
                self.count = 1
        else:
            self.count = len(literals)

    def negative(self):
        clause_list = []

        for literal in self.literal_list:
            clause_list.append(Clause([negavtive_literal(literal)]))

        return clause_list

    def __str__(self):
        if self.count == 0:
            return ''
        else:
            s = ''
            for literal in self.literal_list[0:-1]:
                s += literal + ' OR '
            return s + self.literal_list[-1]

    def __eq__(self, clause):
        return self.literal_list == clause.literal_list


def sort_key(s):
    return s[-1]

def canResolve(c1: Clause, c2: Clause):
    check = 0

    for liter1 in c1.literal_list:
        for liter2 in c2.literal_list:
            if (liter2 == negavtive_literal(liter1)):
                check+=1
                if check==2:
                    return False

    if check==1:
        return True
    else:
        return False


def resolve(c1: Clause, c2: Clause):
    check=0

    for liter1 in c1.literal_list:
        for liter2 in c2.literal_list:
            if (liter2 == negavtive_literal(liter1)):
                liters1 = c1.literal_list.copy()
                liters1.remove(liter1)
                liters2 = c2.literal_list.copy()
                liters2.remove(liter2)
                liters = liters1+liters2
                check=1
                break
        
        if check==1:
            if (len(liters) == 0):
                return Clause([r'{}'])

            return Clause(sorted(list(set(liters)), key=sort_key))

    return Clause([])


def PL_Resolution(KB: list, alpha: Clause, output_file: str):
    f = open(output_file, 'w', encoding='utf-8')
    solve = 0
    prevlenClause = 0
    clauses = KB+alpha.negative()

    while True:
        new = []
        for i in range(prevlenClause, len(clauses)):
            for j in range(i+1, len(clauses)):
                if canResolve(clauses[i], clauses[j]):
                    newClause = resolve(clauses[i], clauses[j])
                    if not ((newClause in clauses) or (newClause in new) or (newClause.count == 0)):
                        new.append(newClause)

            for j in range(0, prevlenClause):
                if canResolve(clauses[i], clauses[j]):
                    newClause = resolve(clauses[i], clauses[j])
                    if not ((newClause in clauses) or (newClause in new) or (newClause.count == 0)):
                        new.append(newClause)

        f.write(str(len(new)))
        f.write('\n')
        for liters in new:
            if (liters.count == -1):
                solve = 1
            f.write(str(liters))
            f.write('\n')

        if (len(new) == 0):
            f.write('NO')
            f.close()
            return False

        if (solve == 1):
            f.write('YES')
            f.close()
            return True

        prevlenClause = len(clauses)
        clauses = clauses + new


def input(input_flie):
    f = open(input_flie, 'r')
    data = f.readlines()
    f.close()
    temp = data[0].replace('\n', '').replace(' ', '').split('OR')
    alpha = Clause(sorted(list(set(temp)), key=sort_key))
    count = int(data[1])
    KB = []

    for i in range(2, count+2):
        temp = data[i].replace('\n', '').replace(' ', '').split('OR')
        KB.append(Clause(sorted(list(set(temp)), key=sort_key)))

    return KB, alpha


def main():
    file_list = os.listdir(os.getcwd()+'/INPUT')

    for file in file_list:
        fi = 'INPUT/'+file
        fo = fi.replace('INPUT', 'OUTPUT').replace('input', 'output')
        KB, alpha = input(fi)
        PL_Resolution(KB, alpha, fo)


if __name__ == "__main__":
    main()
