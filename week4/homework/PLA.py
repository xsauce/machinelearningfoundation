import functools
import random
import time

import numpy as np
class PLA():
    def __init__(self):
        pass

    def sign_func(self, val):
        if val > 0:
            return 1
        else:
            return -1

    def cal_mistake_count(self, w, x, y):
        map_sign_func = np.vectorize(self.sign_func)
        result = map_sign_func(np.dot(x, w)) - y
        return result[result != 0].size

    def pocket(self, x, y, init_w, update_iter_count=50):
        w = init_w
        error = self.cal_mistake_count(w, x, y)
        best_w = np.matrix.copy(w)
        n = x.shape[0]
        random.seed()
        for i in range(update_iter_count):
            index_list = random.sample(range(n), n)
            for j in index_list:
                if y[j] != self.sign_func(np.dot(x[j], w)):
                    w += (y[j] * x[j]).T
                    new_error = self.cal_mistake_count(w, x, y)
                    if new_error < error:
                        best_w = np.matrix.copy(w)
                        error = new_error
                    break
        return best_w, w

    def test_error_rate(self, w, test_x, test_y):
        return 1.0 * self.cal_mistake_count(w, test_x, test_y) / test_y.shape[0]


    def run(self, x, y, init_w, shuffle_func, step_size=1.0):
        '''
        :param x: m row n col
        :param y: m row 1 col
        :param init_w: n row 1 col
        :return: void
        '''
        iter_count = 0
        w = init_w
        while 1:
            finished = True
            iter_list = shuffle_func(list(range(x.shape[0])))
            for i in iter_list:
                if y[i] == self.sign_func(np.dot(x[i], w)):
                    continue
                else:
                    iter_count += 1
                    finished = False
                    w += (step_size * y[i] * x[i]).T
            if finished:
                break
        return w, iter_count

def read_data(file, test_count=None):
    x = []
    y = []
    count = 0
    with open(file) as f:
        for line in f.readlines():
            if test_count and count > test_count:
                break
            count += 1
            xyline = line.split("\t")
            rx = list(map(float, xyline[0].split(" ")))
            ry = int(xyline[1])
            x.append(rx + [1.0])
            y.append(ry)
    return np.mat(x), np.mat(y).T

def random_shuffle(lst):
    random.shuffle(lst)
    return lst

if __name__ == "__main__":
    pla = PLA()
    x, y = read_data("hw1_15_train.dat", test_count=None)
    w, iter_count = pla.run(x, y, np.zeros((x.shape[1], 1)), lambda x: x)
    print("native loop:", iter_count)
    # native loop: 45

    print("random_loop start")
    iter_count_list = []
    for i in range(2000):
        w, iter_count = pla.run(x, y, np.zeros((x.shape[1], 1)), random_shuffle)
        iter_count_list.append(iter_count)
    print("avg iter count:", sum(iter_count_list) * 1.0 / len(iter_count_list))

    print("random_loop start with step size", 0.5)

    #random loop avg iter count: 39.7445

    iter_count_list = []
    for i in range(2000):
        w, iter_count = pla.run(x, y, np.zeros((x.shape[1], 1)), random_shuffle, step_size=0.5)
        iter_count_list.append(iter_count)
    print("avg iter count:", sum(iter_count_list) * 1.0 / len(iter_count_list))

    # random_loop with step size 0.5, avg iter count: 40.114

    px, py = read_data("hw1_18_train.dat")
    print(px.shape, py.shape)
    px_test, py_test = read_data("hw1_18_test.dat")
    print(px_test.shape, py_test.shape)
    print("pocket start")
    pocket_error_rate_list = []
    normal_error_rate_list = []
    for i in range(2000):
        print(i)
        best_w, w = pla.pocket(px, py, np.zeros((px.shape[1], 1)), update_iter_count=100)
        pocket_error_rate = pla.test_error_rate(best_w, px_test, py_test)
        normal_error_rate = pla.test_error_rate(w, px_test, py_test)
        pocket_error_rate_list.append(pocket_error_rate)
        normal_error_rate_list.append(normal_error_rate)
    print("pocket avg error rate:", sum(pocket_error_rate_list) * 1.0 / len(pocket_error_rate_list))
    print("normal avg error rate:", sum(normal_error_rate_list) * 1.0 / len(normal_error_rate_list))

    # pocket avg error rate: 0.1325239999999994
    # normal avg error rate: 0.355488

    # pocket avg error rate: 0.11568700000000022
    # normal avg error rate: 0.32767400000000013