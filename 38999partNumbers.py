# 19-35 plugs for PWM with 22D contacts
milspec = ['MS']
ms_number = ['27467']
service_class = ['E', 'P', 'T']
shell_size = ['19']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['35']
contacts = ['P']
keying = ['']

'''
# MS27056 crimp strain relief
# base = ['MS27506']
# finish = ['C', 'A', 'B', 'F']
# shell_size = ['8', '10']
# suffix = ['-2']

# crimp strain relief
# base = ['10-405982-']
# shell_size = ['08', '10']
# finish = ['0', '5', '7', '9', 'G']

# 11-4 receptacle crimp
# milspec = ['MS']
# ms_number = ['27466', '27468', '27656']
# service_class = ['E', 'P', 'T']
# shell_size = ['11']
# shell_finish = ['A', 'B', 'C', 'E', 'F']
# arrangement = ['4']
# contacts = ['S']
# keying = ['']

# 9-35 receptacle crimp
# milspec = ['MS']
# ms_number = ['27466', '27468', '27656']
# service_class = ['E', 'P', 'T']
# shell_size = ['9']
# shell_finish = ['A', 'B', 'C', 'E', 'F']
# arrangement = ['35']
# contacts = ['S']
# keying = ['']

# 11-4 plugs for less than 7.5A power with size 20 contacts
# milspec = ['MS']
# ms_number = ['27467']
# service_class = ['E', 'P', 'T']
# shell_size = ['11']
# shell_finish = ['A', 'B', 'C', 'E', 'F']
# arrangement = ['4']
# contacts = ['P']
# keying = ['']

# 9-35 plugs for PWM with 22D contacts
# milspec = ['MS']
# ms_number = ['27467']
# service_class = ['E', 'P', 'T']
# shell_size = ['9']
# shell_finish = ['A', 'B', 'C', 'E', 'F']
# arrangement = ['35']
# contacts = ['P']
# keying = ['']
'''

# for connectors
a = [milspec, ms_number, service_class, shell_size, shell_finish, arrangement, contacts, keying]

# for 10-part number backshells
# a = [base, shell_size, finish]

# for MS number backshells
# a = [base, finish, shell_size, suffix]

# concatenate a string for each combo with a bit of recursion
part_numbers = []


def combine(terms, accum):
    for i in range(len(terms[0])):
        item = accum + terms[0][i]
        if len(terms) == 1:
            part_numbers.append(item)
        else:
            combine(terms[1:], item)


combine(a, '')
for part_number in part_numbers:
    print(part_number)
