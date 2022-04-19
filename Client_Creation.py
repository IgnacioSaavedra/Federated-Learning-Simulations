#Create 30 clients, one for each subject
import os
import shutil

original = 'Clients/client.py'

#Create folder clients if it has not yet been created
if (not os.path. isdir(r'Clients')):
    os. mkdir(r'Clients')



for i in range(30):
    target = 'Clients/client'+str(i+1)+'.txt'
    #the reader won't take a .py file, so a .txt copy is created
    shutil.copyfile(original, target)
    target2='Clients/client'+str(i+1)+'.py'
    
    with open(target, 'r+') as f:
        with open(target2, 'w') as g:
            lines = f.readlines()
            for line in lines:
                if line.startswith('    subject_number='):
                    g.write(line.replace(line,"    subject_number="+str(i+1)+"\n"))
                elif line.startswith('    data_file="integrated data/readied data subject'):
                    g.write(line.replace(line,'    data_file="integrated data/readied data subject '+str(i+1)+'.csv"'+"\n"))                    
                else:
                    g.write(line)  

                
