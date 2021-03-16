import os
import pickle
import numpy as np
from tqdm import tqdm
from tensorflow.nn import softmax


class Tester:
    def __init__(self,
                 model,
                 data,
                 batch_size,
                 log_path,
                 ):
        self.data = data
        self.batch_size = batch_size
        self.model = model
        self.log_path = log_path

    def run(self):
        n_items = len(self.data.test_data[0])
        n_batches = int(np.ceil(n_items / self.batch_size))
        outcome = {'ID': np.empty(0),
                   'class': np.empty(0),
                   'y': np.empty(0),
                   "y_hat": np.empty(0)}
        for batch in tqdm(range(n_batches)):
            batch_data = next(self.data.next_batch_test_all(self.batch_size, batch))
            # expand data
            inputs = batch_data[:8]
            y_hat = softmax(self.model(inputs))
            outcome['ID'] = np.concatenate((outcome['ID'], batch_data[10]))
            outcome['class'] = np.concatenate((outcome['class'], batch_data[9]))
            outcome['y'] = np.concatenate((outcome['y'], batch_data[8].numpy()))
            outcome['y_hat'] = np.concatenate((outcome['y_hat'],
                                               y_hat.numpy()[:, 1]))
        with open(self.log_path, 'wb') as f:
            pickle.dump(outcome, f)
