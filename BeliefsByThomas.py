
from sympy import symbols, to_cnf, And, Or
from sympy.parsing.sympy_parser import parse_expr
from itertools import combinations

class BeliefBase:
    def __init__(self, beliefs=None):
        self.beliefs = set(beliefs) if beliefs else set()

    def add_formula(self, formula):
        """ Adds a formula to the belief base, using revision if necessary. """
        conflicting_beliefs = self.find_conflicting_beliefs(formula)
        if conflicting_beliefs:
            print("Conflicting beliefs detected. Revising...")
            self.revise(formula, conflicting_beliefs)
        else:
            self.beliefs.add(formula)
            print(f"Added '{formula}' to the belief base.")
            
    def show(self):
        return self.beliefs
    
    def remove_formula(self, formula):
        self.beliefs.discard(formula)
        
    def revise(self, formula, conflicting_beliefs):
        """ Revise the belief base by contracting before adding the new formula. """
        self.contraction(conflicting_beliefs)
        self.beliefs.add(formula)
        print(f"Added '{formula}' after revision.")

    def contraction(self, conflicting_beliefs):
        """ Contract the belief base to remove conflicting beliefs using minimal change. """
        for belief in conflicting_beliefs.copy():
            self.beliefs.remove(belief)
            print(f"Removed '{belief}' to resolve contradiction.")

    def find_conflicting_beliefs(self, formula):
        """ Identify beliefs that conflict with the given formula. """
        conflicting_beliefs = set()
        clause_temp = self.beliefs.copy()
        clause_temp.add(formula)
        conflict = False
        if not resolution_entailment(BeliefBase(clause_temp), 'False'):  # Check if belief and formula together lead to contradiction
            return conflicting_beliefs  # No conflicts found, return empty set
        
        for subset_size in range(1, len(self.beliefs) + 1):
            for subset in combinations(self.beliefs, subset_size):
                super_sub = self.beliefs - set(subset)
                super_sub.add(formula)
                if not resolution_entailment(BeliefBase(super_sub), 'False'):
                    conflicting_beliefs.update(subset)
                    return conflicting_beliefs
        return conflicting_beliefs

    def entails(self, formula):
        """ Check if the belief base logically entails the given formula. """
        return resolution_entailment(self, formula)

def negate(literal):
    if literal.startswith('!'):
        return literal[1:]
    else:
        return '!' + literal



# A mapping from your operators to sympy's function calls
operator_mapping = {
    '!': '~',
}
def to_cnf2(formula_str):
    # Replace the operators in your formula with sympy's equivalents
    while '->' in formula_str or '<->' in formula_str:
        if '<->' in formula_str:
            p_index = formula_str.index('<->')
            formula_str = replace_operator(formula_str, p_index, '<->', lambda a, b: f"Equivalent({a},{b})")
        if '->' in formula_str:
            p_index = formula_str.index('->')
            formula_str = replace_operator(formula_str, p_index, '->', lambda a, b: f"Implies({a},{b})")

    for op_str, op_sympy in operator_mapping.items():
        formula_str = formula_str.replace(op_str, f' {op_sympy} ')
    
    # Create symbols for every unique alphabetical character in the string
    atomic_propositions = set(filter(str.isalpha, formula_str))
    symbols_map = {prop: symbols(prop) for prop in atomic_propositions}

    # Translate the formula string into a sympy expression
    sympy_expr = parse_expr(formula_str, local_dict=symbols_map)
    #sympy_expr = formula_str

    # Convert to CNF using sympy's to_cnf function
    cnf_expr = to_cnf(sympy_expr, simplify=True)

    # # Convert the CNF expression into a set of clauses
    if isinstance(cnf_expr, And):
        clauses = set(cnf_expr.args)

    clauses = str(clauses).replace(" ", "").replace("~", "!").replace("{","").replace("}","")
    clauses = set(clauses.split(','))

    return clauses

# def to_cnf2(formula_str):
#     # Replace the operators in your formula with sympy's equivalents
#     while '->' in formula_str or '<->' in formula_str:
#         if '<->' in formula_str:
#             p_index = formula_str.index('<->')
#             formula_str = replace_operator(formula_str, p_index, '<->', lambda a, b: f"Equivalent({a},{b})")
#         if '->' in formula_str:
#             p_index = formula_str.index('->')
#             formula_str = replace_operator(formula_str, p_index, '->', lambda a, b: f"Implies({a},{b})")

#     for op_str, op_sympy in operator_mapping.items():
#         formula_str = formula_str.replace(op_str, f' {op_sympy} ')
    
#     # Create symbols for every unique alphabetical character in the string
#     atomic_propositions = set(filter(str.isalpha, formula_str))
#     symbols_map = {prop: symbols(prop) for prop in atomic_propositions}

#     # Translate the formula string into a sympy expression
#     sympy_expr = parse_expr(formula_str, local_dict=symbols_map)
#     #sympy_expr = formula_str

#     # Convert to CNF using sympy's to_cnf function
#     cnf_expr = str(to_cnf(sympy_expr, simplify=True)).replace(" ", "").replace("~", "!")
#     if '&' in cnf_expr:
#         if '(' not in cnf_expr:
#             cnf_expr = cnf_expr.split('&')
#         else:
#             cnf_expr = set(cnf_expr[1:-1].split(')&('))
#     else:
#         cnf_expr = [cnf_expr]
    
#     return cnf_expr
    

def resolve(clause1, clause2):
    # Convert string representation of clauses to sets of literals
    c1 = set(clause1.split('|'))
    c2 = set(clause2.split('|'))
    resolved = False
    clauses = set()
    for x in c1:
        for y in c2:
            if x == negate(y):
                resolved = True
                c1_temp = c1 - {x}
                c2_temp = c2 - {y}
                new_clause = c1_temp.union(c2_temp)
                if len(new_clause) == 2:
                    new_clause_list = list(new_clause)
                    if negate(new_clause_list[0]) != new_clause_list[1]:
                        clauses.add('|'.join(new_clause))
                else:
                    clauses.add('|'.join(new_clause))
                if not new_clause:  # Empty clause found
                    return set([''])        
    if resolved:
        return clauses
    else:
        return None
    


def resolution_entailment(belief_base, formula):
    clauses = set()
    for belief in belief_base.beliefs:
        beliefs = to_cnf2(belief)
        for b in beliefs:
            clauses.add(b)
    if formula != 'False':
        negated_formula = '!' + formula
        clauses.update(to_cnf2(negated_formula))

    clauses = list(clauses)  # Convert set to list to allow indexing
    new = set()

    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if resolvents is not None:
                if resolvents == {''}:  # Found an empty clause, contradiction implies entailment
                    return True
                new.update(resolvents)

        if new.issubset(set(clauses)):  # No new clauses are added, stop the loop
            return False

        # Update clauses with new resolvents found
        clauses.extend(new - set(clauses))

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

def main_menu():
    print("\nBelief Revision Engine")
    print("1. Show Belief Base")
    print("2. Add Formula to Belief Base")
    print("3. Remove Formula from Belief Base")
    print("4. Check Formula Entailment")
    print("5. Exit")
    choice = input("Enter choice (1-5): ")
    return choice

def adds_formula(bb):
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
        adds_formula(bb)
    elif choice == '3':
        remove_formula(bb)
    elif choice == '4':
        check_entailment(bb)
    elif choice == '5':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")




