import re

class BeliefBase:
    def __init__(self):
        self.beliefs = set()

    def add_formula(self, formula):
        self.beliefs.add(formula)

    def remove_formula(self, formula):
        self.beliefs.discard(formula)

    def show(self):
        return self.beliefs

def negate(literal):
    if literal.startswith('-'):
        return literal[1:]
    else:
        return '-' + literal

def distribute(or_clause1, or_clause2):
    new_clause = set()
    for a in or_clause1:
        for b in or_clause2:
            if isinstance(a, set) and isinstance(b, set):
                new_clause.add(frozenset(a.union(b)))
            elif isinstance(a, set):
                new_clause.add(frozenset(a.union({b})))
            elif isinstance(b, set):
                new_clause.add(frozenset({a}.union(b)))
            else:
                new_clause.add(frozenset({a, b}))
    return new_clause





def to_cnf(formula):
    print(f"Original formula: {formula}")
    formula = formula.replace(" ", "")  # Remove spaces

    # Handle implications and biconditionals
    formula = replace_implications_and_biconditionals(formula)
    print(f"Formula after handling implications and biconditionals: {formula}")

    # Convert to CNF recursively and handle distributions
    cnf_formula = convert_to_cnf_recursive(formula)
    return cnf_formula or set()

def replace_implications_and_biconditionals(formula):
    while '->' in formula or '<->' in formula:
        if '<->' in formula:
            p_index = formula.index('<->')
            formula = replace_operator(formula, p_index, '<->', lambda a, b: f"(({a}&{b})|(!{a}&!{b}))")
        if '->' in formula:
            p_index = formula.index('->')
            formula = replace_operator(formula, p_index, '->', lambda a, b: f"(!{a}|{b})")
    print(f"Formula after handling implications and biconditionals: {formula}")
    return formula

def replace_operator(formula, op_index, operator, replacement_func):
    left_expr, left_start, left_end = find_bound_expression(formula, op_index, -1)
    right_expr, right_start, right_end = find_bound_expression(formula, op_index + len(operator), 1)
    replacement = replacement_func(left_expr, right_expr)
    return formula[:left_start] + replacement + formula[right_end:]

def find_bound_expression(formula, index, direction):
    if direction == -1:  # Search backward for left expression
        depth = 0
        for i in range(index - 1, -1, -1):
            if formula[i] == ')': depth += 1
            elif formula[i] == '(': depth -= 1
            if depth == 0 and (i == 0 or formula[i-1] in '(&|'):
                return formula[i:index], i, index
    else:  # Search forward for right expression
        depth = 0
        length = len(formula)
        for i in range(index, length):
            if formula[i] == '(': depth += 1
            elif formula[i] == ')': depth -= 1
            if depth == 0 and (i == length - 1 or formula[i+1] in ')&|'):
                return formula[index:i+1], index, i+1
    return None  # in case of unbalanced expressions

def convert_to_cnf_recursive(formula):
    if formula.isalpha() or (formula.startswith('-') and formula[1:].isalpha()):
        return {frozenset([formula])}

    if formula.startswith('!'):
        inner = convert_to_cnf_recursive(formula[1:])
        if inner is not None:
            return {frozenset({negate(x) for x in clause}) for clause in inner}

    depth = 0
    for i, char in enumerate(formula):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif depth == 0 and char in '|&':
            left = convert_to_cnf_recursive(formula[:i])
            right = convert_to_cnf_recursive(formula[i+1:])
            if left is None or right is None:
                return None
            if char == '|':
                return distribute_or(left, right)
            elif char == '&':
                return left.union(right)
            break
    print("distribute_or: " + formula)
    if formula.startswith("(") and formula.endswith(")"):
        return convert_to_cnf_recursive(formula[1:-1])

    return None

def distribute_or(or_sets_1, or_sets_2):
    result = set()
    for s1 in or_sets_1:
        for s2 in or_sets_2:
            result.add(frozenset(s1.union(s2)))
    return result







def resolve(ci, cj):
    resolvents = set()
    for x in ci:
        for y in cj:
            if x == negate(y):
                new_clause = ci.union(cj) - {x, y}
                if not new_clause:  # Empty clause found
                    return {frozenset()}
                resolvents.add(frozenset(new_clause))
    return resolvents

def resolution_entailment(belief_base, formula):
    clauses = set()
    for belief in belief_base.beliefs:
        clauses.update(to_cnf(belief))
    negated_formula = '!' + formula
    clauses.update(to_cnf(negated_formula))

    clauses = list(clauses)  # Convert set to list to allow indexing
    new = set()

    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:  # Found an empty clause, contradiction implies entailment
                return True
            new.update(resolvents)

        if new.issubset(set(clauses)):  # No new clauses are added, stop the loop
            return False

        # Update clauses with new resolvents found
        clauses.extend(new - set(clauses))


def contract(belief_base, formula):
    belief_base.remove_formula(formula)

def expand(belief_base, formula):
    belief_base.add_formula(formula)


def main_menu():
    print("\nBelief Revision Engine")
    print("1. Show Belief Base")
    print("2. Add Formula to Belief Base")
    print("3. Remove Formula from Belief Base")
    print("4. Check Formula Entailment")
    print("5. Exit")
    choice = input("Enter choice (1-5): ")
    return choice

def add_formula(bb):
    print("\nFormula Syntax Guide:")
    print("Logical Operators Allowed:")
    print("  ! : NOT")
    print("  & : AND")
    print("  | : OR")
    print("  -> : IMPLICATION (use as a->b for a implies b)")
    print("  <-> : BICONDITIONAL (use as a<->b for a if and only if b)")
    print("Use parentheses to group expressions as needed.")
    formula = input("Enter a formula to add to the belief base: ")
    bb.add_formula(formula)
    print("Formula added successfully.")

def remove_formula(bb):
    formula = input("Enter a formula to remove from the belief base: ")
    if formula in bb.beliefs:
        bb.remove_formula(formula)
        print("Formula removed successfully.")
    else:
        print("Formula not found in the belief base.")

def check_entailment(bb):
    print("\nCheck Formula Entailment:")
    print("Enter a formula using the logical operators !, &, |, ->, <->.")
    formula = input("Enter a formula to check entailment: ")
    if resolution_entailment(bb, formula):
        print("The belief base entails the formula.")
    else:
        print("The belief base does not entail the formula.")

bb = BeliefBase()
while True:
    choice = main_menu()
    if choice == '1':
        print("Current Belief Base:", bb.show())
    elif choice == '2':
        add_formula(bb)
    elif choice == '3':
        remove_formula(bb)
    elif choice == '4':
        check_entailment(bb)
    elif choice == '5':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")




