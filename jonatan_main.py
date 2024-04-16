

def main():
    print("Welcome to Group 44's Belief Revision Agent!")
    print("Input a belief that will be added to the belief base.")

    belief_base = set()
    while True:
        belief = input("\n"+"Input a new belief that will be added to the belief base"+"\n")
        if syntax_is_valid(belief):
            if belief_base_is_satisfyable(belief, belief_base):
                belief_base.add(belief)
                belief = print("\n"+"Input was added. The belief base is now:"+"\n")
                for element in belief_base:
                    print(element)
            else:
                print("\n"+"Input was NOT added. It contradicts existing beliefs."+"\n")
                for element in belief_base:
                    print(element)
        else:
            print("\n"+"Invalid input. Try again!")

def syntax_is_valid(belief):
    if len(belief) > 0:
        return True
    return False

def belief_base_is_satisfyable(belief, belief_base):
    my_dict = {}
    # Add existing belief_base to my_dict. It is assumed to have no contradictions
    for element in belief_base:
        split_element = element.split('&')
        for subelement in split_element:
            my_dict[subelement[-1]] = evaluate(subelement)

    # Check if belief contradicts existing beliefs
    split_belief = belief.split('&')
    for subbelief in split_belief:
        if subbelief[-1] not in my_dict:
            my_dict[subbelief[-1]] = evaluate(subbelief)
        if my_dict[subbelief[-1]] ^ evaluate(subbelief):
            return False
    return True

def evaluate(element):
    if element[0] == "~":
        return False
    else:
        return True



if __name__ == "__main__":
    main()