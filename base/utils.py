def print_value(*args):
    """ Print value inside special characters to watch the value clearly """
    print("\n")
    print("+"+ "===="*20 + "+")
    print("\n")
    print(*args)
    print("\n")
    print("+"+ "===="*20 + "+")
    print("\n")


def without_keys(dictionany, keys):
    """ Return a new dictionary without specific keys """
    return {x: dictionany[x] for x in dictionany if x not in keys}