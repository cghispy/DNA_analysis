import re
import os
import csv


#find files
here = os.path.dirname(os.path.abspath(__file__))
files = []
for file in os.listdir(here):
    if file.endswith(".gbk"):
        files.append(file)

genes = []





def findBackGenes(depth, LineNum, lines):

    pattern = r'/gene="([^"]+)"'
    product=''
    fieldNum = 0
    geneAdded = False
    for i in range (LineNum, -1, -1):
        if depth < 0 :
            fillListBack(fieldNum)
            break
        elif re.search('ORIGIN', lines[i]) != None:
            break
        if re.search(r'/product="([^"]+)"', lines[i]) != None:
            product = re.search(r'/product="([^"]+)"', lines[i]).group(1)
        match = re.search(pattern, lines[i])
        if (match != None):
            gene_value = match.group(1)
            genes.insert(0, [(fieldNum), gene_value])
            fieldNum = fieldNum-1
            depth = depth-1
            geneAdded = True
        elif (re.search('CDS', lines[i]) != None) and geneAdded == False:
            genes.insert(0,[(fieldNum), product])
            depth -= 1
            fieldNum -= 1
        elif (re.search('CDS', lines[i]) != None) and geneAdded == True:
            geneAdded = False




def findforwardGenes(depth, LineNum, LinesLen, lines):
    pattern = r'/gene="([^"]+)"'
    fieldNum = 1
    product = ''
    geneAdded = False
    for i in range (LineNum+1, LinesLen):
        if (re.search('CDS', lines[i]) != None):
            LineNum = i
            break
    for i in range (LineNum+1, LinesLen):
        if depth <= 0 :
            fillListFront(fieldNum)
            break
        elif re.search('ORIGIN', lines[i]) != None:
            break
        if re.search(r'/product="([^"]+)"', lines[i]) != None:
            product = re.search(r'/product="([^"]+)"', lines[i]).group(1)
        match = re.search(pattern, lines[i])
        if (match != None):
            gene_value = match.group(1)
            genes.append([(fieldNum), gene_value])
            fieldNum = fieldNum+1
            depth = depth-1
            geneAdded = True
        elif (re.search('CDS', lines[i]) != None) and geneAdded == False:
            genes.append([(fieldNum), product])
            depth -= 1
            fieldNum += 1
        elif (re.search('CDS', lines[i]) != None) and geneAdded == True:
            geneAdded = False
            product =''


def fillListBack(fieldNum):
        for i in range (fieldNum, -11, -1):
            genes.insert(0,[(i), None])
def fillListFront(fieldNum):
        for i in range (fieldNum, 11):
            genes.append([(i), None])    



def writeToCSV(genes, CSV):    
    fields = ['filename'] + list(range(-depth, depth+1))

    # Initialize the dictionary with all fieldnames and set their default value to None
    gene_dict = {field: None for field in fields}

    for key, value in genes:
        if key == 'filename':
            gene_dict['filename'] = value
        else:
            position = int(key)
            if position in gene_dict:
                gene_dict[position] = value

    file_exists = os.path.isfile(CSV)

    with open(CSV, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(gene_dict)



def searchFile(filename, gene):

    #open file
    file = os.path.join(here, filename) 
    GBK = open(file, 'r')
    lines = GBK.readlines() 

    
    #search for gene
    complement = False

    for i in range (0, len(lines)):
        pattern = 'gene="'+gene+'"'
        found = False
        if (re.search(pattern, lines[i]) != None):
            # check for complement
            complement = (re.search('complement', lines[i-1]) != None)

            # gene found, find genes before & after
            findBackGenes(depth, i, lines)
            findforwardGenes(depth, i, len(lines), lines)
            found = True

            if complement:
                for i in range (0, len(genes)):
                    genes[i][0]= genes[i][0]*-1

            genes.insert(0,('filename',filename))
            return (found,genes)
    return found, genes


'''///////////////////*main*/////////////////'''

#take input
gene = input("Input gene name (case sensitive): ")
while (gene != 'exit'):

    depth = -1
    while (depth<0):
        depth = int(input("Input search depth (>1): "))
    instances = 0
    filesSearched = 0
    fileNum = len(files)

    #create CSV
    CSV = gene + ".csv"

    #delete it ifit exists already
    file_exists = os.path.isfile(CSV)
    if file_exists:
        os.remove(CSV)

    #main loop
    for file in files:
        percentage = int((filesSearched/fileNum)*100)
        print(str(percentage)+"% " +"\t|\t"+ "Instances found: "+str(instances) + '\t|\tFiles searched: ' + str(filesSearched)+'/'+str(fileNum), end="\r")
        filesSearched+=1

        found = False
        (found, genesFound) = searchFile(file, gene)
        if found:
            writeToCSV(genesFound, CSV)
            instances+=1
        genes = []

        variations = 1
        if (not found):
            found = True
            while (found):
                nextGene = str(f"{gene}_{variations}")
                (found, genesFound) = searchFile(file, nextGene)
                if found:
                    writeToCSV(genesFound, CSV)
                    instances+=1
                genes = []
                variations = variations+1


    print("100% " +"\t|\t"+ "Instances found: "+str(instances) + '\t|\tFiles searched: ' + str(filesSearched)+'/'+str(fileNum))

    if instances > 0:
        
        print("We found "+str(instances)+" instances of " + gene )
        print("Search your GBk files' directory for " +gene+".csv")
    else: 
        print("We haven't found any genes " + gene + ", make sure you're searching for the correct gene, check spelling")

    gene = input("Enter 'exit' to exit program OR input another gene name (case sensitive) : ")

