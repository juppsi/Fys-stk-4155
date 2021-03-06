from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np 
from random import random, seed
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, LinearRegression, Lasso
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split, KFold
from sklearn.utils import resample
from numpy.random import randint, randn
from sklearn.pipeline import make_pipeline
from random import randrange
from sklearn.metrics import r2_score


def FrankeFunction(x,y):
	term1 = 0.75*np.exp(-(0.25*(9*x-2)**(2)) - 0.5*((9*y-2)**(2)))
	term2 = 0.75*np.exp(-((9*x+1)**(2))/49.0 - 0.1*(9*y+1))
	term3 = 0.5*np.exp(-(9*x-7)**(2) - (9*y-7)**(2))
	term4 = -0.2*np.exp(-(9*x-4)**(2) - (9*y-7)**(2))

	return term1+ term2+ term3+ term4


def Create_DesignMatrix(x,y,degree):
	n = x.shape[0]
	if degree ==1:
		x = np.c_[np.ones(n), x, y]


	elif degree == 2:
		x= np.c_[np.ones(n), x, y, x**2, x*y, y**2]

	elif degree == 3:
		x= np.c_[np.ones(n), x,y, x**2, x*y, y**2, x**3, x**2*y, x*y**2, y**3]

	elif degree == 4:
		x= np.c_[np.ones(n), x,y, x**2, x*y, y**2, x**3, x**2*y, x*y**2, y**3, x**4, x**3*y, x**2*y**2, x*y**3, y**4]

	elif degree == 5:
		x= np.c_[np.ones(n), x,y, x**2, x*y, y**2, x**3, x**2*y, x*y**2, y**3, x**4, x**3*y, x**2*y**2, x*y**3, y**4, \
		x**5, x**4*y, x**3*y**2, x**2*y**3, x*y**4, y**5]

	else:
		raise ValueError('Degree not less than 6! :{}'.format(degree))


	#print(x.shape)
	return x

def MSE(z_test, z_pred):
	mse = np.sum((z_test-z_pred)**2)/(np.size(z_pred))
	return mse


def R2(z_test, z_pred):
	R2 = 1 - np.sum((z_test-z_pred) ** 2) / np.sum((z_test - np.mean(z_pred)) ** 2)
	return R2

"""
def ConfidenceInterval(x):
	sigma = np.std(x)/np.sqrt(len(x))
	high = np.mean(x) + 1.96*(sigma)
	low = np.mean(x) - 1.96*(sigma)
	return np.mean(x), low, high
"""
def ConfidenceInterval(beta):
	#sigma = np.var(beta)
	sigma =np.sqrt(np.diag(np.linalg.inv(X.T @ X)))

	betahigh = beta + 1.96*(sigma)
	betalow = beta - 1.96*(sigma)

	diff = betahigh - betalow

	plt.scatter(range(len(beta)),beta)
	plt.errorbar(range(len(beta)), beta, yerr =np.array(diff),capsize=3, lw=1, fmt='r')
	plt.xlabel('$\\beta$ Range')
	plt.ylabel('$\\beta$')
	plt.legend(['Beta', 'Confidence Interval'])
	plt.title('Ridge regression with degree 5, noise 0.05, \n lambda 0.0001 and 100 datapoints')
	#plt.savefig('RidgeErrorbar0.0001.png')
	#for i in range(len(beta)):
		#plt.errorbar(i, y= beta[i], yerr= 1.96*sigma[i])
	plt.show()
	
	return betalow, betahigh

datapoints = 100
degree = 5


x = np.linspace(0,1,datapoints)
y = np.linspace(0,1,datapoints)


x,y  = np.meshgrid(x,y)
noise = 0.05*np.random.rand(len(x))
z= FrankeFunction(x,y) + noise


x= np.ravel(x)
y= np.ravel(y)
z = np.ravel(z)
X = Create_DesignMatrix(x, y, degree)

X_train, X_test, z_train, z_test = train_test_split(X, z, test_size = 0.2)

R_lambda = 0.0001

p = np.eye(X.shape[1])
beta_R = np.dot(np.dot(np.linalg.inv(np.dot(X.T,X) + R_lambda*p), X.T),z)	
z_predict_ridreg = X_test.dot(beta_R)
z_tilde = X_train @ beta_R

print('Training MSE: {}'.format(MSE(z_train, z_tilde)))
print('Test MSE: {}'.format(MSE(z_test, z_predict_ridreg)))

print('Training R2: {}'.format(R2(z_train, z_tilde)))
print('Test R2: {}'.format(R2(z_test, z_predict_ridreg)))

print('Training Variance: {}'.format(np.var(z_train)))
print('Test Variance: {}'.format(np.var(z_predict_ridreg)))

print('Confidence Interval: {}'.format(ConfidenceInterval(beta_R)))