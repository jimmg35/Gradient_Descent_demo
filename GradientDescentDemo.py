
'''
    ***********************
    *   Notification!!!!  *
    ***********************

    function z = sin(sqrt(x^2 + y^2))
    derivative : ∂z/∂x = x(cos(sqrt(x^2 + y^2))) / sqrt(x^2 + y^2)
                 ∂z/∂y = y(cos(sqrt(x^2 + y^2))) / sqrt(x^2 + y^2)
    starting point : (5,5)
    learning rate : 0.001
'''

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
    

class Configuration():
    def __init__(self):
        self.X = 5
        self.Y = 5
        self.Z = self.Calculate_Z(self.X,self.Y)
        self.lr = 0.001
        self.slope_limit = 0.00000001 #close to 0 enough?

    def Calculate_Z(self,X,Y):
        Z = math.sin(math.sqrt(X ** 2 + Y ** 2))
        return Z
        
    def Derivative_X(self,X,Y):
        X_gradient = X * math.cos(math.sqrt(X ** 2 + Y ** 2)) / math.sqrt(X ** 2 + Y ** 2)
        return X_gradient

    def Derivative_Y(self,X,Y):
        Y_gradient = Y * math.cos(math.sqrt(X ** 2 + Y ** 2)) / math.sqrt(X ** 2 + Y ** 2)
        return Y_gradient

    def Graph_Z(self,np_X,np_Y):
        np_Z = np.sin(np.sqrt(np_X ** 2 + np_Y ** 2))
        return np_Z
        

class GradientDescend(Configuration):
    def Initialize(self):
        #record
        self.epoch = [0]
        self.X_vary_list = [self.X]
        self.Y_vary_list = [self.Y]
        self.Z_vary_list = [self.Z]
        self.Gradient_X_vary_list = [self.Derivative_X(self.X,self.Y)]
        self.Gradient_Y_vary_list = [self.Derivative_Y(self.X,self.Y)]
        
    def GetGradient(self):
        self.gradient = [self.Derivative_X(self.X,self.Y) , self.Derivative_Y(self.X,self.Y)] #based on the derivative of function  ##
        self.Gradient_X_vary_list.append(self.gradient[0])
        self.Gradient_Y_vary_list.append(self.gradient[1])
        
    def ApplyLearningRate(self):
        self.delta_X = self.gradient[0] * self.lr
        self.delta_Y = self.gradient[1] * self.lr

    def UpdateWeight(self):
        self.X -= self.delta_X
        self.Y -= self.delta_Y
        self.X_vary_list.append(self.X)
        self.Y_vary_list.append(self.Y)
        self.Z_vary_list.append(self.Calculate_Z(self.X,self.Y))

    def ReturnHistory(self):
        return self.epoch,self.X_vary_list,self.Y_vary_list,self.Z_vary_list,self.Gradient_X_vary_list,self.Gradient_Y_vary_list

    def Perform(self):
        i = 0
        while True:
            GD.GetGradient()
            GD.ApplyLearningRate()
            GD.UpdateWeight()
            i += 1
            self.epoch.append(i)
            if abs(self.gradient[0]) <= self.slope_limit and abs(self.gradient[1]) <= self.slope_limit:
                print('Gradient Descent Complete!')
                break
    
    def GenerateGraph(self,X_vary_list, Y_vary_list, Z_vary_list):
        fig = plt.figure()
        ax = plt.axes(projection="3d")

        x = np.linspace(0, 10, 100)
        y = np.linspace(0, 10, 100)

        X, Y = np.meshgrid(x, y)
        Z = self.Graph_Z(X, Y)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('surface')

        #函數圖形
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,alpha = 0.3,cmap='viridis', edgecolor='none')  

        #下降曲線
        ax.plot_wireframe(X_vary_list, Y_vary_list, Z_vary_list, color='red') 

        #等高2D圖
        fig = plt.figure()
        cm = plt.cm.get_cmap('viridis')
        plt.scatter(X, Y, c=Z, cmap=cm)

        cp = plt.contour(X, Y, Z, colors='black', linestyles='dashed', linewidths=1)
        plt.clabel(cp, inline=1, fontsize=10)
        cp = plt.contourf(X, Y, Z, )
        plt.xlabel('X')
        plt.ylabel('Y')

        #2D下降曲線
        plt.plot(X_vary_list, Y_vary_list,color = 'red')
        

        plt.show()
        
        #圖形動畫，取用前須把前一行刪除
        #for angle in range(0, 360):   
        #    ax.view_init(30, angle)
        #    plt.draw()
        #    plt.pause(0.00001)


                
if __name__ == '__main__':

    #從(5,5,?)開始下降，學習率0.001
    GD = GradientDescend()
    GD.Initialize()
    GD.Perform()

    #獲得下降紀錄包含X紀錄、Y紀錄、Z紀錄、X方向梯度紀錄、Y方向梯度紀錄
    epoch,X_vary_list,Y_vary_list,Z_vary_list,Gradient_X_vary_list,Gradient_Y_vary_list = GD.ReturnHistory()

    #轉型成matplotlib所需之numpy型別
    X_vary_list = np.array(X_vary_list)
    Y_vary_list = np.array(Y_vary_list)
    Z_vary_list = np.array([Z_vary_list])

    #產生圖片
    GD.GenerateGraph(X_vary_list, Y_vary_list, Z_vary_list)