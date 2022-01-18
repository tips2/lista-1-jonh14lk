rules_file_path = "./input/rules.txt"
facts_file_path = "./input/facts.txt"
hypothesis_file_path = "./input/hypothesis.txt"


val = {}  # valor de um item ou "?" caso seja indefinido
rules = {}  # dicionário que guarda todas as regras nas quais o item x com valor y está presente como uma conclusao
hypothesis = []  # lista com as hipoteses (consultas)
rule = []  # lista que guarda todas as regras


def check_item(item):
    if item not in val:
        val[item] = "?"
        rules[item] = []


def set_fact(fact, value):
    check_item(fact)
    val[fact] = value


def set_hypothesis(h, value):
    hypothesis.append((h, value))


def add_rule(item, index):
    check_item(item)
    rules[item].append(index)


def parse_line(words):
    conditions = []
    conclusion = ("", "")
    i = 0

    while i < len(words):
        if words[i] == "se" or words[i] == "e":
            conditions.append((words[i + 1], words[i + 3]))
            i += 4
        else:
            conclusion = (words[i + 1], words[i + 3])
            i += 4

    return (conditions, conclusion)


def read_rules():
    lines = []

    with open(rules_file_path) as file:
        lines = file.readlines()

    index = 0

    for l in lines:
        parsed = parse_line(l.split())
        conditions = parsed[0]
        conclusion = parsed[1]
        rule.append((conditions, conclusion))

        for c in conditions:
            check_item(c)

        add_rule(conclusion, index)
        index += 1

    print("Regras:")
    for item in rule:
        j = 0

        while j < len(item[0]):
            print(str(item[0][j][0]) + " = " + str(item[0][j][1]), end="")
            print("" if j == len(item[0]) - 1 else " e ", end="")
            j += 1

        print(" entao ", end="")
        print(str(item[1][0]) + " = " + str(item[1][1]))

    print()


def read_facts():
    lines = []

    with open(facts_file_path) as file:
        lines = file.readlines()

    for l in lines:
        fact = l.split()
        set_fact(fact[0], fact[2])

    print("Fatos:")
    for item in val.keys():
        if val[item] != "?":
            print(str(item) + " = " + str(val[item]))
    print()


def read_hypothesis():
    lines = []

    with open(hypothesis_file_path) as file:
        lines = file.readlines()

    for l in lines:
        h = l.split()
        set_hypothesis(h[0], h[2])


def print_rule(r):
    print("Aplicando a regra " + str(r) + ": " +
          str(rule[r][1][0]) + " = " + str(rule[r][1][1]))


def dfs(item):
    check_item(item[0])

    if val[item[0]] != "?" and val[item[0]] != item[1]:
        return 0  # falso

    if val[item[0]] == item[1]:
        return 2  # verdadeiro

    if len(rules[item]) == 0:
        return 1  # inconclusivo

    flag = 1

    for r in rules[item]:
        current_flag = 2

        for child_item in rule[r][0]:
            current = dfs(child_item)

            if current == 1:
                val[child_item[0]] = child_item[1]
                current_flag = 1
            elif current == 0:
                current_flag = 0
                break

        if current_flag == 2:
            val[item[0]] = item[1]
            print_rule(r)

        if current_flag != 1:
            flag = current_flag
            break

    return flag


def answer():
    for item in hypothesis:
        flag = dfs(item)

        if flag == 2:
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é verdadeira!\n")
        elif flag == 1:
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é inconclusiva!\n")
        else:
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é falsa!\n")


def main():
    read_rules()
    read_facts()
    read_hypothesis()
    answer()


if __name__ == "__main__":
    main()
