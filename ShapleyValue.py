import itertools
import numpy as np
import math

participant = {
    'P1':
        {
        'X1': 3,
        'X2': 5,
        'X3': 8
        },
    'P2':
        {
        'X1': 6,
        'X2': 4,
        'X3': 5
        },
    'P3':
        {
        'X1': 7,
        'X2': 1,
        'X3': 3
        },
    'P4':
        {
        'X1': 8,
        'X2': 2,
        'X3': 4
        },
    }

np.random.seed(42)

def form_all_subsets(all_members_sets):
    '''Form all the subsets of the whole coalation'''

    subsets = set()

    for i in range(0, len(all_members_sets)):
        for coa in itertools.combinations(all_members_sets, i):
            subsets.add(coa)
    return subsets

def test_form():
    '''Test the function that produces all subsets of a coalation'''
    all_members_sets = set()
    for i in range(4):
        all_members_sets.add(i)
    print(all_members_sets)
    subsets = form_all_subsets(all_members_sets)
    print(subsets)


class ValueFunction():

    def __init__(self, input_):

        self.input_ = input_
        self.all_members_subsets = set()
        self.all_members_sets = set(input_.keys())
        self.score = dict()
        self.initial()

    def initial(self):
        '''Initialization'''
        self.form_subsets()

    def store_input(self, input_):
        '''Store the input'''
        self.all_members_sets = set(input_.keys())
        self.input_ = input_

    def form_subsets(self):
        '''Form all the subsets of the whole coalation'''
        self.all_members_subsets = form_all_subsets(self.all_members_sets)
        self.all_members_subsets.add(('P2', 'P3', 'P1', 'P4'))

    def extract(self):
        '''Extract the value of each participant'''
        input2 = {}
        for member_subset in self.all_members_subsets:
            values = []
            for member in self.all_members_sets:
                if member in member_subset:
                    values.append(list(self.input_[str(member)].values()))
            if len(values) > 0:
                values = np.reshape(values, (len(member_subset), len(list(self.input_[str(member)]))))
            # print(values)
            input2[member_subset] = values
        # print('***************')
        W = np.random.randint(1, 9, (len(list(self.input_[str(member)])), 1))
        # print(W)
        # print('***************')
        # print(input2)
        return input2, W

    def forward(self):
        '''Calculate the value function'''
        scores = []
        final_output = {}
        input2, W = self.extract()
        W = np.array(W)
        for values in input2.values():
            values = np.array(values)
            if values != np.array([]):
                output = np.sum(np.dot(values, W))
            else:
                output = 0
            scores.append(output)
        for member_subset, score in zip(self.all_members_subsets, scores):
            final_output[member_subset] = score

        return final_output

    def calculate_shapley_values(self):
        '''the function is used to calculate shapley valeus'''
        scores = self.forward()
        scores2 = {}
        # print(scores)
        for score, value in scores.items():
            score2 = tuple(sorted(score))
            scores2[score2] = value
        # print(scores2)
        n = len(self.all_members_sets)
        shapley_dict = {}
        for member in self.all_members_sets:
            participant_shapley = 0
            for member_subset in self.all_members_subsets:
                if member in member_subset:
                    # v(B U {j})
                    score_set = scores[member_subset]
                    # B
                    difference_set = set(member_subset).difference({member})
                    # v(B)
                    score_difference = scores2[tuple(sorted(difference_set))]
                    # v(B U {j}) - v(B)
                    difference = score_set - score_difference
                    S = len(difference_set)
                    factor = (math.factorial(n-S-1)*math.factorial(S)) / math.factorial(n)
                    factor_difference = factor * difference
                    participant_shapley += factor_difference
            # add to dict
            shapley_dict[member] = participant_shapley
            shapley_sorted_list = sorted(shapley_dict.items())
        # print(shapley_dict)
        # for key, value in shapley_dict.items():
            # print('Member', key, 'Shapley value is ', value)
        return shapley_sorted_list

def test_value_function(input):
    '''Test the function that produces all subsets of a coalation'''
    V = ValueFunction(input)
    # print(V.input_)
    # print(V.all_members_sets)
    # print(V.all_members_subsets)
    # print(V.extract())
    # print(V.forward())
    V.calculate_shapley_values()

if __name__ == '__main__':
    v = ValueFunction(participant)
    shapley_list = v.calculate_shapley_values()
    print(shapley_list)