import numpy as np
import h5py


inp = '''
*Title
 test

*Node
 1, 0, 0, 1
 2, 2, 1, 0

*Element, TYPE=Element
 1,2,1

*Step
 0.1
'''


nodes = [
  [1,3,1,0,0],
  [2,3,0,21],
  [3,1,2,1,3],
  [4,5,1,2,3,1,4]]

elms = [
        [1, 0,0, 10,0],
        [2, 10,0,12,1],
        [3, 1,2,3,-4,2,1]]

f = h5py.File('fem.h5','w')

sdtype = h5py.string_dtype(encoding='utf-8')
vdtype = h5py.vlen_dtype(np.dtype('float64'))

#inpGroup = f.create_group('/inp')
#inpGroup.create_dataset('inp',data=inp,dtype=sdtype)  # only one string : (1,) string

f.attrs['inp'] = inp

step1 = f.create_group('/Step1')         # /2/1
step1.attrs['TargetElement'] = 'Elset1, Elset2, Elset3'
step1.attrs['TargetLoad'] = 'LC1, LC2'
step1.attrs['TargetConstraint'] = 'C1, C2'
step1.attrs['FieldOutputs'] = 'D, SF'

dofs = np.zeros((len(nodes),2),dtype='int')
for i,n in enumerate(nodes):
    dofs[i,0] = n[0]
    dofs[i,1] = n[1]

step1.attrs['dofs'] = dofs

frame1 = step1.create_group('frame1')
frame1.attrs['time'] = 0.1


disp = frame1.create_dataset('D',shape=(4,),dtype=[("id",np.dtype('int')),("data",vdtype)])

for i, n in enumerate(nodes):
    disp[i] = (n[0],np.array(n[2:]))

sf = frame1.create_dataset('SF',shape=(3,),dtype=[("id",np.dtype('int')),("data",vdtype)])


for i, e in enumerate(elms):
    sf[i] = (e[0],np.array(e[1:]))

f.close()


f = h5py.File('fem.h5','r')
inputStream = f.attrs['inp']
print(inputStream)


f.close()