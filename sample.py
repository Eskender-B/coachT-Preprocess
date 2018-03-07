import numpy as np
import pylab as plt
import sys
import os

if len(sys.argv) < 1:
	print("Usage: "+sys.argv[0] + "width (exact param used when slicing)")
	exit(1)

width = int(sys.argv[1]) 

os.system('rm -r sampled; mkdir sampled; mkdir sampled/data')
os.system('mkdir sampled/data/train; mkdir sampled/data/test')

os.system('mkdir sampled/figure')
os.system('mkdir sampled/figure/train; mkdir sampled/figure/test')



dic_train = { 'forehand-standard':[], 
		'forehand-toohigh' :[],
		'forehand-toolow' : [],
		'backhand-standard': [],
		'backhand-toohigh' : [],
		'backhand-toolow' : []}


dic_test = { 'forehand-standard':[], 
		'forehand-toohigh' :[],
		'forehand-toolow' : [],
		'backhand-standard': [],
		'backhand-toohigh' : [],
		'backhand-toolow' : []}



total = np.zeros((2*width+1,3))
for name in['train', 'test']:
	for key in eval('dic_'+name).keys():
		files = os.listdir('sliced/data/'+name+'/'+key) 
		for file in files:
			if file.endswith('.CSV'):
				data = np.loadtxt('sliced/data/'+name+'/'+key+'/'+file, dtype=float, delimiter=',')
				if name == 'train':
					total = np.add(total, abs(data))
					dic_train[key].append(data)
				elif name == 'test':
					dic_test[key].append(data)
		


diff_data = abs(np.diff(total, axis=0))
diff_data = np.sum(diff_data, axis=1)
diff_indx = diff_data.argsort()[::-1][0:42]


for name in ['train', 'test']:
	for key in eval('dic_'+name).keys():
		os.system('mkdir sampled/data/'+name+'/'+key)
		os.system('mkdir sampled/figure/'+name+'/'+key)
		for i in range(len(eval('dic_'+name)[key])):

			data = eval('dic_'+name)[key][i]
			x = plt.linspace(1,len(data),len(data))
			
			plt.subplot(3,1,1)
			plt.plot(x, data[:,0])
			plt.plot(diff_indx, data[:,0][diff_indx], 'r+')

			plt.subplot(3,1,2)
			plt.plot(x, data[:,1])
			plt.plot(diff_indx, data[:,1][diff_indx], 'r+')

			plt.subplot(3,1,3)
			plt.plot(x, data[:,2])
			plt.plot(diff_indx, data[:,2][diff_indx], 'r+')



			plt.savefig('sampled/figure/'+name+'/'+ key +'/swing'+str(i+1)+'.jpg')
			plt.close()

			np.savetxt('sampled/data/'+name+'/'+ key +'/swing'+str(i+1)+'.CSV',data[diff_indx], fmt='%.2f', delimiter=',')
