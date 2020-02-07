from typing import List, Dict, Tuple

from DataStructures import Stack


# TODO IDEA FOR A FEATURE: ALLOW THE USER TO ADD NEW FUNCTIONS TO BE ACCEPTED BY THE TCA WITH CERTAIN RETURN TYPES ETC.
# TODO USE THE ALREADY DEFINED METHODS AND THEIR RETURN TYPES
# TODO ADD LIST, DICT, AND TUPLE TOKENS, MODIFY THE Variable CLASS AND ADD LIST ATTRIBUTES, ETC.
# TODO ANALYSE THE CASE WHAT HAPPENS IF THERE IS A VAR with just an = sign (e.g. bigVar= )
# TODO NOTE: VARIABLES IN SCOPES ABOVE CAN BE ACCESSED BUT NOT MODIFIED WITHOUT GLOBAL KEYWORD
# TODO RETHINK THE ERROR PRINTING METHOD, MAYBE ADD AN OPTION FOR POINTING THE ERROR DIRECTLY (LOOK test1.py for an example)

# TODO differentiate list reference from a new list definition (e.g. arr: List[int] = [] and arr[0] = 4 is still the same list

# TODO new idea for keeping track of the scopes - for each one remember at which line the scope began and ended,
# in each scope store the their children in a list
# Idea #2:
# Don't keep track of the scopes, analyze the code line by line,
# looking how each variable is referenced and used on each line
# TODO if possible, replace all string with string TOKENS --> youll never have to worry about them again!
# Issue #1: if two scopes are parallel, e.g. two loops one after the other and a function is defined in the one above,
# it will not be recognised in the next scope

class Scope:
    def __init__(self, parent=None, scopeBeginning: int = 0):
        self.scopeBeginning: int = scopeBeginning
        self.scopeEnding: int = None
        # a dictionary with all variables in a certain scope,
        # [key: variable name, value: variable type]
        self.variables: Dict[str, str] = {}
        # if there are functions within the scope, it will be
        # defined as a new scope within the scope (checked separately)
        # [key: function, value: return type]
        # self.subscopes: Dict[str: str] = {}
        self.subscopes: List[Scope] = []
        # pointer to the Scope one layer higher
        self.parent: Scope = parent

    def addVariable(self, name: str, varType: str):
        self.variables[name] = varType

    def addSubscope(self, scopeBeginning):
        self.subscopes.append(Scope(self, scopeBeginning))
        # add  parent, attribute

    def setScopeBeginning(self, index: int) -> None:
        self.scopeBeginning = index

    def setScopeEnding(self, index: int) -> None:
        self.scopeEnding = index

    def getScopeParent(self):
        return self.parent

    def getScopeVariables(self) -> Dict[str, str]:
        return self.variables

    def getScopeVariableTypeByKey(self, Key: str) -> str:
        return self.variables[Key]

    def getMostRecentScope(self):
        return self.subscopes[-1]

    def getScopeBeginning(self) -> int:
        return self.scopeBeginning

    def getScopeEnding(self) -> int:
        return self.scopeEnding

    def getSubscopes(self) -> List:
        return self.subscopes

    def getSubscopesBeginning(self, result: str = ''):
        result += ' b' + str(self.scopeBeginning)
        result += str(self.variables)
        result += ' e'
        result += str(self.scopeEnding) + ' '
        if not self.subscopes:
            return result
        for scope in self.subscopes:
            result += scope.getSubscopesBeginning()
        return result

    def __str__(self):
        return self.getSubscopesBeginning()


class Variable:
    def __init__(self, variableName: str, variableType: str, indexOnLine: int):
        self._name = variableName
        self._type = variableType
        self._indexOnLine = indexOnLine

    def getName(self) -> str:
        return self._name

    def getType(self) -> str:
        return self._type

    def getIndex(self) -> int:
        return self._indexOnLine

    def __str__(self) -> str:
        return self.getName() + ';' + self.getType() + ';' + str(self.getIndex()) + ';'


class ListVariable(Variable):
    def __init__(self, variableName: str, listType: str, indexOnLine: int):
        super().__init__(variableName, listType, indexOnLine)


class DictionaryVariable(Variable):
    def __init__(self, variableName: str, keyType: str, valueType: str, indexOnLine: int):
        super().__init__(variableName, keyType, indexOnLine)
        self._valueType = valueType

    def getValueType(self) -> str:
        return self._valueType

    def __str__(self) -> str:
        return self.getName() + ';' + self.getType() + ';' + self.getValueType() + ';' + str(self.getIndex()) + ';'


class TupleVariable(Variable):
    def __init__(self, variableName: str, variableTypes: List[str], indexOnLine: int):
        if len(variableTypes) == 2:
            if variableTypes[1] == '...':
                super().__init__(variableName, variableTypes[0], indexOnLine)
                self._variableTypes = []
            else:
                super().__init__(variableName, '', indexOnLine)
                self._variableTypes = variableTypes

    def getType(self) -> List[str]:
        if self._variableTypes:
            return self._variableTypes

        else:
            return list(self._type)

    def getTypeOfIndex(self, index: int) -> str:
        if self._variableTypes:
            return self.getType()[index]

        else:
            return ''

    def __str__(self) -> str:
        if self._variableTypes:
            return self.getName() + ';' + str(self.getType()) + ';' + str(self.getIndex()) + ';'


class TCA:
    def __init__(self):
        # List of all scopes, each scope points to their parent
        # self._scopes: List[Scope] = []
        self._scopes: Scope = Scope()
        self._tokens: List[str] = []  # Keeps track of all INDENT and DEDENT tokens and other tokens
        # token list: i indent token, d dedent token, c comparison token, f definition token, v var redefinition with an
        # operator token followed by var name and ; sign indicating end of var name, r variable reassignment
        # l list use token, t tuple use token, s dictionary use token
        self._variableUseTokens: List[
            List[Variable]] = []  # This list keeps track of all variable usage in this format:
        # index i: VariableName;VariableType;Variable2Name;Variable2Type;
        self._operators: Tuple[str, ...] = ('+', '-', '*', '**', '/', '//', '%')
        self._comparisonOperators: Tuple[str, ...] = ('==', '!=', '>', '<', '<=', '>=')
        self._integerCharacters: Tuple[str, ...] = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        self._integerOperators: Tuple[str, ...] = ('+', '-', '*' '**', '//', '%')
        self._errors: List[str] = []
        self._lines: List[str] = []
        self._numLines: List[int] = []
        self._funcReturnTypes: Dict[str, str] = {}
        self.setInitialFuncReturnTypes()

    # Getters and setters for TCA
    def getScopes(self) -> Scope:
        return self._scopes

    def getTokens(self) -> List[str]:
        return self._tokens

    def getOperators(self) -> Tuple[str, ...]:
        return self._operators

    def getComparisonOperators(self) -> Tuple[str, ...]:
        return self._comparisonOperators

    def getErrorMessages(self) -> List[str]:
        return self._errors

    def getLines(self) -> List[str]:
        return self._lines

    def getNumLines(self) -> List[int]:
        return self._numLines

    def getVariableUseToken(self) -> List[List[Variable]]:
        return self._variableUseTokens

    def getIntegerCharacters(self) -> Tuple[str, ...]:
        return self._integerCharacters

    def getIntegerOperators(self) -> Tuple[str, ...]:
        return self._integerOperators

    def addErrorMessage(self, line: int, error: str) -> None:
        self._errors.append("Line " + str(line) + ": " + error)

    def addToken(self, token: str, lineIndex) -> None:
        self._tokens[lineIndex] += token

    def addVariableUseToken(self, lineIndex: int, varIndex: int, variableName: str, variableType: str) -> None:
        self._variableUseTokens[lineIndex].append(Variable(variableName, variableType, varIndex))

    def addListVariableUseToken(self, lineIndex: int, varIndex: int, listName: str, listType: str) -> None:
        self._variableUseTokens[lineIndex].append(ListVariable(listName, listType, varIndex))

    def addDictVariableUseToken(self, lineIndex: int, varIndex: int, dictName: str, dictType: str,
                                dictValueType: str) -> None:
        self._variableUseTokens[lineIndex].append(DictionaryVariable(dictName, dictType, dictValueType, varIndex))

    def addTupleVariableUseToken(self, lineIndex: int, varIndex: int, tupleName: str, tupleTypes: List[str]) -> None:
        self._variableUseTokens[lineIndex].append(TupleVariable(tupleName, tupleTypes, varIndex))

    def setInitialVariableUseTokens(self, lengthOfFile: int):
        self._variableUseTokens = [[] for _ in range(lengthOfFile)]

    def setInitialFuncReturnTypes(self) -> None:
        # TODO FINISH INIT RETURN TYPES (Might need to add an option for parameters
        f = open("functions")
        for line in f:
            newL = line.split()
            self._funcReturnTypes[newL[0]] = newL[1]

        f.close()

    def setLines(self, lines: List[str]):
        self._lines = lines

    def setNumLines(self, numLines: List[int]):
        self._numLines = numLines

    def setVariableUseTokens(self, tokens: List[List[Variable]]):
        self._variableUseTokens = tokens

    def cleanAttributes(self) -> None:  # TODO keeping some of these values might be useful
        # (quicker runtime for multiple checks)
        self._scopes = Scope()
        self._tokens = []
        self._errors = []

    def handleSpecialVarAdding(self, variableName: str, variableType: str, variableIndex: int, lineIndex: int) -> None:
        if 'List' in variableType[:4]:
            newVarType = variableType[len('List') + 1:-1]
            self.addListVariableUseToken(lineIndex, variableIndex, variableName, newVarType)

        elif 'Dict' in variableType[:4]:
            # Split the type of dict into the key type and the value type
            listType = variableType[variableType.find('[') + 1:].split(',')
            listType[-1] = listType[-1][:len(listType[-1]) - 1]
            variableKeyType = ''
            variableValueType = ''
            if len(listType) == 2:
                for char in listType[0]:
                    if char != ' ':
                        variableKeyType += char

                for char in listType[1]:
                    if char != ' ':
                        variableValueType += char
            self.addDictVariableUseToken(lineIndex, variableIndex, variableName, variableKeyType, variableValueType)

        elif 'Tuple' in variableType[:5]:
            ...
        # TODO ADD FOR TUPLE AND DICT

    def removeLastToken(self, index: int):
        self._tokens[index] = self._tokens[index][:-1]

    def removeComments(self, lines: List[str]) -> List:
        # Iterates over every line
        for i, line in enumerate(lines):
            apostrophes: int = 0
            speechmarks: int = 0
            # Iterates over every element of each line, with enumerate,
            # so I have the index as well as the value thanks to
            # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
            for j, character in enumerate(lines[i]):
                if character == '\'':  # The part below ensures that no string literals containing
                    if j > 0:  # '#' signs will be cut off
                        if not self.checkForEscapeChar(lines[i], j):
                            apostrophes += 1
                    else:
                        apostrophes += 1

                elif character == '\"':
                    if j > 0:
                        if not self.checkForEscapeChar(lines[i], j):
                            speechmarks += 1
                    else:
                        speechmarks += 1
                elif character == '#':
                    if apostrophes % 2 == 0 and speechmarks % 2 == 0:
                        lines[i] = lines[i][:j]
                        break

        return lines

    def removeEmptyLines(self, lines: List[str], numLines: List[int]) -> Tuple[List[str], List[int]]:
        # Iterate over every element of the list, if empty, remove it
        i: int = 0
        while i < len(lines):
            # While loop used, because in a for loop, when doing the
            # 'in range(0, len(lines))', length of the List lines is checked only once
            if lines[i] == '':
                # If there is an empty line, delete it (subtract 1 from the iterator,
                # because the indices of the list have changed) as well as the corresponding
                # line number
                lines.pop(i)
                numLines.pop(i)
                i -= 1
            elif lines[i].isspace():  # if the line is only made up of whitespaces, delete it
                lines.pop(i)
                numLines.pop(i)
                i -= 1

            i += 1

        return lines, numLines

    def isAnAllowedCharacterInVarName(self, character: str) -> bool:  # TODO currently added an option to allow . sign
        # might need to remove later one
        if ord('a') <= ord(character) <= ord('z') or ord('A') <= ord(character) <= ord('Z') or ord('0') <= ord(
                character) <= ord('9') or character in ('_',):
            return True
        return False

    def sortScopes(self, lines: List[str], numLines: List[int]) -> None:
        # Prep the variable use tokens for future use:
        self.setInitialVariableUseTokens(len(lines))
        currentScope = self._scopes
        self._scopes.setScopeEnding(len(lines) - 1)
        #  use: https://docs.python.org/3/reference/lexical_analysis.html#indentation
        # create a stack to keep track of INDENT/DEDENT Tokens
        indents: Stack = Stack(len(lines) + 1)  # The '+1' is required because there is a 0 at the start
        self._tokens = ['' for _ in range(len(lines))]
        indents.push(0)  # Initial 0, to indicate that there is no indentation at the start of the file
        skipUntilDedentNTimes = 0  # Necessary for correct scope separation

        for i in range(len(lines)):  # iterate over every line:
            for j, char in enumerate(lines[i]):  # and over every character
                # if it's a space and the indentation is greater than previously,
                # generate indent token and push the new indentation on top of the stack,
                # (also create a new scope), if its smaller than current indent, keep popping,
                # (and adding dedent tokens) until its at the same level
                if char != ' ':
                    if j > indents.peek():
                        indents.push(j)
                        keyIndexD = lines[i - 1].find('def')
                        keyIndexC = lines[i - 1].find('class')
                        if keyIndexD == -1 and keyIndexC == -1:
                            skipUntilDedentNTimes += 1
                            break
                        elif keyIndexD != -1:
                            # if it turns out that the def or Class keyword found in the line above aren't actually
                            #  keywords, then it is not a proper scope
                            if not self.checkIfVarReference(lines[i - 1], 'def', keyIndexD):  # This checks if there are
                                #  any characters before/after the keyword that would interfere with it
                                skipUntilDedentNTimes += 1
                                break
                        elif not self.checkIfVarReference(lines[i - 1], 'class', keyIndexC):
                            skipUntilDedentNTimes += 1
                            break
                        currentScope.addSubscope(i)
                        self.addToken('i', i)
                        currentScope = currentScope.getMostRecentScope()
                    while j < indents.peek():
                        if skipUntilDedentNTimes > 0:
                            skipUntilDedentNTimes -= 1
                            indents.pop()
                        else:
                            self.addToken('d', i)
                            currentScope.setScopeEnding(i)
                            currentScope = currentScope.parent
                            indents.pop()
                    break
            # After managing the current scope, the algorithm looks for variables on that line,
            # and adds them to the current scope
            variables: List[Tuple[str, str]] = self.findVariableDefinitionsOnLine(lines[i], i, currentScope)
            for var in variables:
                currentScope.addVariable(var[0], var[1])
        print(self._tokens)
        print(self._scopes)

    def identifyVariable(self, line: str, signLoc: int, index: int) -> Tuple[str, str]:
        # This function is called whenever a variable definition is found, it returns
        # the name and the type of this variable
        varType: str = ''
        varName: str = ''
        whitespaceOccurred: bool = False
        # The above variable is necessary, because if there are any non-whitespace characters
        # before the var definition, they might get included in the varType
        openingBrackets: int = 0  # Used to keep track of opening brackets, allows the use of Complex types,
        # such as Tuple[str, ...]
        closingBrackets: int = 0
        for i in range(signLoc - 1, -1, -1):
            # If it's a colon, that means the type definition happened before
            if line[i] == ':':
                j = i - 1  # omit colon
                while j >= 0:
                    if line[j] == ' ':  # if end of the definition, break
                        break
                    if self.isAnAllowedCharacterInVarName(line[j]):  # omits characters not valid for var definition
                        varName += line[j]  # add all characters to the varName until a space appears
                    #elif line[j] == '[' or line[j] == ']':  # THIS SHOULD NEVER OCCUR!
                    #    return '', ''
                    else:
                        self.addErrorMessage(self.getNumLines()[index], "This is not a valid variable name. Variables "
                                                                        "can only consists of characters a-z, A-Z, "
                                                                        "_ and 0-9 (starting with a letter or _)")
                        return '', ''
                    j -= 1
                break

            if line[i] == ']':
                openingBrackets += 1
            elif line[i] == '[':
                closingBrackets += 1

            if line[i] != ' ':  # if a colon hasn't appeared, than all non-whitespace
                # characters are part of the var type
                if not whitespaceOccurred:  # If a whitespace appeared before, and it's still varType,
                    # break the loop
                    varType += line[i]
                else:
                    break
            elif varType != '':  # If it's not the whitespace between '=' sign and the varType,
                # this is the end of the variable type
                if openingBrackets <= closingBrackets:  # unless its in the middle of a definition
                    whitespaceOccurred = True

        varType = varType[::-1]
        varName = varName[::-1]
        if varName == '':  # If the user hasn't assigned a type, then the var name got stored in varType
            varName = varType
            varType = ''
            if openingBrackets or closingBrackets:
                # This is a list/tuple/dictionary reference, delete the index reference from the name
                firstOpeningBracket = varName.find('[')
                varName = varName[:firstOpeningBracket]
                varType = 'specialVar'
        return varName, varType

    def findVariableDefinitionsOnLine(self, line: str, index: int, currentScope: Scope) -> List[Tuple[str, str]]:
        skipNext: bool = False
        isASpecialItem: bool = False  # Used to check if the variable is an item of List/Dict/Tuple
        newVars: List[Tuple[str, str]] = []
        for j in range(0, len(line)):
            if not skipNext:
                if line[j] == '=':
                    if not self.checkIfInString(line, j):
                        if j > 0:
                            if line[j - 1] in self._operators:
                                # if ^ true, a variable is used here, check its value
                                print("Variable redefinition with an operator on line: " + str(
                                    self.getNumLines()[index]) + ", : " + line)  # TODO remove when working
                                self.addToken('v', index)
                                # TODO run value checking here
                                # start by checking the type of the variable, if not defined, pass
                                # otherwise check the operator. If invalid, add value error. then, check the RHS of the
                                # = sign. if type not assigned, mark as checked (there already will be an error for the
                                # var not being assigned a type) afterwards, pass it to a suitable function
                                break

                            elif (line[j - 1] + line[j]) in self._comparisonOperators:
                                # ^ if true a variable is used here for comparison
                                print("Variable comp on line: " + str(
                                    self.getNumLines()[index]) + ", : " + line)  # TODO remove when working
                                self.addToken('c', index)
                                break

                        if j < len(line) - 1:
                            if line[j + 1] == '=':
                                # two equal signs - comparison operator
                                skipNext = True
                                print("Variable comp on line: " + str(self.getNumLines()[index]) + ", : " + line)
                                self.addToken('c', index)
                                break

                            else:
                                print("Variable found on line: " + str(self.getNumLines()[index]) + ", : " + line)
                                newVar = self.identifyVariable(line, j, index)
                                if newVar != ('', ''):
                                    if newVar[1] == 'specialVar':
                                        # IT IS A LIST/TUPLE/DICT ITEM DEF / REDEFINITION
                                        newVar = (newVar[0], '')
                                        isASpecialItem = True
                                    if self.checkVariableDefinition(newVar, index, currentScope):
                                        newVars.append(newVar)
                                        self.addToken('f', index)
                                        self.addSpecialVariableRef(newVar[0], newVar[1], index)
                                    else:
                                        if isASpecialItem:
                                            isASpecialItem = False
                                            self.removeLastToken(index)
                                break

                        else:
                            print("Incomplete Variable definition on line: " + str(index) + ': ' + line)
                            # But it can still be identified:
                            newVar = self.identifyVariable(line, j, index)
                            if newVar != ('', ''):
                                if newVar[1] == 'specialVar':
                                    newVar = (newVar[0], '')  # IT IS A LIST/TUPLE/DICT ITEM DEF / REDEFINITION
                                    isASpecialItem = True

                                if self.checkVariableDefinition(newVar, index, currentScope):
                                    newVars.append(newVar)
                                    self.addToken('f', index)
                                    self.addSpecialVariableRef(newVar[0], newVar[1], index)
                                else:
                                    if isASpecialItem:
                                        isASpecialItem = False
                                        self.removeLastToken(index)
                            break
            else:
                skipNext = False
        return newVars

    def checkIfSpecialVariable(self, varName: str, varType: str) -> (bool, str):
        # TODO MAKE SURE THE TOKENS ARE ADDED AND USED CORRECTLY ALONG WITH THE CLASSES (ONLY ADD IF ATTRIBUTES NOT REF ERNCED)
        if 'List' in varType[:4]:
            return True, 'List'

        elif 'Dict' in varType[:4]:
            return True, 'Dict'

        elif 'Tuple' in varType[:5]:
            return True, 'Tuple'
        return False, ''

    def addSpecialVariableRef(self, varName: str, varType: str, index: int) -> bool:
        if 'List' in varType:
            if 'l' not in self.getTokens()[index]:
                self.addToken('l', index)
            return True

        elif 'Dict' in varType:
            if 's' not in self.getTokens()[index]:
                self.addToken('s', index)
            return True

        elif 'Tuple' in varType:
            if 't' not in self.getTokens()[index]:
                self.addToken('t', index)
            return True
        return False

    def checkIfVarReference(self, line: str, varName: str, varID: int) -> bool:
        if varID > 0:
            if self.isAnAllowedCharacterInVarName(line[varID - 1]):
                return False
        if varID + len(varName) < len(line):
            if self.isAnAllowedCharacterInVarName(line[varID + len(varName)]):
                return False
        return True

    def findVariablesReference(self, lines: List[str], numLines: List[int], scope: Scope):
        currentScope = scope
        for var in currentScope.getScopeVariables():
            searchStart = currentScope.getScopeBeginning()
            searchEnd = currentScope.getScopeEnding() + 1
            i: int = searchStart
            while i < searchEnd:
                varRef = self.findVariableReferenceOnLine(self._lines[i], var)
                # CREATE a var use token for each variable reference, unless its a dict/tuple/list, add an
                # appropriate use token then
                if self.checkIfSpecialVariable(var, currentScope.getScopeVariableTypeByKey(var))[0]:
                    for newReferenceIndex in varRef:
                        # IF ITS NOT AN ITEM DEF / REDEFINITION, ADD A LIST/DICT/TUPLE USE TOKEN
                        if newReferenceIndex + len(var) >= len(
                                self.getLines()[i]):  # CHECK IF NOT AT THE END OF THE LINE
                            self.addSpecialVariableRef(var, currentScope.getScopeVariableTypeByKey(var), i)

                        elif self.getLines()[i][newReferenceIndex + len(var)] != '[':
                            self.addSpecialVariableRef(var, currentScope.getScopeVariableTypeByKey(var), i)

                        self.handleSpecialVarAdding(var, currentScope.getScopeVariableTypeByKey(var), newReferenceIndex,
                                                    i)
                        print("Special Var", var, "found on line: ", numLines[i])
                else:
                    for newReferenceIndex in varRef:
                        self.addVariableUseToken(i, newReferenceIndex, var, currentScope.getScopeVariableTypeByKey(var))
                        print("Var", var, " found on line: ", numLines[i], ". start index: ", newReferenceIndex)
                i += 1
        for myScope in currentScope.getSubscopes():
            self.findVariablesReference(lines, numLines, myScope)

    def findVariableReferenceOnLine(self, line: str, variable: str) -> List[int]:
        # Returns all occurrences of a variable on a line
        myLine = line[:]
        delLine = ''  # used to keep track of the part of the string that got deleted while looking for vars
        varReference: List[int] = []
        variableName = variable
        while True:
            varID = myLine.find(variableName)
            if varID == -1:
                break
            if not self.checkIfInString(line, varID + len(delLine)):  # If the variable isn't in a string literal,
                if self.checkIfVarReference(line, variableName,
                                            varID + len(delLine)):  # check in the whole string, not the cut part
                    varReference.append(varID + len(delLine))  # this returns the actual index of the ref on the line

            delLine += myLine[:varID + len(variableName)]
            myLine = myLine[varID + len(variableName):]

        return varReference

    def sortVariableUseTokens(self):
        # This function sorts all varUse tokens according to the order of appearance (key attribute means that the
        # following function will be applied to all elements, and assumes it returns a single value based on which it
        # can be sorted
        newList = []
        for line in self.getVariableUseToken():
            newList.append(sorted(line, key=lambda varIndex: varIndex.getIndex()))
        self.setVariableUseTokens(newList)

    def checkVariablesUsage(self):  # TODO finish it!!
        # TODO Booleans, ensuring the homogeneity of lists and dictionaries' keys and values
        # TODO VARIABLES IN CAPS ARE CONSTANTS
        # TODO ALLOWS HETEROGENEITY OF TUPLES
        # TODO ENSURE PARAMETERS ARE TYPED, AND ALL FUNCT HAVE A RETURN TYPE
        self.sortVariableUseTokens()
        # for i in self.getVariableUseToken():
        #    print(i)
        useTokens = self.getVariableUseToken()
        useTypeTokens = self.getTokens()
        for index, line in enumerate(self.getLines()):
            print(index, line)
            # This dictionary is used to select, depending on the type, appropriate references to the var in error messages
            errorMsgReferenceDict: Dict[str, str] = {'int': 'integer variable',
                                                     'str': 'string variable',
                                                     'float': 'float variable',
                                                     'bool': 'boolean variable',
                                                     'List': 'item in the List',
                                                     'Dict': 'value in the Dictionary',
                                                     'Tuple': 'NONE FOR NOW'}
            errorMsgReference: str = 'variable'
            if useTypeTokens[index] == '':
                continue

            if 'c' in useTypeTokens[index]:
                pass  # It's a comparison

            elif 'f' in useTypeTokens[index] or 'r' in useTypeTokens[index]:  # It is a definition or
                #                                                               no operator redefinition
                definedVar = useTokens[index][0]
                if definedVar.getType() == '':
                    continue

                if isinstance(definedVar, ListVariable):
                    errorMsgReference = errorMsgReferenceDict['List']

                elif isinstance(definedVar, DictionaryVariable):
                    errorMsgReference = errorMsgReferenceDict['Dict']

                elif isinstance(definedVar, TupleVariable):
                    errorMsgReference = errorMsgReferenceDict['Tuple']

                elif isinstance(definedVar, Variable):
                    # This must be checked last, as all the classes above are inheriting
                    #  from this class so their objects are also instances of this class
                    errorMsgReference = errorMsgReferenceDict[definedVar.getType()]

                if 'r' in useTypeTokens[index]:
                    # ---- CHECK IF IT IS A CONSTANT -----
                    if definedVar.getName().isupper():
                        # it is a constant
                        self.addErrorMessage(self.getNumLines()[index],
                                             "The constant variable " + definedVar.getName()
                                             + " cannot change its value. (Constant variables are defined with all "
                                               "uppercase chars)")
                        continue

                useTokens[index].remove(definedVar)
                # if not useTokens[index]:  # Run single variable checking here
                checkLine = line

                # -----  LIST  -----
                if 'l' in useTypeTokens[index]:  # List definition/redefinition
                    listType = definedVar.getType()
                    checkTuple = self.checkIfAllVarsOfType(listType, useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")

                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non ' + listType + ' value on '
                                                                                                          'this line. '
                                                                                                          '(A variable of different type was used.')
                        continue
                    checkLine = checkLine[checkLine.find('=') + 1:]
                    checkVal = self.checkIfListOfType(checkLine, listType)
                    if checkVal == 0:
                        continue
                    elif checkVal == 1:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: List ' + definedVar.getName() +
                                             ' was assigned a non list value on this line.')
                        continue
                    elif checkVal == 2:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: List ' + definedVar.getName() +
                                             ' is not homogeneous (not all elements in the list are of type  '
                                             + listType + ')')
                        continue
                    pass  # TODO FINISH HERE
                # ------------------
                # -----  DICT  -----
                elif 's' in useTypeTokens[index]:  # Dictionary definition/redefinition
                    pass
                # ------------------
                # ----- TUPLES -----
                elif 't' in useTypeTokens[index]:
                    pass
                # ------------------
                # -----INTEGERS-----
                if definedVar.getType() == 'int':
                    # TODO IMPORTANT, MAKE SURE THAT LIST VAR IF REFERENCE TO THE WHOLE LIST CHECKED SEPERATELY AS A LIST
                    # TODO CHECK WHAT ACTION CAN BE PERFORMED ON LIST/DICT/TUPLE ETC
                    checkTuple = self.checkIfAllVarsOfType('int', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")

                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non integer value on this line. '
                                                                      '(A variable of different type was used. maybe us'
                                                                      'e a conversion function int() ?)')
                        continue

                    checkLine = checkLine[checkLine.find('=') + 1:]
                    print(checkLine)
                    if not self.checkIfInteger(checkLine):
                        self.addErrorMessage(self.getNumLines()[index],
                                             ('TYPE ERROR: ' + errorMsgReference + ' ' + definedVar.getName() +
                                              ' was assigned a non integer value on this line.'))
                # ------------------
                # -----STRINGS------
                elif definedVar.getType() == 'str':
                    # ENSURES OTHER VARS APPEARING ON THIS LINE ARE OF THE SAME TYPE/CONVERTED TO THIS TYPE
                    checkTuple = self.checkIfAllVarsOfType('str', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non string value on this line. '
                                                                      '(A variable of different type was used. maybe us'
                                                                      'e a conversion function str() ?)')
                        continue

                    checkLine = checkLine[checkLine.find('=') + 1:]
                    checkVal = self.checkIfString(checkLine)
                    if checkVal == 0:
                        continue
                    elif checkVal == 1:
                        self.addErrorMessage(self.getNumLines()[index], 'Unexpected character '
                                                                        'after line continuation character'
                                                                        ' (backslash) ')
                    else:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non string value on this line.')
                # ------------------
                # -----FLOATS-------
                elif definedVar.getType() == 'float':
                    checkTuple = self.checkIfAllVarsOfType('float', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non float value on this line. '
                                                                      '(A variable of different type was used. maybe us'
                                                                      'e a conversion function float() ?)')
                        continue

                    checkLine = checkLine[checkLine.find('=') + 1:]
                    checkVal = self.checkIfFloat(checkLine)
                    if checkVal == 0:
                        continue
                    elif checkVal == 1:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + definedVar.getName() + ' was assigned a non Float value on this line.')
                    elif checkVal == 2:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' ' +
                                             definedVar.getName() + ' was assigned a non Float value on this line; '
                                                                    'Only integers appeared (Perhaps use a single /'
                                                                    ' division or add a decimal point')
                # ------------------
                elif definedVar.getType() == 'bool':
                    pass
                else:
                    pass  # Run multi-var checking here

            # elif 'r' in self.getTokens()[index]:  # It is a redefinition with no operators
            #    redefinedVar = useTokens[index][0]  # First variable is the redefined var
            #    if redefinedVar.getType() == '':
            #        continue
            #
            #    useTokens[index].remove(redefinedVar)
            #
            #    if not useTokens[index]:
            #        # If no other variable references on this line, its a single var redef
            #        equalSignIndex = line.find('=')
            #        checkLine = line[equalSignIndex + 1:]
            #        # ---- INTEGER ----
            #        if redefinedVar.getType() == 'int':
            #            if not self.checkIfInteger(checkLine):
            #                self.addErrorMessage(self.getNumLines()[index], ('TYPE ERROR: Integer Variable '
            #                                                                 + redefinedVar.getName() +
            #                                                                 ' is assigned a non integer value'
            #                                                                 ' on this line.'))
            #                continue
            #        # -----------------
            #        # ---- STRING -----
            #        if redefinedVar.getType() == 'str':
            #            pass
            #        # -----------------

            elif 'v' in self.getTokens()[index]:  # It is a redefinition
                print(line)
                redefinedVar = useTokens[index][0]  # First variable is the redefined var
                if redefinedVar.getType() == '':
                    continue

                if isinstance(redefinedVar, ListVariable):
                    errorMsgReference = errorMsgReferenceDict['List']

                elif isinstance(redefinedVar, DictionaryVariable):
                    errorMsgReference = errorMsgReferenceDict['Dict']

                elif isinstance(redefinedVar, TupleVariable):
                    errorMsgReference = errorMsgReferenceDict['Tuple']

                elif isinstance(redefinedVar, Variable):
                    # This must be checked last, as all the classes above are inheriting
                    #  from this class so their objects are also instances of this class
                    errorMsgReference = errorMsgReferenceDict[redefinedVar.getType()]
                # ---- CHECK IF IT IS A CONSTANT -----
                if redefinedVar.getName().isupper():
                    # it is a constant
                    self.addErrorMessage(self.getNumLines()[index], "The constant variable " + redefinedVar.getName()
                                         + " cannot change its value. (Constant variables are defined with all "
                                           "uppercase chars)")
                    continue
                useTokens[index].remove(redefinedVar)
                equalSignIndex = line.find('=')

                # ----- INTEGER -----
                if redefinedVar.getType() == 'int':
                    # CHECK OTHER VARIABLES:
                    checkTuple = self.checkIfAllVarsOfType('int', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")

                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + redefinedVar.getName() + 'was assigned a non integer value on this '
                                                                        'line. (A variable of different type was used.'
                                                                        ' maybe use a conversion function int() ?)')
                        continue

                    if 'l' in useTypeTokens[index]:  # List redefinition
                        if line[equalSignIndex - 1] != '+':
                            self.addErrorMessage(self.getNumLines()[index], "TYPE ERROR: Lists can only be "
                                                                            "added together (other standard "
                                                                            "operations are not supported)")
                            continue
                    elif 's' in useTypeTokens[index]:  # Dictionary redefinition
                        pass
                    elif 't' in useTypeTokens[index]:
                        self.addErrorMessage(self.getNumLines()[index], "Tuple objects do not support item "
                                                                        "assignment. (Tuples are immutable, their "
                                                                        "items cannot be modified after creation)")
                        continue
                    if line[equalSignIndex - 1] == '/':
                        if equalSignIndex - 2 >= 0:
                            if line[equalSignIndex - 1] + line[equalSignIndex - 2] != '//':
                                self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference
                                                     + ' ' + redefinedVar.getName()
                                                     + ' was reassigned using a non Integer operator '
                                                       '(Non-Integer Division / )')
                                continue

                    checkLine = checkLine[checkLine.find('=') + 1:]
                    if not self.checkIfInteger(checkLine):
                        self.addErrorMessage(self.getNumLines()[index], ('TYPE ERROR: ' + errorMsgReference + ' '
                                                                         + redefinedVar.getName() +
                                                                         ' was assigned a non integer value'
                                                                         ' on this line.'))
                        continue
                # --------------------
                # ------ STRING ------
                elif redefinedVar.getType() == 'str':
                    if line[equalSignIndex - 1] != '+':
                        self.addErrorMessage(self.getNumLines()[index], "TYPE ERROR: " + errorMsgReference + ' ' +
                                             redefinedVar.getType() + " redefined using an invalid operator"
                                                                      " for strings; Strings can only be added to"
                                                                      " each other")
                        continue
                    # ENSURES OTHER VARS APPEARING ON THIS LINE ARE OF THE SAME TYPE/CONVERTED TO THIS TYPE
                    checkTuple = self.checkIfAllVarsOfType('str', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + redefinedVar.getName() + ' was assigned a non integer value on'
                                                                        ' this line. (A variable of different type was'
                                                                        ' used. maybe use a conversion '
                                                                        'function str() ?)')
                        continue
                    checkLine = checkLine[checkLine.find('=') + 1:]
                    checkVal = self.checkIfString(checkLine)
                    if checkVal == 0:
                        continue
                    elif checkVal == 1:
                        self.addErrorMessage(self.getNumLines()[index], 'Unexpected character '
                                                                        'after line continuation character'
                                                                        ' (backslash) ')
                    else:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + redefinedVar.getName() +
                                             ' was assigned a non string value on '
                                             'this line.')
                # --------------------
                # ------ FLOATS ------
                elif redefinedVar.getType() == 'float':
                    if line[equalSignIndex - 1] == '/':
                        if equalSignIndex - 2 >= 0:
                            if line[equalSignIndex - 1] + line[equalSignIndex - 2] == '//':
                                self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference
                                                     + ' ' + redefinedVar.getName()
                                                     + ' was reassigned using an Integer operator '
                                                       '(Integer Division // )')
                                continue
                    # ENSURES ALL VARS OF THE SAME TYPE/CONVERTED TO THE SAME TYPE
                    checkTuple = self.checkIfAllVarsOfType('float', useTokens[index], line)
                    if checkTuple[0]:
                        print(self.getNumLines()[index], " All vars same type")
                        checkLine = checkTuple[1]
                        checkLine = self.removeAllVarsInLine(useTokens[index], checkLine)
                        # remove all occurrences of the var in the line ^
                    else:
                        print(self.getNumLines()[index], " Not All vars same type")
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference + ' '
                                             + redefinedVar.getName() + ' was assigned a non float value on this line. '
                                                                        '(A variable of different type was used. maybe'
                                                                        ' use a conversion function float() ?)')
                        continue

                    checkLine = checkLine[checkLine.find('=') + 1:]
                    checkVal = self.checkIfFloat(checkLine)
                    if checkVal == 0:
                        continue
                    elif checkVal == 1:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference
                                             + ' ' + redefinedVar.getType() + ' was assigned a non Float value'
                                                                              ' on this line.')
                    elif checkVal == 2:
                        self.addErrorMessage(self.getNumLines()[index], 'TYPE ERROR: ' + errorMsgReference
                                             + ' ' + redefinedVar.getType() + ' was assigned a non Float value on '
                                                                              'this line; Only integers appeared ('
                                                                              'Perhaps use a single /'
                                                                              ' division or add a decimal point')
                else:
                    pass  # Multi-var checking here

    def removeAllVarsInLine(self, vars: List[Variable], codeLine: str) -> str:
        deletedChars = 0  # TODO MAKE SURE IT REMOVES THE int( ) before and after part, maybe do it in the funct below and pop from the list
        for var in vars:
            # Removes the variables specified in the vars List from the codeLine str
            varStart = var.getIndex() - deletedChars
            varEnd = var.getIndex() + len(var.getName()) - deletedChars
            codeLine = codeLine[:varStart] + codeLine[varEnd:]
            print(codeLine)
            deletedChars += len(var.getName())
        return codeLine

    def checkIfAllVarsOfType(self, type: str, vars: List[Variable], codeLine: str) -> (bool, str):
        newCodeLine = codeLine[:]
        for var in vars:
            if var.getType() != type:
                # check if there isn;t a conversion function before
                funStart = var.getIndex() - len(type) - 1
                funEnd = var.getIndex() - 1
                if funStart < 0:
                    return False, newCodeLine
                if codeLine[funStart:funEnd] == type:
                    # Removes the conversion function along with the reference for further checking
                    endRef = funEnd + len(var.getName()) + 2  # take the () into account
                    newCodeLine = codeLine[:funStart] + ' ' * len(codeLine[funStart:endRef]) + codeLine[
                                                                                               endRef:]  # TODO FINISH (other functions?)
                    vars.remove(var)
                    print("Length before and after removing conversion func: ", len(codeLine), len(newCodeLine))
                    continue
                return False, newCodeLine
        return True, newCodeLine

    def checkIfListOfType(self, checkLine: str, type: str) -> int:
        openingBrackets: int = 0
        closingBrackets: int = 0

        for char in checkLine:
            if char == '[':
                openingBrackets += 1
                continue
            if char == ']':
                closingBrackets += 1
                continue

            # chop it by ,
        if openingBrackets != closingBrackets:
            return 1  # NOT A LIST

        if openingBrackets == 1:  # There is only one list
            listVals = checkLine.split(',')
            listVals[0] = listVals[0][listVals[0].find('[') + 1:]  # remove the brackets
            listVals[-1] = listVals[-1][:listVals[-1].find(']')]
            for lineI, line in enumerate(listVals):
                if not self.checkIfInteger(line):
                    return 2  # NOT HOMOGENEOUS

        return 0  # ALL GOOD

    def checkIfInteger(self, checkLine: str) -> bool:
        # TODO Modify so that it checks for common functions and their return types (e.g. find(random.randint() etc.)
        skipNext = False
        for charIndex, character in enumerate(checkLine):
            if skipNext:
                skipNext = False
                continue

            if not (character in self.getIntegerCharacters()
                    or character in self.getIntegerOperators() or character == ' '):
                if charIndex < len(checkLine) - 1:  # Checks if its not a 2 character operator (//)
                    if (character + checkLine[charIndex + 1]) not in self.getIntegerOperators():
                        return False
                    else:
                        skipNext = True  # skip next character to avoid errors, (a // char was used)
                        continue
                else:
                    return False
        return True

    def checkIfString(self, checkLine: str) -> int:
        apostrophes: int = 0
        speechmarks: int = 0
        for charIndex, character in enumerate(checkLine):
            if character == "'":
                if not self.checkForEscapeChar(checkLine, charIndex):
                    apostrophes += 1
                elif (apostrophes != 0 and apostrophes % 2 != 0) or (speechmarks != 0 and speechmarks % 2 != 0):
                    continue  # Nothing to do here, the sign is inside a string so its valid
                else:
                    return 1  # This will never occur, because the \ sign would not be allowed by the last elif
                    #           statement ( Might modify how this method works, so I will keep it if anything
                    #           was to ever go wrong
            elif character == '"':
                if not self.checkForEscapeChar(checkLine, charIndex):
                    speechmarks += 1
                elif (apostrophes != 0 and apostrophes % 2 != 0) or (speechmarks != 0 and speechmarks % 2 != 0):
                    continue  # Nothing to do here, the sign is inside a string so its valid
                else:
                    return 1
            # If the character is inside a string literal, skip it
            elif (apostrophes != 0 and apostrophes % 2 != 0) or (speechmarks != 0 and speechmarks % 2 != 0):
                continue
            # Check if non-string value
            elif not (character == ' ' or character == '+'):
                return 2
        return 0

    def checkIfFloat(self, checkLine: str) -> int:
        decimalPointOcurred: bool = False
        isAFloat: bool = False
        currentlyNumber: bool = False
        skipNext: bool = False
        for index, character in enumerate(checkLine):
            if skipNext:
                skipNext = False
                continue
            if character in self.getIntegerCharacters():
                currentlyNumber = True
            elif character == '.':
                # CAN ADD AN IF STATEMENT TO CHECK IF . OCCURRED BEFORE, TO ENSURE THERE ARE NO ERRORS,
                # CURRENTLY ONLY CHECKS IF "FLOAT CHARACTERS" ARE USED
                if currentlyNumber:
                    decimalPointOcurred = True
                    isAFloat = True

            elif character == ' ':
                decimalPointOcurred = False
                currentlyNumber = False

            elif character in self.getOperators():
                decimalPointOcurred = False
                currentlyNumber = False
                if character == '/' and index < len(checkLine) - 1:
                    if checkLine[index + 1] != '/':
                        isAFloat = True  # If there was a non-Integer division, it isn't an integer
                    else:
                        skipNext = True

            else:
                return 1  # non FLOAT characters used

        if isAFloat:
            return 0  # only FLOAT characters used, let the interpreter do
            #           the hard work of checking if they are in correct order
        else:
            return 2  # INTEGER characters used, but no FLOAT characters

    def checkVariableUsageOnLine(self, line: str, lineNo: int, variable: Tuple[str, str]):
        pass  # Checks if the variable was used correctly here

    def checkIfInString(self, line: str, signIndex: int) -> bool:
        # This function checks if a particular part of code is within a string, or not (mainly used to check whether
        # an = sign is used in a string or not. It achieves that by counting how many ' or " are found on the right
        # of it, if it's odd, then it already knows that it must be in a string. If its even, it makes sure whether
        #  there is an even number of those signs on the left as well TODO check all cases work
        apostrophes: int = 0
        speechmarks: int = 0
        for i in range(signIndex, len(line)):
            if line[i] == '\'':
                if not self.checkForEscapeChar(line, i):
                    apostrophes += 1
            elif line[i] == '\"':
                if not self.checkForEscapeChar(line, i):
                    speechmarks += 1
        if (speechmarks + apostrophes) % 2 != 0:
            for i in range(0, signIndex):
                if line[i] == '\'':
                    if not self.checkForEscapeChar(line, i):
                        apostrophes += 1
                elif line[i] == '\"':
                    if not self.checkForEscapeChar(line, i):
                        speechmarks += 1
            if not speechmarks and not apostrophes:
                return False
            return (speechmarks + apostrophes) % 2 == 0
        elif not speechmarks and not apostrophes:
            return False
        return (speechmarks + apostrophes) % 2 != 0

    def checkForEscapeChar(self, line, index):  # Checks whether there is an escape character, or is it just a
        # backslash before a character with an index -> index
        backslashes = 0
        if index == 0:
            return False

        for i in range(index - 1, -1, -1):
            if line[i] == '\\':
                backslashes += 1
            else:
                break
        if backslashes == 0:
            return False
        return backslashes % 2 != 0

    # This function will check if all variables were defined correctly (were given a type)
    def checkVariableDefinition(self, variable: Tuple[str, str], index: int, currentScope: Scope) -> bool:
        # TODO REMOVE CHECKING IF IN THE SCOPES ABOVE, SEE EXAMPLE IN TEST1
        varName: str = variable[0]
        varType: str = variable[1]
        thisScope: Scope = currentScope
        if varName in thisScope.getScopeVariables().keys():
            if varType == '':
                if thisScope.getScopeVariableTypeByKey(varName) != '':
                    self.addToken('r', index)
                    self.addSpecialVariableRef(varName, thisScope.getScopeVariableTypeByKey(varName), index)
                    return False
                # no errors, type hasn't been retyped, but the variable has a type
                # No need to put an else here, if the variable wasn't assigned a type before, this error was
                # already returned
            elif varType == thisScope.getScopeVariables()[varName]:
                self.addErrorMessage(self.getNumLines()[index], " The type of the variable " + varName +
                                     " was unnecessarily reassigned (it was already assigned in this program)")
                return False
            else:
                self.addErrorMessage(self.getNumLines()[index],
                                     " The type of the variable " + varName + " was changed.")
                return False

        elif varType == '':  # if the var isn;t in this scope, and it has no type, check if its in the scope above
            if thisScope.getScopeParent():
                return self.checkVariableDefinition(variable, index, thisScope.getScopeParent())
            else:
                self.addErrorMessage(self.getNumLines()[index], " No type assigned for variable " + variable[0])
                return True
        elif thisScope.getScopeParent():  # otherwise, simply check if its in the scope above
            return self.checkVariableDefinition(variable, index, thisScope.getScopeParent())

        else:  # otherwise, it hasn't appeared in the scopes above and it has a type => is a correct variable def
            return True

    def printErrors(self):
        for line in self._errors:
            print(line)

    def unitTests(self):
        assert self.removeComments(['#dupadupa', '', 'def hi: # this is a comm']) == ['',
                                                                                      '', 'def hi: '], (
            'Removing comments for TCA failed!',)

        assert self.removeComments(['#aaaaaaahhhhhh', '', '#aaaaah',
                                    's: str = \'#yeee\'', 'd: str = \'\'#oof\'']) == ['', '', '', 's: str = \'#yeee\'',
                                                                                      'd: str = \'\''], (
            'Removing comments for TCA failed!',)

        assert self.removeEmptyLines(['', '', 'Hello There!', '', '',
                                      ' ', 'General Kenobi!'], [0, 1, 2, 3, 4, 5, 6]) == (['Hello There!',
                                                                                           'General Kenobi!'],
                                                                                          [2, 6]), (
            'Removing empty lines for TCA failed!',)

        assert self.identifyVariable('bazinga auauu:  myGuy  = wowza', 23, 1) == ('auauu', 'myGuy'), (
            'Identifying variables for TCA failed! - (name and type)',
        )

        assert self.identifyVariable('kupa  wowza  = thats pretty epic', 13, 1) == ('wowza', ''), (
            'Identifying variables for TCA failed! - (name)',
        )

        assert self.identifyVariable('myString:Tuple[str, int, ...] = \'#nice\'', 30, 1) == (
            'myString', 'Tuple[str,int,...]'), (
            'Identifying variables for TCA failed! - (name and type)',)

        assert self.identifyVariable("testList[2] = 23", 12, 0) == ('testList', 'specialVar'), (
            "Identifying variables for TCA failed! - (special var reference)")

        assert self.checkIfSpecialVariable('myList', 'Dict[List[int], str]') == (True, 'Dict'), (
            "Checking if variable is a special variable of type Dict failed!")

        assert self.checkIfSpecialVariable('notSpecial', 'int') == (False, ''), (
            'Checking if variable is special failed! (int is not special!)')

        assert self.checkIfSpecialVariable('myTuple', 'Tuple[List[int], str, Dict[str, int])') == (True, 'Tuple'), (
            'Checking if variable is a special variable of type Tuple failed!')

        assert self.checkIfSpecialVariable('BublinJechane', 'Dict[List[str], int]') == (True, 'Dict'), (
            'Checking if variable is a special variable of type Dict failed!')

        assert self.findVariableReferenceOnLine("ooga += 2 - 3*ooga", "ooga") == [0, 14], ("Finding variable "
                                                                                           "references on a "
                                                                                           "specific line "
                                                                                           "failed!",)

        assert self.findVariableReferenceOnLine("self._myString -= self._myString + str(ooga)",
                                                "self._myString") == [0, 18], (
            " Finding variable references on a specific line failed!",)

        assert self.findVariableReferenceOnLine("thisVar >= smallVar", "smallVar") == [11], (
            "Finding variable references on a specific line for a comparison failed!",)

        assert self.removeAllVarsInLine([Variable('Bublin', 'int', 0), Variable('newVar', 'str', 10)],
                                        'Bublin += newVar') == ' += ', (
            'Removing all Variables in a line failed!') # TODO check if keeeping the spaces is necessary

        assert self.checkIfInteger("-5 + 2 // 3"), ("Checking if only integer-like operators"
                                                    " and chars used failed!",)

        assert not self.checkIfInteger('-5/2'), ("Checking if only integer-like operators and chars used failed!",)

        assert self.checkIfString('\'my * 2 string\' + \'string\\') == 0, ("Checking if only string-like operators and "
                                                                           "chars used failed!",)

        assert self.checkIfFloat('23 - 4//6') == 2, ("Checking if only float-like operators and chars used failed!",)

        assert self.checkIfFloat('5/2 -1') == 0, ("Checking if only float-like operators and chars used failed!",)

        assert self.checkIfFloat('2-d') == 1, ("Checking if only float-like operators and chars used failed!",)

        assert not self.checkForEscapeChar('\\\\se\'', 2), ("Checking for Escape Character before a sing with "
                                                            "index i failed!",)

        assert self.checkForEscapeChar('\\\'not a string\'', 1), ("Checking for Escape Character before "
                                                                  "sign with index i failed!",)

        assert self.checkIfInString('\'au\'', 1), ("Checking if character with index i is in a string failed!",)

        assert not self.checkIfInString('\'this is not a string', 1), ("Checking if character with index i is in a"
                                                                       " string failed!")
