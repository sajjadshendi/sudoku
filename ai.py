import json
import random
from random import randint
import copy


# *** you can change everything except the name of the class, the act function and the problem_data ***


class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self, population_count):
        #تعداد کروموزوم ها
        self.population_count = population_count

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        # ^^^ DO NOT change the solve function above ***
        problem_data = json.loads(problem)
        # ^^^ DO NOT change the problem_data above ***
        problem_data_cp = copy.deepcopy(problem_data)
        data = problem_data_cp["sudoku"]
        population = self.make_population(data)
        flag = False
        while (True):
            new_population = []
            count = len(population)
            for j in range(count):
                x_index, y_index = self.make_two_chice_from_population(data, population)
                x = population[x_index[0]]
                y = population[y_index[0]]
                child = self.reproduce(x, y)
                child = self.MUTATE(data, child)
                new_population.append(child)
                if(self.goal_test(data, child)):
                    finished = child
                    flag = True
                    self.show(data, child)
                    break
            if(flag):
                break
            population = new_population
        # finished is the solved version
        return finished

    #تابع ساخت کروموزوم های اولیه
    def make_population(self, init_data):
        population = []
        for i in range(self.population_count):
            sudoku_table = []
            for row in init_data:
                sudoku_table_row = []
                for column in row:
                    if column == 0:
                        sudoku_table_row.append(randint(1, 9))
                    else:
                        sudoku_table_row.append(0)
                sudoku_table.append(sudoku_table_row)
            population.append(sudoku_table)
        return population

    #تابع شایستگی کروموزوم ها که بر اساس تعداد اعداد اشتباه در جدول سودوکو است
    def merit_function(self, init_data, population):
        merits = []
        for table in population:
            mistake_count = 0
            for i in range(9):
                for j in range(9):
                    flag = False
                    if (table[i][j] == 0):
                        pass
                    else:
                        number = table[i][j]
                        for column in range(9):
                            if ((init_data[i][column] == number or table[i][column] == number) and column != j):
                                mistake_count += 1
                                flag = True
                                break
                        if (flag == False):
                            for row in range(9):
                                if ((init_data[row][j] == number or table[row][j] == number) and row != i):
                                    mistake_count += 1
                                    flag = True
                                    break
                        if (flag == False):
                            start_row = 3 * (i // 3)
                            start_column = 3 * (j // 3)
                            for row in range(start_row, start_row + 3):
                                for column in range(start_column, start_column + 3):
                                    if ((init_data[row][column] == number or table[row][column] == number) and row != i):
                                        mistake_count += 1
                                        flag = True
                                        break
            merits.append(mistake_count)
        return merits

    #تابع تولید فرزند از والدین
    def reproduce(self, x, y):
        child = []
        for i in range(9):
            child_row = []
            for j in range(9):
                turn = randint(0, 1)
                if(turn == 0):
                    child_row.append(x[i][j])
                else:
                    child_row.append(y[i][j])
            child.append(child_row)
        return child

    #تابع جهش
    def MUTATE(self, data, table):
        zero_count = self.zero_count(data)
        alpha = randint(1, 2*zero_count)
        flag = alpha
        array = [0,1]
        choice = random.choices(array, weights=[80, 20], k=1)
        if(choice[0] == 1):
            while(alpha != 0):
                row = randint(0,8)
                column = randint(0,8)
                if(table[row][column] == 0):
                    continue
                else:
                    table[row][column] = randint(1, 9)
                    alpha -= 1
            return table
        else:
            return table

    #انتخاب دو اندیس از جمعیت برای آمیزش
    def make_two_chice_from_population(self, data, population):
        zero_count = self.zero_count(data)
        merits = self.merit_function(data, population)
        merits = list(map(lambda x: (100 * zero_count) - (100 * x) + 1, merits))
        indices = []
        count = len(population)
        for i in range(count):
            indices.append(i)
        x_index = random.choices(indices, weights=merits, k=1)
        indices2 = copy.deepcopy(indices)
        del indices2[(x_index[0])]
        merits2 = copy.deepcopy(merits)
        del merits2[x_index[0]]
        y_index = random.choices(indices2, weights=merits2, k=1)
        return x_index, y_index

    def goal_test(self, init_data, chart):
        if((self.merit_function(init_data, [chart]))[0] == 0):
            return True
        else:
            return False

    def show(self, init_data, table):
        for row in range(9):
            line = ""
            for column in range(9):
                if(init_data[row][column] == 0):
                    line = line + str(table[row][column]) + "  "
                else:
                    line = line + str(init_data[row][column]) + "  "
            print(line)

    #تعداد خانه های خالی حدول سودوکو
    def zero_count(self, data):
        number = 0
        for row in range(9):
            for column in range(9):
                if (data[row][column] == 0):
                    number += 1
        return number
