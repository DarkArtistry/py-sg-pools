from itertools import combinations, permutations
from copy import deepcopy
import random
import numpy as np
import pandas as pd

class PyToto:
    def __init__(self):
        self.toto_numbers = [i+1 for i in range(49)]
        self.current_board = []
        self.gambling_slip = []
        self.budget = 0
        pass

    def pretty_print_toto_numbers(self, in_toto_numbers):
        """
        pretty_print_toto_numbers prints the toto board
        """
        existing_numbers = deepcopy(self.toto_numbers)
        row_1 = np.arange(1, 10)
        row_2 = np.arange(10, 19)
        row_3 = np.arange(19, 28)
        row_4 = np.arange(28, 37)
        row_5 = np.arange(37, 46)
        row_6 = np.array([46,47,48,49, 0, 0, 0, 0, 0])
        np_arr = np.array([
            row_1,
            row_2,
            row_3,
            row_4,
            row_5,
            row_6
        ])
        rows = np_arr.shape[0]
        cols = np_arr.shape[1]
        if in_toto_numbers:
            for x in range(0, rows):
                for y in range(0, cols):
                    if np_arr[x][y] not in existing_numbers:
                        np_arr[x][y] = 0
        print(np_arr)
    
    def self_pick_number(self, in_toto_numbers):
        print()
        self.pretty_print_toto_numbers(in_toto_numbers)
        number = input("Pick a number: ")
        number = int(number)
        if number not in self.toto_numbers and in_toto_numbers:
            print("number is already picked!")
            number = input("Pick a number: ")
            number = int(number)

        number_index = self.toto_numbers.index(number)
        self.toto_numbers.pop(number_index)
        return number

    def self_pick_board(self, count, in_toto_numbers):
        temp_board = []

        while len(temp_board) < count:
            number_picked = self.self_pick_number(in_toto_numbers)
            if number_picked not in temp_board:
                temp_board.append(number_picked)

        print("current_board ({}): \n {}".format(len(temp_board), temp_board))
        self.current_board = temp_board
        pass

    def random_board(self, count, in_toto_numbers):
        temp_board = []
        numbers_to_pick_from = None

        if in_toto_numbers:
            numbers_to_pick_from = self.toto_numbers
        else:
            numbers_to_pick_from = [i+1 for i in range(49)]

        while len(temp_board) < count:
            temp_number = random.choice(numbers_to_pick_from)
            if temp_number not in temp_board:
                temp_board.append(temp_number)

        for number in temp_board:
            if number in self.toto_numbers:
                number_index = self.toto_numbers.index(number)
                self.toto_numbers.pop(number_index)

        print('randomnized board ({}): {}'.format(len(temp_board), temp_board))
        self.current_board = temp_board
        pass

    def play(self):
        types_and_costs = np.array([
            ['','QuickPick', 'System-Roll', 'System-7', 'System-8', 'System-9', 'System-10', 'System-11', 'System-12'],
            ['Combinations', 1, 44, 7, 28, 84, 210, 462, 924],
            ['Cost', '$1', '$44', "$7", "$28", "$84", "$210", "$462", "$924"],
        ])
        budget = input("What's your budget? (integer): ")
        self.budget = int(budget)
        while self.budget > 0:
            print("Types and Costs:")
            df = pd.DataFrame(types_and_costs)
            print(df)
            print()
            print("sysmtem-roll is unavailable")
            print()
            types_arr = ['quickpick', 'system-7', 'system-8', 'system-9', 'system-10', 'system-11', 'system-12']
            buy_type = input("What do you want to buy?: ")
            buy_type = buy_type.lower()
            while buy_type not in types_arr:
                print()
                print("Invalid type!")
                buy_type = input("What do you want to buy?: ")
                buy_type = buy_type.lower()
            
            count = 7 if buy_type == 'system-7' else 8 if buy_type == 'system-8' else 9 if buy_type == 'system-9' else 10 if buy_type == 'system-10' else 11 if buy_type == 'system-11' else 12 if buy_type == 'system-12' else 6
            cost = 7 if buy_type == 'system-7' else 28 if buy_type == 'system-8' else 84 if buy_type == 'system-9' else 210 if buy_type == 'system-10' else 462 if buy_type == 'system-11' else 924 if buy_type == 'system-12' else 1

            choice = ["random", "self-pick"]
            print()
            random_choice = input("random or self-pick?: ")
            if random_choice not in choice:
                print()
                print("Invalid choice!")
                random_choice = input("random or self-pick?: ")

            self.pretty_print_toto_numbers(True)
            print()
            in_toto_numbers = input("pick only from unpicked numbers? True/False: ")
            if in_toto_numbers == "True":
                in_toto_numbers = True
            else:
                in_toto_numbers = False
            
            if random_choice == "random":
                self.random_board(count, in_toto_numbers)
            else: 
                self.self_pick_board(count, in_toto_numbers)

            self.budget = self.budget - cost
            self.gambling_slip.append(self.current_board)
            print("Amount left: {}".format(self.budget))
            print()
        print()
        print("Your bets are:")
        for board in self.gambling_slip:
            print(board)

