""" tools.py """


def groupBy(iterable, keyer, valuer=lambda e: e):
    dictionary = {}
    done = 0
    for item in iterable:
        key = keyer(item)
        if key not in dictionary:
            dictionary[key] = [valuer(item)]
        else:
            dictionary[key].append(valuer(item))
        done += 1
    return dictionary
