# Charlie Johnson
# 2022-05-10
# create permutations of part numbers


# 11-35 receptacles for CAN/serial/12V power/other things
a = [['MS'],  # milspec
     ['27466', '27468', '27656'],  # ms number
     ['E'],  # service class
     ['11'],  # shell size
     ['B'],  # shell finish
     ['35'],  # arrangement
     ['S'],  # contacts
     ['']]  # keying

# 9-98 receptacles for servos with size 20 contacts
# a = [['MS'],  # milspec
#      ['27466', '27468', '27656'],  # ms number
#      ['E'],  # service class
#      ['9'],  # shell size
#      ['B'],  # shell finish
#      ['98'],  # arrangement
#      ['S'],  # contacts
#      ['']]  # keying

# 11-2 receptacle for big servo motor power
# a = [['MS'],  # milspec
#      ['27466', '27468', '27656'],  # ms number
#      ['E'],  # service class
#      ['11'],  # shell size
#      ['B'],  # shell finish
#      ['2'],  # arrangement
#      ['S'],  # contacts (P for plug or S for receptacle)
#      ['']]  # keying

# 11-2 plug for big servo motor power
# a = [['MS'],  # milspec
#      ['27467'],  # ms number
#      ['E'],  # service class
#      ['11'],  # shell size
#      ['B'],  # shell finish
#      ['2'],  # arrangement
#      ['P'],  # contacts (P or S)
#      ['']]  # keying

# 23-35 plug for autopilot
# a = [['MS'],  # milspec
#      ['27467'],  # ms number
#      ['E'],  # service class
#      ['23'],  # shell size
#      ['A', 'B', 'C', 'E', 'F'],  # shell finish
#      ['35'],  # arrangement
#      ['P'],  # contacts (P or S)
#      ['']]  # keying


# 23-35 receptacles for autopilot
# a = [['MS'],  # milspec
#      ['27466', '27468', '27656'],  # ms number
#      ['E'],  # service class
#      ['23'],  # shell size
#      ['A', 'B', 'C', 'E', 'F'],  # shell finish
#      ['35'],  # arrangement
#      ['S'],  # contacts (P or S)
#      ['']]  # keying


# # M85049/49 crimp strain relief
# a = [['M85049/49-2-'],  # base
#      ['08', '8', '10', '18'],  # shell size
#      ['A', 'W', 'N']]  # finish

'''
These are a bunch of ones in a different syntax. Easy to convert
# 11-35 plugs for CAN/serial/12V power/other things
milspec = ['MS']
ms_number = ['27467']
service_class = ['E']
shell_size = ['11']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['35']
contacts = ['P']
keying = ['']


# 9-98 plugs for servos with size 20 contacts
milspec = ['MS']
ms_number = ['27467']
service_class = ['E']
shell_size = ['9']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['98']
contacts = ['P']
keying = ['']


# 19-35 plugs for PWM with 22D contacts
milspec = ['MS']
ms_number = ['27467']
service_class = ['E']
shell_size = ['19']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['35']
contacts = ['P']
keying = ['']

# MS27056 crimp strain relief
base = ['MS27506']
finish = ['C', 'A', 'B', 'F']
shell_size = ['8', '10', '18']
suffix = ['-2']

# crimp strain relief
base = ['10-405982-']
shell_size = ['08', '10']
finish = ['0', '5', '7', '9', 'G']

# 11-4 receptacle crimp
milspec = ['MS']
ms_number = ['27466', '27468', '27656']
service_class = ['E']
shell_size = ['11']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['4']
contacts = ['S']
keying = ['']

# 9-35 receptacle crimp
milspec = ['MS']
ms_number = ['27466', '27468', '27656']
service_class = ['E']
shell_size = ['9']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['35']
contacts = ['S']
keying = ['']

# 11-4 plugs for less than 7.5A power with size 20 contacts
milspec = ['MS']
ms_number = ['27467']
service_class = ['E']
shell_size = ['11']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['4']
contacts = ['P']
keying = ['']

# 9-35 plugs for PWM with 22D contacts
milspec = ['MS']
ms_number = ['27467']
service_class = ['E']
shell_size = ['9']
shell_finish = ['A', 'B', 'C', 'E', 'F']
arrangement = ['35']
contacts = ['P']
keying = ['']
'''

# concatenate a string for each combo with a bit of recursion
part_numbers = []


def combine(terms, accum):
    for i in range(len(terms[0])):
        item = accum + terms[0][i]
        if len(terms) == 1:
            part_numbers.append(item)
        else:
            combine(terms[1:], item)

if __name__ == '__main__':
    combine(a, '')
    for part_number in part_numbers:
        print(part_number)
