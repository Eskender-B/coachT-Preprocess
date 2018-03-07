### slice.py is used to slice a CSV file containing swing records into single swings
### The slicing is done based on command line parameters threshold and width and finding the peak point 
### of ax among vector acceleration data of (ax, ay, az) specific for the direction setup used when
### collecting the data. 
### This is all experimental and not gaurentied to work always. So you need to see the final plot result
### and do the slicing again with different parameters until you are satisfied.
### 
### threshold:  minimum value above which maximum is detected
### width:      the value in number of points to the right and left of the maximum point marking
###		the begining and end of a single swing




import numpy as np
import pylab as plt
import sys
import os


if len(sys.argv) < 4:
	print("Usage: "+sys.argv[0] + " input_file threshold width")
	exit(1)

direc = 'sliced/'+ sys.argv[1].replace(".CSV", "") + '/'
threshold = float(sys.argv[2])
width = int(sys.argv[3])
os.system('rm -r ' + direc)
os.system('mkdir ' + direc)


data = np.loadtxt(sys.argv[1], dtype=float, delimiter=',')

cut = []
abs_ax = abs(data[:,0])
maxx = 0
indx = 0
thresh = False
for i in range(len(abs_ax)):
	if abs_ax[i] > threshold:
		thresh = True
	if abs_ax[i] > maxx and thresh:
		maxx = abs_ax[i]
		indx = i

	elif maxx!=0 and maxx - abs_ax[i] >= 0.95*maxx:
		cut.append(indx)
		maxx = 0
		indx = 0
		thresh = False



print len(cut)
print cut
print abs_ax[cut]

x = plt.linspace(1,len(data),len(data))	

for i in [1, 2, 3]:
	plt.subplot(3,1,i)
	plt.plot(x, data[:,i-1])
	for j in range(len(cut)):
		#plt.axvline(x=j, color='g')
		left = cut[j] - width
		right = cut[j] + width
		
		if left < 0:
			left = 0
		if right >= len(data):
			right = len(data) - 1
		
		plt.axvline(x=left, color='r')
		plt.axvline(x=right, color='r')
		#plt.axvline(x=cut[j], color='r')


		if i ==1:
			pass
			np.savetxt(direc + "swing"+str(j+1)+'.CSV',data[left:right+1,:], fmt='%.2f',delimiter=',')


plt.savefig(direc+sys.argv[1].replace(".CSV", ".jpg"))
plt.show()
