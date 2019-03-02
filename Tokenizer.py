#Tokenizer for Jack
#Written by Matthew Hahn

import os

def detType(Type): #Returns a string for given integer value
    return {
        1:'symbol',
        2:'symbol',
        3:'keyword',
        4:'intConstant',
        4.25:'stringConstant',
        4.50:'boolConstant',
        4.75:'nullConstant',
        5:'identifiers',
        }.get(Type,'Unknown')

def ReadIn():   #Returns raw read-in data from a given text file
    File_Data = open("Jack_Test.jack", "r")
    Each_Line = []
    for line in File_Data:
        Each_Line.append(line)
    File_Data.close()
    return Each_Line

def WriteOut(toWrite, Type, inc, Max):  #Writes a single line of processed data to a .txt in XML format
    File_Data = open("XML Output.txt", "a")
    if(os.stat("XML Output.txt").st_size == 0):
        File_Data.write("<tokens>")
    File_Data.write("\n\t <" + detType(Type) + ">" + toWrite + "</" + detType(Type) + ">")
    if(inc == Max):
        File_Data.write("\n</tokens>")
    File_Data.close()

def isIgnore(Line): #Determiner subroutine for if a line should be ignored
    if(len(Line.strip()) == 0):
       return -1
    if(Line.startswith("/")):
       return -1
    return 0

def isSymbol(P,S,O, Next_): #Determiner subroutine for if a character is a symbol
    if(P in S): #Returns 1 for symbol
        return 1
    elif(P in O): #Returns 2 for operator
        return 2
    else:
        return 0

def isReserved(Word, S, O, RS, Next_): #Determiner subroutine for if a string is a reserved word
    if((Word in RS)
       and ((Next_ is " ") or (Next_ in S) or (Next_ in O))): #Returns 3 if so
        return 3
    else:
        return 0

def isConstant(Value, S, O,  Next_): #Determiner subroutine if a string is a constant (Returns some iteration of 4)
    if((Value.isdigit())                                    #If the value is a number
       and ((Next_ is " ") or (Next_ in S) or (Next_ in O))):
        return 4
    elif((Value.startswith('"') and (Value.endswith('"')))  #If the value is in parentheses
         and len(Value) > 1):
        return 4.25
    elif(("true" in Value) or ("false" in Value)):          #If that value is a boolean
        return 4.50
    elif('null' in Value):                                  #If that value is Null
        return 4.75
    else:
        return 0

def isUser(Value, S, O, RS, Next_): #Determiner subroutine if a given string is a user defined identifier
    if(((Value not in RS) and (Value) and (not Value.startswith('"')))
       and ((Next_.isspace()) or (Next_ in S) or (Next_ in O))):
        return 5
    else:
        return 0

if __name__ == "__main__":
    Raw_Data = ReadIn()
    Symbols = ['(',')','[',']','{','}',',',';','=','.']                     #Legal symbols of Jack
    Operators = ['+','-','*','/','&','|','~','<','>']                       #Legal operators of Jack
    R_Words = ['class','constructor','method','function','int','boolean',   #Legal reserved words of Jack
               'char','static','field','let','do','if','else','while',
               'return','true','false','null','this', 'var']

    Raw_Word = ""
    index = inc = ig = ch = wd = cw = 0
    Max = len(Raw_Data)

    for i in Raw_Data: #Reads through raw data, line by line
        inc+=1
        index = 0
        if(isIgnore(i) == -1): #If value should be ignored
            continue
        for j in i:            #Reads through the line, character by character
            Raw_Word += j      #Appends current char to a temporary string for processing
            if((Raw_Word.isspace()) and (not Raw_Word.startswith('"'))):
                Raw_Word = ""  #If value reaches an end character and isn't a constant, clear temp string
            if index+1 < len(i):
                Next_ = i[index+1]
            ch = isSymbol(j,Symbols,Operators,Next_)                   #Checks if this character is a symbol
            wd = isReserved(Raw_Word,Symbols,Operators,R_Words,Next_)  #Checks if this string is a reserved word
            cw = isConstant(Raw_Word,Symbols,Operators,Next_)          #Checks if this string is a constant
            ud = isUser(Raw_Word,Symbols,Operators,R_Words,Next_)      #Checks if this string is a user defined identifier
            if((ch == 1) or (ch == 2)): #If value is a symbol or operator
                WriteOut(j, ch, inc, Max) #Write to XML
                Raw_Word = ""
            elif(wd == 3):  #If value is a reserved word
                WriteOut(Raw_Word, wd, inc, Max) #Write to XML
                Raw_Word = ""
            elif((cw == 4) or (cw == 4.25) or (cw == 4.50) or (cw == 4.75)): #If value is a constant of some kind
                WriteOut(Raw_Word, cw, inc, Max) #Write to XML
                Raw_Word = ""
            elif(ud == 5):  #If value is a user defined identifier
                WriteOut(Raw_Word, ud, inc, Max) #Write to XML
                Raw_Word = ""
            index+=1
