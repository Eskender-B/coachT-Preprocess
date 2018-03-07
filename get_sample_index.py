import numpy as np
import pylab as plt
import sys
import os

dic = { 'forehand-standard':[], 
		'forehand-toohigh' :[],
		'forehand-toolow' : [],
		'backhand-standard': [],
		'backhand-toohigh' : [],
		'backhand-toolow' : []}


total = np.zeros((261,3))

for key in dic.keys():
	for i in range(40):
		try:
			data = np.loadtxt('sliced/'+key+'/swing'+str(i+1)+'.CSV', dtype=float, delimiter=',')
			total = np.add(total, abs(data))
			dic[key].append(data)
		except IOError:
			break


diff_data = abs(np.diff(total, axis=0))
diff_data = np.sum(diff_data, axis=1)
diff_indx = diff_data.argsort()[::-1][0:42]

diff_indx.sort()

# Print result
print diff_indx

