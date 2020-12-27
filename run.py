# By Navid Hasanzadeh 9323701
import matplotlib.pyplot as plt
from id3 import id3
import pylab 

print('::Decision Tree Python Code By Navid Hasanzadeh::')
a = id3()
#Learn
print('Learning:')
a.learn(file='noisy_train.ssv')
beforePruneErrTrain = a.getError(a.predict(file='noisy_train.ssv'))
beforePruneErrTest = a.getError(a.predict(file='noisy_test.ssv'))

#Prune
print('Pruning:')
tree = a.treePrune(file='noisy_valid.ssv',testFile='noisy_test.ssv', trainFile = 'noisy_train.ssv')
errs = a.pruneTestErrors()

print('Non-pruned tree train error = ', beforePruneErrTrain )
print('Non-pruned tree test error = ', beforePruneErrTest )
print('Pruned tree test error = ', a.getError(a.predict(file='noisy_test.ssv')))
#Errors Plot
plt.figure(num=None, figsize=(8, 6), dpi=175, facecolor='w', edgecolor='k')
trainErr=[100 * x for x in errs[0:len(errs):3]]
testErr=[100 * x for x in errs[1:len(errs):3]]
validErr=[100 * x for x in errs[2:len(errs):3]]
steps = np.arange(0, len(trainErr))
plt.plot(steps,trainErr , 'r--', label='Train')
plt.plot(steps, testErr, 'bo', label='Test')
plt.plot(steps, validErr, 'g^', label='Validation')
pylab.legend(loc='upper right')
plt.xlabel('Number of Pruned Nodes', fontsize=16)
plt.ylabel('Error %', fontsize=16)
plt.title('Decision Tree - Errors', fontsize=20,fontweight="bold")
plt.grid(True)

plt.show()
