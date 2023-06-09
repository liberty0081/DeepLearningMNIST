# -*- coding: utf-8 -*-
"""NeuralNetworkOptimizerGPU.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18mWQWya7zrxiyWfR_jk71pkfSs8zu3G6
"""

import cupy as np

class SDG():
    def __init__(self, lr = 0.01):
        self.lr = lr

    def learning(self, W, dW, b, db):
        W -= dW*self.lr
        b -= db*self.lr

class Momentum():
    def __init__(self, lr = 0.01, rv = None):
        self.lr = lr
        self.v1 = None
        self.v2 = None 

        if rv is None:
            self.rv = 0.9
        
        elif not rv is None:
            self.rv = rv

    def learning(self, W, dW, b, db):
        if self.v1 is None:
            self.v1 = np.zeros_like(dW)

        if self.v2 is None:
            self.v2 = np.zeros_like(db)

        self.v1 = self.rv*self.v1 - self.lr*dW
        self.v2 = self.rv*self.v2 - self.lr*db
        W      += self.v1
        b      += self.v2

class AdaGrad():
    def __init__(self, lr = 0.01):
        self.lr = lr
        self.h1 = None
        self.h2 = None

    def learning(self, W, dW, b, db):
        if self.h1 is None:
            self.h1 = np.zeros_like(dW)

        if self.h2 is None:
            self.h2 = np.zeros_like(db)

        self.h1 = self.h1 + dW*dW
        self.h2 = self.h2 + db*db
        W      -= self.lr*dW/(np.sqrt(self.h1) + 1e-8)
        b      -= self.lr*db/(np.sqrt(self.h2) + 1e-8)

class Adam():
    def __init__(self, lr = 0.01, beta1 = None, beta2 = None):
        self.lr    = lr
        self.m1    = None
        self.m2    = None
        self.v1    = None
        self.v2    = None
        self.t     = 0

        if beta1 is None:
            self.beta1 = 0.9

        if beta2 is None:
            self.beta2 = 0.99

        elif not beta1 is None:
            self.beta1 = beta1

        elif not beta2 is None:
            self.beta2 = beta2

    def learning(self, W, dW, b, db):
        if self.m1 is None:
            self.m1 = np.zeros_like(dW)
        
        if self.v1 is None :
            self.v1 = np.zeros_like(dW)

        if self.m2 is None:
            self.m2 = np.zeros_like(db)

        if self.v2 is None:
            self.v2 = np.zeros_like(db)

        self.t  += 1
        iter     = self.lr*np.sqrt(1.0 - self.beta2**self.t)/(1.0 - self.beta1**self.t)
        self.m1 += (1.0 - self.beta1)*(dW - self.m1)
        self.v1 += (1.0 - self.beta2)*(dW**2 - self.v1)
        self.m2 += (1.0 - self.beta1)*(db - self.m2)
        self.v2 += (1.0 - self.beta2)*(db**2 - self.v2)

        W       -= iter*self.m1/(np.sqrt(self.v1) + 1e-7)
        b       -= iter*self.m2/(np.sqrt(self.v2) + 1e-7)