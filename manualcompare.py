from climvc.exceptions import Cancel
from mylibrary import initials

from decisionmaker import Choice


def manual_compare(x: Choice, y: Choice):
    if not x.value or not y.value:
        values = x.scale.values
        keys = initials(values)
        for choice in (x, y):
            if not choice.value:
                print('Rating for ' + str(choice) + ': ')
                for value, key in zip(values, keys):
                    print(value + ' (' + key + ')', end='')
                    if values.index(value) + 1 != len(values):
                        print(', ')
                    if values.index(value) + 1 == len(values) - 1:
                        print('or ', end='')
                print('? ', end='')
                while True:
                    try:
                        choice.value = values[keys.index(input())]
                        break
                    except ValueError:
                        print("That's not one of the choices. Try again.")
                print()
        return x > y
    else:
        choices = {";": True, "'": False}
        while True:
            response = input(str(x) + " (;) or " + str(y) + " (')?")
            try:
                print()
                choice = choices[response]
                return choice
            except KeyError:
                if response == 'x':
                    raise Cancel
                else:
                    print("That's not one of the choices. Try again.")