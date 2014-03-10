#parse Justin Vandenbroucke configure.py 


speed='fast'
findElse = False
writeFlag = True
indentFlag = True
cmdNum = 0
filename = open("/home/salvo/Scrivania/DEV-PROJ/Target/1-SOFTWARE/1-libtarget-code/tutorials/configure.py",'r')
filename2 =open("t5configfast.csv",'w')
filename2.write("SeqNum,Address,Value,Descr\n")


for line in filename:
    if not(line[0] == '#'):
        if ('board.WriteRegister' in line):
            writeFlag = True
        else: 
            writeFlag = False
 
        if (line[0] in (' ','\t')) and not(indentFlag):     #indent condition
            writeFlag = False

        if ('speed=="fast"' in line.replace("'",'"')):      #speed condition handling
            if(speed=='fast'):
                findElse = True
                indentFlag = True
            else:
                findElse = False
                indentFlag = False

        if ('else' in line) and findElse: #speed condition handling
            findElse = False
            indentFlag = False
        
 
        if writeFlag:
            cmdNum+=1
            filename2.write('{0},"{2}","{3}","{1}"\n'.format(cmdNum, line[line.find('#'):line.find("\n")].replace("'",'"'), *tuple(line[line.find('(')+1:line.find(')')].split(','))))
            print '{0},"{2}","{3}","{1}"\n'.format(cmdNum, line[line.find('#'):line.find("\n")].replace("'",'"'), *tuple(line[line.find('(')+1:line.find(')')].split(',')))
