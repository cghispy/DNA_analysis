import os
import re

here = os.path.dirname(os.path.abspath(__file__))
files = []
for file in os.listdir(here):
    if file.endswith(".gbk"):
        files.append(file)



def searchFile(lines, gene):

    #search for gene
    complement = False
    endLine = len(lines)
    pattern = 'gene="'+gene+'"'
    for i in range (0, endLine):
        if (re.search(pattern, lines[i]) != None):

            # gene found
            found = True

            # check for complement
            complement = (re.search('complement', lines[i-1]) != None)

            # get sequence boudaries
            pattern = r'(\d+)\.\.(\d+)'
            match = re.search(pattern, lines[i-1])
            
            if match != None:
                lower = match.group(1)
                upper = match.group(2)
                for j in range (i, endLine):
                    match = re.search(r'/product="([^"]+)"', lines[j])
                    if (match!= None):
                        product = match.group(1)
                        return (found, lower, upper, complement, i, product)
                return (found, lower, upper, complement, i, '')  
    return (False, 0, 0, 0, 0, 0)

def getGeneSeq(fileLine, flag, lower, upper):

    # find start line
    startLine = 1
    while startLine < lower and startLine+60 <= lower:
        startLine+=60
    
    lowBuffer = lower - startLine
    endLine = startLine

    
    # find end line
    while endLine < upper and endLine+60 < upper:
        endLine+= 60
    uppBuffer = upper - endLine+1


    startLine = ' '+str(startLine)+' '
    endLine = ' '+str(endLine)+' '
     
    # find beginning 
    for i in range (fileLine, len(lines)):

        #search for the lower limit of the sequence
        if (re.search(startLine, lines[i]) != None):
            #lower limit found, copy cleaned up line
            
            fileLine = i # keep copy of line where beginning was found

            # Regular expression to match the letters while ignoring numbers and spaces
            match = re.search(r'\b\d+\s*([a-z]+(?:\s+[a-z]+)*)', lines[i])

            # Extract the letters if a match is found
            if match:
                sequence = match.group(1).replace(" ", "")[lowBuffer:]
                 
                # capitalize start codon when not complement (first letters)
                if not isComplement and not flag :
                    startCodon = sequence[0:3].upper()
                    sequence = startCodon + sequence[3:]
            break

    # middle to end
    for i in range (fileLine+1, len(lines)):
        
        
        if (re.search(endLine, lines[i],) == None):

            # before reaching end, cleanup and copy all lines to sequence
            match = re.search(r'\b\d+\s*([a-z]+(?:\s+[a-z]+)*)', lines[i])
            if match:
                sequence+= match.group(1).replace(" ", "")

        else :

            # last line
            match = re.search(r'\b\d+\s*([a-z]+(?:\s+[a-z]+)*)', lines[i])
            if match:
                sequence+= match.group(1).replace(" ", "")[0:uppBuffer]
            
            # capitalize start codon if complement (last letters)
            if isComplement and not flag:
                startCodon = sequence[-3:].upper()
                sequence+= sequence[:-3]+startCodon
            break
    return sequence

def complementSeq(sequence):
    seqList = list(sequence)
    for i in range (0, len(seqList)):
        if seqList[i] == 'a':
            seqList[i] = "t"
        elif seqList[i] == 't':
            seqList[i] = "a"
        elif seqList[i] == 'g':
            seqList[i] = "c"
        elif seqList[i] == 'c':
            seqList[i] = "g"
        elif seqList[i] == 'A':
            seqList[i] = "T"
        elif seqList[i] == 'T':
            seqList[i] = "A"
        elif seqList[i] == 'G':
            seqList[i] = "C"
        elif seqList[i] == 'C':
            seqList[i] = "G"
    sequence = ''.join(seqList)
    return sequence

def reverseSeq(sequence):
    seqList = list(sequence)
    
    sequence = ''.join(reversed(seqList))
    return sequence    



def main(lower, upper):

    lower = int(lower) 
    upper = int(upper)
    flag = False
    
    # get gene sequence from boudaries
    sequence = getGeneSeq(fileLine, flag, lower, upper)
    flag = True


    # change boundaries to get 100 bases pre- start codon
    if isComplement:
        lower = upper + 1
        upper = upper + 100 
        sequence = sequence + getGeneSeq(fileLine, flag, lower, upper)
    else:
        upper = lower -1
        lower = lower - 100
        sequence = getGeneSeq(fileLine, flag, lower, upper) + sequence 

    
    # if is complement, complement and reverse sequence
    if isComplement:
        sequence = complementSeq(sequence)
        sequence = reverseSeq(sequence)
    

    return sequence




gene = input("Input gene name (case sensitive): ")
while (gene != 'exit'):


    filesSearched = 0
    fileNum = len(files)
    sequence = ''
    product = ''
    for file in files:

        percentage = int((filesSearched/fileNum)*100)
        print(str(percentage)+"% "  + '\t|\tFiles searched: ' + str(filesSearched)+'/'+str(fileNum), end="\r")
        filesSearched+=1
        TXT = gene + ".txt"
        found = False
        nameFlag = False

        #open file
        file = os.path.join(here, file) 
        GBK = open(file, 'r')
        lines = GBK.readlines() 

        # search file
        found, lower, upper, isComplement, fileLine, product= searchFile(lines, gene)
    
        
        if found:
            # gene found, open file to write in
            f = open(TXT ,"a")
            f.write('>'+ os.path.basename(file).split('/')[-1]+ '-' + product+ '\n')

            # get sequence
            sequence = main(lower, upper)

            f.write(sequence+'\n'+'\n')
            f.close()


        
        else:
            variations = 1
            found = True
            while (found):
                nextGene = str(f"{gene}_{variations}")
                found, lower, upper, isComplement, fileLine , product= searchFile(lines, nextGene)
                if found:
                    # gene found, open file to write in
                    f = open(TXT ,"a")
                    f.write('>'+os.path.basename(file).split('/')[-1]+'_'+str(variations)+'-'+product+'\n')

                    # get sequence
                    sequence = main(lower, upper)
                    
                    f.write(sequence+'\n'+'\n')
                    f.close()
                variations = variations+1
        
    gene = input("Enter 'exit' to exit program OR input another gene name (case sensitive) : ")

    


