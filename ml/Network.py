import numpy as np
from Layer import Layer


class Network(object):
    def __init__(self, layer_num, layer_nodes_num, eta, momentum, weights_list):
        '''
        weights_list: 权值列表，二维list。依次从左到右，从上到下
        '''
        self.layer_num = layer_num
        self.eta = eta
        self.momentum = momentum
        self.layer = []
        # 输入层
        self.layer.append(Layer('input_layer'))
        # 隐藏层
        weight_num = 0
        for i in range(1, layer_num - 1):
            sigmoid_num = layer_nodes_num[i]
            layer = Layer('hidden_layer', sigmoid_num,
                          weights_list[weight_num:weight_num + sigmoid_num])
            self.layer.append(layer)
            weight_num += sigmoid_num
        pass
        # 输出层
        sigmoid_num = layer_nodes_num[layer_num - 1]
        layer = Layer('output_layer', sigmoid_num,
                      weights_list[weight_num:weight_num + sigmoid_num])
        self.layer.append(layer)
        pass

    pass

    def train(self, input_date, correct_result):
        '''
        input_data: 为一个 numpy 的链表，表示一组输入值
        correct_result: 为正确值的链表，与input_data一一对应
        '''
        error_times = 0
        diff_val = 0
        for input_val, out_put in zip(input_date, correct_result):
            # 正向传播
            self.layer[0].layer_predict(input_val)
            for j in range(1, self.layer_num):
                # print('j = ' + str(j))
                self.layer[j].layer_predict(self.layer[j - 1].outputs)
            pass
            # 反向求delta
            # print('output' + str(out_put))
            self.layer[self.layer_num - 1].calc_delta(out_put)
            for j in range(2, self.layer_num):
                self.layer[self.layer_num -
                           j].calc_delta(self.layer[self.layer_num - j + 1])
            pass
            # 更新权值
            for j in range(1, self.layer_num):
                self.layer[j].update_weights(self.layer[j - 1].outputs,
                                             self.eta, self.momentum)
            pass
            predict_val = self.layer[self.layer_num - 1].outputs

            if not np.argmax(predict_val) == np.argmax(out_put):
                error_times += 1

            diff_val += np.sum(np.square(predict_val - out_put))
        pass
        return {'error_times': error_times, "diff_val": diff_val}

    def test(self, input_date, correct_result):
        '''
        input_data: 为一个 numpy 的链表，表示一组输入值
        correct_result: 为正确值的链表，与input_data一一对应
        '''
        error_times = 0
        diff_val = 0
        for input_val, out_put in zip(input_date, correct_result):
            self.layer[0].layer_predict(input_val)
            for j in range(1, self.layer_num):
                self.layer[j].layer_predict(self.layer[j - 1].outputs)
            pass
            predict_val = self.layer[self.layer_num - 1].outputs

            if not np.argmax(predict_val) == np.argmax(out_put):
                error_times += 1
            diff_val += np.sum(np.square(predict_val - out_put))
        pass
        return {'error_times': error_times, "diff_val": diff_val}