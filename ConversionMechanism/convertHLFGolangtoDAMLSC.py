import re
import argparse
import os
import glob
from datetime import datetime


parser = argparse.ArgumentParser(description='Insert Smart Contract Name')
parser.add_argument('--fabric', dest='smartcontractname', type =str, help='Type the name of the smart contract')
args = parser.parse_args()
smartcontractname =args.smartcontractname
print('The inserted Chaincode name is:', smartcontractname)


#start time monitoring
startTime = datetime.now()

#Delete generated files
def deleteIntermediateFiles():
    for f in glob.glob("function*.go"):
        os.remove(f)
    for j in glob.glob("struct*.go"):
        os.remove(j)

#Split SM based on the number of the functions
class Writer():
    def __init__(self):
        self._num = 0
        self._fh = None

    def close(self):
        if self._fh:
            self._fh.close()

    def start_file(self,filename):
        self.close()
        self._fh = open(filename + "{}.go".format(self._num), "w")
        self._num += 1
        

    def write(self, data):
        if self._fh:
            self._fh.write(data)  

#Removing empty lines from the smart contract
def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)


#Delete comments from the smart contract
def remove_comments(smartcontractname):
    with open(smartcontractname, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if "//" not in line:
                f.write(line)
        f.truncate()

#Find the Fabric's SM name in order to name the same the daml SM
def find_SM_name(smartcontractname):
    global name
    with open(smartcontractname,) as dataFile:
        data = dataFile.read()
        name = data[data.find('type')+5: data.rfind('struct' + '{' + '}')-1]
        with open(name + (".daml") , 'w') as f:
            startdaml = ("module " + name.title() + " where\n")
            f.write(startdaml)
    return (name)


#Finds functions name
def find_functions_names(countFunctions, CCname, arrayStructNames):  
    for y in range(0,countFunctions):
        foundStructs = []
        putStatePointer = 0
        structAboutUpdateValuesArray = []
        updateValeu = ''
        updatedVals = ''
        with open("function" + str(y) + ".go") as dataFile:
            for line in dataFile:
                stringToMatchfunctionName = 'func'
                putStateMessage = 'PutState'
                if stringToMatchfunctionName in line:
                    pointer = find_between(line, '(', ' *')
                    if len(pointer) > 0:
                        searcher = '(' + pointer + ' ' + '*' + CCname+')'
                        countSearcherLen = len(searcher)
                        functionsnames = line[line.find(searcher) + countSearcherLen: line.rfind('(stub')]
                for struct in arrayStructNames:
                    searchStuctforEachFunction = '&' + struct + '{'
                    if searchStuctforEachFunction in line:
                        foundStructs.append(struct)
                if putStateMessage in line:
                    putStatePointer = 1

                for struct in arrayStructNames:
                    searchUpdateChoice = ':= ' + struct + '{' + '}'
                    if searchUpdateChoice in line:
                        removeString = len(searchUpdateChoice) + 2 
                        updateValeu = line[ : -removeString]
                        structAboutUpdateValuesArray.append(struct)
                #Search if the function updates some fields of any struct
                if len(updateValeu):
                    updatedVals = find_update_values(y, updateValeu)
                    

            #Create DAML templates for Fabric functions that invokes the ledger
            if (putStatePointer == 1) and foundStructs and functionsnames:
                with open( CCname + (".daml") , 'a+') as f:
                    writetemplates = ("\ntemplate" + functionsnames.title() + "\n" + "\t" + "with\n")
                    f.write(writetemplates)
                    for value in foundStructs:
                        writevalue = value[0].lower() + value[1:]
                        writeValues=('\t\t' + writevalue + ' : ' +  value + "\n")
                        f.write(writeValues)
                    f.write("\t" + 'where' + "\n")
                    f.write("\t\t" + "--signatory" + "\n")
                    f.write("\t\t" + "--observer" + "\n")
                    f.close()
            #Add DAML choices
            if updatedVals:
                write_choices(CCname, functionsnames, structAboutUpdateValuesArray, updatedVals)

#Check if the function updates a specific struct
def find_update_values (y, key):
    updateValuesArray = []
    with open("function" + str(y) + ".go") as dataFile:
        searcherForUpdateValeu = key + '.'
        for line in dataFile:
            if searcherForUpdateValeu in line:
                keyUpdate = find_between(line,searcherForUpdateValeu,'=')
                updateValuesArray.append(keyUpdate)
        return(updateValuesArray)


#Write DAML choices for connected HLF structs to DAML templates
def write_choices(CCname, functionsnames, structAboutUpdateValuesArray, updatedVals):
    keyStructPointer = 0
    lineCounter = 0
    contractIDCounter = 0
    with open(CCname + ".daml", "r") as dataFile:
        for line in dataFile:
            findTemplate = 'template' 
            if findTemplate in line:
                contractID = line.split(findTemplate,1)[1]
                contractIDCounter = 1

            for structs in structAboutUpdateValuesArray:
                value = structs[0].lower() + structs[1:]
                keyStruct = value + ' : ' + structs
                if keyStruct in line:
                    keyStructPointer = 1
            if 'where' in line:
                wherePointer = 1
                if keyStructPointer == 1 and wherePointer == 1 and contractIDCounter == 1:
                    functionsnames = (functionsnames[1:])
                    with open(functionsnames + ".daml", "w") as newfile:
                        newfile.write('\n')
                        newfile.write('\t\t' + '--' + 'controller' + ' ' + 'can' + '\n')
                        newfile.write('\t\t\t' + functionsnames.title() + ' : ' + 'ContractID ' + contractID)
                        newfile.write('\t\t\t\t' + 'with')
                        newfile.write('\n')
                        with open(CCname + ".daml", "r") as dataFile:
                            for line in dataFile:
                                for newvalues in updatedVals:
                                    value = newvalues[0].lower() + newvalues[1:]
                                    keyUpdatedVal = value + ':'
                                    if keyUpdatedVal in line:
                                        typeOfkeyUpdatedVal = line.split(keyUpdatedVal,1)[1]
                                        if typeOfkeyUpdatedVal:
                                            newfile.write( '\t\t\t\t\t' + 'new' + keyUpdatedVal + typeOfkeyUpdatedVal)
                        newfile.write( '\t\t\t\t' + 'do' + '\n')
                        newfile.write('\t\t\t\t\t' +'create this with' + '\n')
                        for structs in structAboutUpdateValuesArray:
                            newfile.write('\t\t\t\t\t\t' + structs.lower() + ' = ' + structs + ' ' + 'with' + '\n')
                            for newvalues in updatedVals:
                                writeVals = newvalues[0].lower() + newvalues[1:] + '= ' + 'new' + newvalues[0].lower() + newvalues[1:]
                                newfile.write( '\t\t\t\t\t\t\t' + writeVals + '\n')
                            dataFile.close()
                        newfile.close()

                    writeLine = lineCounter + 1
                    merge_CC_with_Options(writeLine, functionsnames, CCname)
                    keyStructPointer = 0
                    contractIDCounter = 0
                    # Finally, delete intermediate files with daml choices
                    os.remove(functionsnames + ".daml")
            lineCounter = lineCounter + 1


#Add the found options
#Merge the generated files with DAML smart contract
def merge_CC_with_Options(writeLine, functionsnames, CCname):
    writeLine = writeLine + 2
    fp = open(functionsnames + ".daml","r")
    # fp is file1
    data = fp.read()
    f = open(CCname + ".daml", 'r')
    #f is file2 on which you want to write data
    ss = f.readlines()
    ss.insert(writeLine,data)
    f = open(CCname + ".daml", 'w')
    f.write(''.join(ss))

#Helper function in order to search for words/phrases into the Chaincode
def find_between( s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last,start)
        return s[start:end]
    except ValueError:
        return ""

#Find the count and the type of the values for each function                    
def find_structs_in_functions(countFunctions, structnames):
    for y in range(0,countFunctions):
        newStructnames = (structnames[1:])
        newStructnames = (newStructnames[:-1])
        searcher ='&' + newStructnames + '{'
        with open("function" + str(y) + ".go") as dataFile:
            putStatePointer = 0
            structPointer = 0
            for line in dataFile:      
                #Find struct on Function name
                stringToMatchStructName = searcher
                putStateMessage = 'PutState'
                
                if stringToMatchStructName in line:
                    structPointer = 1
                if putStateMessage in line:
                    putStatePointer = 1

            if putStatePointer == 1 and structPointer == 1:
                return('Success')

#Remove spaces from parsed values
def convert_data(fieldsStruct):
    newFieldsStruct = re.sub('\s+',' ',fieldsStruct)
    return newFieldsStruct

#Search for the struct names
def find_structs(countStructs):
    arrayStructNames = []
    for x in range(0,countStructs):
        with open("struct" + str(x) + ".go") as dataFileStruct:
            for line in dataFileStruct:
                stringToMatchStructName = 'type'
                if stringToMatchStructName in line:
                    structnames = find_between(line, 'type', 'struct')
                    if len(structnames): 
                        structOnCC =find_structs_in_functions(countFunctions, structnames)
                        if structOnCC == 'Success':
                            newStructnames = (structnames[1:])
                            newStructnames = (newStructnames[:-1])
                            arrayStructNames.append(newStructnames)
    return(arrayStructNames)


#Search for the fields & the data types
def find_data(countStructs, countFunctions, CCname):
    arrayStructNames = find_structs(countStructs)
    for x in range(0,countStructs):
        returnedValue = ''
        structOnCC = 'Not Success'
        previousValue = 'none'
        with open("struct" + str(x) + ".go") as dataFileStruct:
            for line in dataFileStruct:
                for structnames in arrayStructNames:
                    searchBasedOnStructName = 'type' + ' ' + structnames + ' ' + 'struct'
                    if searchBasedOnStructName in line:          
                        with open( CCname + (".daml") , 'a+') as f:
                            writeStructs = ("\ndata" + ' ' + structnames + ' = ' + structnames + " with")
                            f.write(writeStructs)
                            structOnCC = 'Success'
                            f.close()
                stringToMatch = 'string'
                boolToMatch = 'bool'
                intToMatch = 'int'
                floatToMatch = 'float'
                arrayToMatchString = '[]string'
                arrayToMatchFloat = '[]float'
                arrayToMatchInt = '[]int'
                arrayToMatchBool = '[]bool'
                if stringToMatch in line:
                    strValue = line[:line.index(stringToMatch)]
                    returnedValue = convert_data(strValue)
                    valueType = 'Text'
                elif boolToMatch in line:
                    boolValue = line[:line.index(boolToMatch)]
                    returnedValue = convert_data(boolValue)
                    valueType = 'Bool'
                elif intToMatch in line:
                    intValue= line[:line.index(intToMatch)]
                    returnedValue = convert_data(intValue)
                    valueType = 'Int'
                elif floatToMatch in line:
                    floatValue= line[:line.index(floatToMatch)]
                    returnedValue = convert_data(floatValue)
                    valueType = 'Decimal'
                if arrayToMatchString in line:
                    arrayValue= line[:line.index(arrayToMatchString)]
                    returnedValue = convert_data(arrayValue)
                    valueType = '[Text]'
                elif arrayToMatchFloat in line:
                    arrayValue= line[:line.index(arrayToMatchFloat)]
                    returnedValue = convert_data(arrayValue)
                    valueType = '[Decimal]'
                elif arrayToMatchInt in line:
                    arrayValue= line[:line.index(arrayToMatchInt)]
                    returnedValue = convert_data(arrayValue)
                    valueType = '[Int]'
                elif arrayToMatchBool in line:
                    arrayValue= line[:line.index(arrayToMatchBool)]
                    returnedValue = convert_data(arrayValue)
                    valueType = '[Bool]'

                if structOnCC == 'Success' and returnedValue :
                    if previousValue != returnedValue:
                        with open( CCname + (".daml") , 'a+') as f:
                            removeFirstSpace = (returnedValue[1:])
                            firstLetterToLower = removeFirstSpace[0].lower() + removeFirstSpace[1:]
                            dataAndTypes = ("\n " + " " + firstLetterToLower + ': ' + valueType)
                            f.write(dataAndTypes)
                            f.close()
                    previousValue = returnedValue
        if  structOnCC == 'Success':
            with open( CCname + (".daml") , 'a+') as f:
                dataAndTypes = ("\n " + '  '+ 'deriving (Eq,Show)' + "\n ")
                f.write(dataAndTypes)
                f.close()

    find_functions_names(countFunctions, CCname, arrayStructNames)

#Call function in order to delete comments
remove_comments(smartcontractname)
print("Is deleting comments")
#Call function in order to delete empty lines
remove_empty_lines(smartcontractname)
print("Is deleting empty lines")

#Call the class to split the SM into multiples files
writer = Writer()
countFunctions = 0
with open(smartcontractname) as f:
    for line in f:
        if re.match('func', line):
            countFunctions+=1
            writer.start_file('function')
        writer.write(line)        
    writer.close()

writer = Writer()
countStructs = 0
with open(smartcontractname) as f2:
    for line in f2:
        if re.match('type', line):
            countStructs+=1
            writer.start_file('struct')
        if re.match('func', line):
           break
        writer.write(line) 
    writer.close()  



print("Is searching for chaincode name")
CCname = find_SM_name(smartcontractname)
print("Is searching for chaincode fields, data types & structs")
find_data(countStructs,countFunctions, CCname)
print("The smart contract is almost completed")
deleteIntermediateFiles()
print("The conversion time is: ")
print(datetime.now() - startTime)

#The process is finished
DAML_SC =  name +".daml"
print ("Your smart contract has been converted! Check the file" + " " + DAML_SC)
