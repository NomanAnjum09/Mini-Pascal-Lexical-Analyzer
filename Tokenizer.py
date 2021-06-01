from io import StringIO
import re

class Tokenizer():
    symbol_table = {}
    symbol_database = ""
    token_database = ""
    current_line = 0
    current_position =0
    previous_pointer = 0
    previos_lexeme = ""

    symbols = ["<",">",">=","<=","<>","=","(",")","+","-","*","/",":=",";",":"]
    keywords = ["program","var","real","integer","begin","end","if","then","else","while","do","repeat","until","readln","write","writeln","or","div","mod","and","true","false","not","trunc","real"]

    delimeter = [" ","\n"]


    def tokenize(self,code_path):
        file1 = open(code_path,'rb')  # Read file from path

        lines = file1.read() 
        s=str(lines,'utf-8') # Convert to string from bytes
        lines = StringIO(s) 
        for line in lines: #Traverse Each Line
            self.current_line+=1
            lexeme = ""
            self.current_position = -1
            i=0
            while i !=(len(line)): # Traverse each character in line
                self.current_position+=1 # Set current position to 1
                if line[i] == '"': ## String Const Detected
                    if(len(lexeme)>0):
                        self.process_token(lexeme,line) # Process any holded lexeme
                        lexeme=""
                    i = self.parseStringConst(line,i) # Process String Const
                    
                if(line[i] in self.delimeter) and len(lexeme)>0: ## Lexeme completion detected
                    self.process_token(lexeme,line)
                    lexeme=""
                elif line[i:i+2] in self.symbols: # Two character symbol Detected
                    if(len(lexeme)>0):
                        self.process_token(lexeme,line) # process holded lexeme
                        lexeme=""
                    self.current_position+=2
                    self.process_token(line[i:i+2],line,"Symbol") # process two character symbol
                    i+=1
                elif(line[i] in self.symbols): # 1 character symbol detected
                    if(len(lexeme)>0):
                        self.process_token(lexeme,line) #process holded lexeme
                        lexeme=""
                        self.current_position+=1
                    self.process_token(line[i],line,"Symbol") # process one character symbol
                
                elif line[i] not in [" ","\n",""]:
                    lexeme += line[i]
                i+=1
            if len(lexeme)>0:
                self.process_token(lexeme,"") # Process Last token


    def parseStringConst(self,line,i): # Parse string untill closing " is found
       
        i+=1
        lexeme = ""
        self.current_position+=1
        while line[i] != '"':
            lexeme+=line[i]
            i+=1
            self.current_position+=1
        self.process_token(lexeme,line,"StringConst")
        i+=1
        self.current_position+=1
        self.previos_lexeme = lexeme
        return i


    def process_token(self, lexeme,line,token_type=None):
        if token_type is None:
            token_type = self.lookup(lexeme,line) #lookup for token type
            self.token_database+=token_type+","+lexeme+","+str(self.current_line)+","+str(self.current_position-len(lexeme)+1)+"\n"
        else:
            self.token_database+=token_type+","+lexeme+","+str(self.current_line)+","+str(self.current_position-len(lexeme)+1)+"\n"
    
    
    def lookup(self, lexeme,line):
        
        if lexeme in self.keywords:
            self.previos_lexeme = lexeme
            return "Keyword"
        elif lexeme in self.symbols:
            self.previos_lexeme = lexeme
            return "Symbol"

        else: # Not a symbol or keyword
            token_type = self.matchRegex(lexeme,line) # match regex to find if Int real or identfier
            self.previos_lexeme = lexeme
            return token_type


    def matchRegex(self, lexeme,line):
        number = "[0-9]+"
        real = "[0-9]\.[0-9]+"

        if re.match(real,lexeme):
            return "RealConst"
        if re.match(number,lexeme):
            return "IntConst"
        
        else:
            self.registerIdentifier(lexeme,line) # Register identfier on symbol table
            return "Identifier"


    def registerIdentifier(self,lexeme,line):
        if lexeme not in self.symbol_table.keys():
            if self.previos_lexeme == "program":
                self.symbol_table[lexeme] = "KeyWord"
            else:
                type = ""
                for i in range(len(line)):
                    if line[i]==":":
                        i+=1
                        while line[i] not in ["\n",";"]:
                            type+=line[i]
                            i+=1
                        self.symbol_table[lexeme] = type
                        return

    def save_result(self):
        file1 = open("./Output/Tokens.csv", "w")
        file1.write(self.token_database)
        file1.close()
        file1 = open("./Output/SymbolTable.csv", "w")
        for key,value in self.symbol_table.items():
            file1.write(key+","+value+"\n")
        file1.close()




tokenizer = Tokenizer()
tokenizer.tokenize("./InputFiles/code1.pas")
tokenizer.save_result()
