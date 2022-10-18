#1
def fibonacci(n):

    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return [0]
    if n == 1:
        return [0, 1]
    first_n_fibonacci = [0, 1]
    for i in range(2, n):
        first_n_fibonacci.append(first_n_fibonacci[i - 1] + first_n_fibonacci[i - 2])

    return first_n_fibonacci
 
#2
def prime_numbers(numbers):

    number_of_divisors = 0
    for nr in numbers:
#searching divisors till we get to rounded half of the number because
#after this point they go in pairs with the previous ones
        for d in range(2, (nr//2 + 1)):
            if nr % d == 0:
                number_of_divisors += 1
        if number_of_divisors == 0:
            return nr

#3
def list_operations(list_1, list_2):

    intersection = []
    reunion = []
    first_minus_second = []
    second_minus_first = []

    for number in list_1:
        if number in list_2 and number not in intersection:
            intersection.append(number)
    for number in list_1:
        if number not in reunion:
            reunion.append(number)
    for number in list_2:
        if number not in reunion:
            reunion.append(number)
    #list_1 - list_2 contains all the numbers of list_1 which are 
    #not in list_2  
    for number in list_1:
        if number not in list_2:
            first_minus_second.append(number)
    #list_2 - list_1 contains all the numbers of list_2 which are 
    #not in list_1
    for number in list_2:
        if number not in list_1:
            second_minus_first.append(number)
    
    return intersection, reunion, first_minus_second, second_minus_first

#5
def replace_0_matrix(matrix):

    for length in range(len(matrix)):
        for width in range(length):
            matrix[length][width] = 0

#6
def exactly_x_times(*lists, x):

    list_reunion = []

    appears_x_times = []
    #making the reunion of the lists to hold all the numbers in one container
    for param_list in lists:
        list_reunion += param_list

    #checking how many times each number appears in the big container 
    #adding it to a list with the numbers that have x repetitions 
    for number in list_reunion:
        if list_reunion.count(number) == x:
            if number not in appears_x_times:
                appears_x_times.append(number)
    return appears_x_times

#7
def palindrome(numbers):
    palindromes = []
  
    for number in numbers:
    #checking if the number is the same reversed
        if str(number) == str(number)[::-1]:
            palindromes.append(number)

    return tuple(len(palindromes), max(palindromes))

#8
def ascii(x = 1, *strings, flag = True):

    list_of_lists = []
    for string in strings:
        if flag == True:
            for character in string:
                if ord(character) % x == 0:
                    list_of_lists.append(character)
        else:
            for character in string:
                if ord(character) % x != 0:
                    list_of_lists.append(character)
    
    return list_of_lists

#9
def seats(matrix):

    spectator_seat = []
    t_matrix = list(zip(*matrix))

    for width in range(len(t_matrix)):
        for length in range(1, len(t_matrix[0])):
            if t_matrix[width][1] <= max(t_matrix)[width][:1]:
                spectator_seat.append(tuple(1, width))
    return spectator_seat
#11
def order_tuples(tuples):
    ordered = False
    while not ordered:
        ordered = True

        for i in range(0, len(tuples) - 1):
            for j in range(i + 1, len(tuples)):
                if ord(tuples[i][1][2]) > ord(tuples[j][1][2]):
                    aux =  tuples[i]
                    tuples[i] = tuples[j]
                    tuples[j] = aux

                    ordered = False 
    return tuples

if __name__ == '__main__':
    print(fibonacci(9))
    print(prime_numbers([11, 2, 6, 5, 19, 97]))
    print(list_operations([2, 5, 8, 10], [8, 10, 12, 15]))
    print(replace_0_matrix([[1, 5, 9], [10, 7, 2], [4, 5, 11]]))
    print(exactly_x_times(([11, 25, 11, 27][1, 2, 3, 4][33, 60, 55, 57, 97, 33, 33]), 2))
    print(palindrome([12321, 11111, 1234, 987]))
    print(seats([[1, 2, 3, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5]]))
    print(order_tuples([('abc', 'bcd'), ('abc', 'zza')]))