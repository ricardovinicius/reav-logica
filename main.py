def hypothetical_syllogism(premise, premises):
    for i in range(len(premises)):
        sentence = premises[i]
        parts = sentence.split("->")
        if len(parts) != 2:
            continue
        
        antecedent = parts[0].strip()
        consequent = parts[1].strip()
        
        if premise == antecedent:
            return consequent
    
    return premise


def modus_tollens(premise, premises):
    for i in range(len(premises)):
        sentence = premises[i]
        parts = sentence.split("->")
        if len(parts) != 2:
            continue

        antecedent = parts[0].strip()
        consequent = parts[1].strip()

        if consequent == premise[1]:
            premises[i] = '~' + antecedent  # Replace the premise with the derived conclusion

    return premises


def modus_ponens(premise, premises):
    for i in range(len(premises)):
        sentence = premises[i]
        parts = sentence.split("->")
        if len(parts) != 2:
            continue

        antecedent = parts[0].strip()
        consequent = parts[1].strip()

        if antecedent == premise:
            premises[i] = consequent  # Replace the premise with the derived conclusion

    return premises


def and_elimination(premise, premises):
    updated_premises = []  # Create a new list to store the updated premises

    for sentence in premises:
        parts = sentence.split("->")
        if len(parts) != 2:
            updated_premises.append(sentence)  # Add non-implication premises as is
            continue

        antecedent = parts[0].replace("(", "").replace(")", "").strip()
        consequent = parts[1].replace("(", "").replace(")", "").strip()

        if "&" in antecedent:
            mini_parts = antecedent.split("&")
            a = mini_parts[0].strip()
            b = mini_parts[1].strip()
            if a in premises and b in premises:
                updated_premises.append(consequent)  # Add the conclusion to updated premises

        if "&" in consequent:
            mini_parts = consequent.split("&")
            a = mini_parts[0].strip()
            b = mini_parts[1].strip()
            if a in premises and b in premises:
                updated_premises.append(antecedent)  # Add the conclusion to updated premises
    
    return updated_premises


premises = [
    "A -> B",
    "~B",
    "B -> C",
    "S -> V",
    "V -> Q",
    "S",
    "Q -> R"
]
conclusion = "R" 

previous = None
# Modus tollens
while previous != premises:
    previous = list(premises)
    for premise in premises:
        if len(premise) == 2 and premise[0] == '~':
            premises = modus_tollens(premise, premises)

previous = None
# Hypothetical syllogism
while previous != premises:
    previous = list(premises)
    for i in range(len(premises)):
        if "->" in premises[i]:
            parts = premises[i].split("->")
            consequent = parts[1].strip()
            new_consequent = hypothetical_syllogism(consequent, premises)
            premises[i] = premises[i].replace(consequent, new_consequent)

previous = None
# Modus ponens
while previous != premises:
    previous = list(premises)
    for premise in premises:
        if len(premise) == 1:
            premises = modus_ponens(premise, premises)

# Elimination of '&'
for premise in premises:
    if "&" in premise:
        premises = and_elimination(premise, premises)

# TODO: Disjunctive syllogism

if conclusion in premises:
    print("Valid argument")        
else:
    print("Invalid argument")

print(premises)
