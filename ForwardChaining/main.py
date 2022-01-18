rules_file_path = "./input/rules.txt"
facts_file_path = "./input/facts.txt"
hypothesis_file_path = "./input/hypothesis.txt"

val = {}  # valor de um item ou "?" caso seja indefinido
rules = {}  # dicionário que guarda todas as regras nas quais o item x com valor y está presente como uma clausula
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
            add_rule(c, index)

        check_item(conclusion)
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


def check_rule(r):
    for item in rule[r][0]:
        if val[item[0]] != item[1]:
            return False

    print("Aplicando a regra " + str(r) + ": " +
          str(rule[r][1][0]) + " = " + str(rule[r][1][1]))
    return True


def bfs():
    used = [False] * len(rule)
    queue = []

    for item in val.keys():
        if val[item] != "?":
            queue.append((item, val[item]))

    while queue:
        item = queue.pop(0)

        for r in rules[item]:
            if used[r]:
                continue

            if check_rule(r):
                used[r] = 1
                val[rule[r][1][0]] = rule[r][1][1]
                queue.append(rule[r][1])


def read_hypothesis():
    lines = []

    with open(hypothesis_file_path) as file:
        lines = file.readlines()

    for l in lines:
        h = l.split()
        set_hypothesis(h[0], h[2])


def answer():
    print()

    for item in hypothesis:
        check_item(item[0])
        if val[item[0]] == item[1]:
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é verdadeira!\n")
        elif val[item[0]] == "?":
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é inconclusiva!\n")
        else:
            print("Hipotese (" + str(item[0]) +
                  " = " + str(item[1]) + ") é falsa!\n")


def main():
    read_rules()
    read_facts()
    bfs()
    read_hypothesis()
    answer()


if __name__ == "__main__":
    main()
