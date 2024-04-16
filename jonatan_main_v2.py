import copy

def main():
    print("Welcome to Group 44's Belief Revision Agent!")
    print("Input a belief that will be added to the belief base.")

    belief_base = set()
    while True:
        belief = input("\n"+"Input a new belief that will be added to the belief base"+"\n")
        if syntax_is_valid(belief):
            if belief_base_is_satisfyable(belief, belief_base):
                belief_base.add(belief)
                print_green("\n"+"Input was added. The belief base is now:"+"\n")
                for element in belief_base:
                    print(element)
            else:
                print_red("\n"+"Input was NOT added. It contradicts existing beliefs."+"\n")
                for element in belief_base:
                    print(element)
        else:
            print("\n"+"Invalid input. Try again!")

def syntax_is_valid(belief):
    if len(belief) > 0:
        return True
    return False

def belief_base_is_satisfyable(belief, belief_base):
    empty_belief_base = {}
    world_interpretations = [empty_belief_base]
    # Add existing belief_base to my_dict. It is assumed to have no contradictions
    for existing_belief in belief_base:
        process_belief(existing_belief, world_interpretations)

    # Check if belief contradicts existing beliefs
    for my_dict in world_interpretations:
        if world_interpretation_has_no_contradiction(belief, my_dict):
            return True
    return False

def world_interpretation_has_no_contradiction(belief, my_dict):
    and_split = belief.split('&')
    for subbelief in and_split:
        or_split = subbelief.split('|')
        true_found = False
        for subsubbelief in or_split:
            if subsubbelief[-1] not in my_dict:
                my_dict[subsubbelief[-1]] = evaluate(subsubbelief)
                true_found = True
            if my_dict[subsubbelief[-1]] == evaluate(subsubbelief):
                true_found = True
        if not true_found:
            return False
    return True


def process_belief(belief, world_interpretations):
    and_split = belief.split('&')
    for subelement in and_split:
        or_split = subelement.split('|')
        new_world_interpretations = []
        for world_interpretation in world_interpretations:
            if len(or_split) == 1:
                world_interpretation[subelement[-1]] = evaluate(subelement)
            elif len(or_split) > 1:
                for subsubelement in or_split:
                    copied_world_interpretation = copy.deepcopy(world_interpretation)
                    copied_world_interpretation[subsubelement[-1]] = evaluate(subsubelement)
                    new_world_interpretations.append(copied_world_interpretation)
        for new_world_interpretation in new_world_interpretations:
            world_interpretations.append(new_world_interpretation)

def evaluate(element):
    if element[0] == "~":
        return False
    else:
        return True

def or_combinations(or_statement):
    new_world_interpretations = {}
    element = or_statement.split('|')
    for subelement in element:
        new_world_interpretations[subelement[-1]] = evaluate(subelement)


def print_red(text):
    print("\033[91m"+text+"\033[0m")

def print_green(text):
    print("\033[92m"+text+"\033[0m")

if __name__ == "__main__":
    main()