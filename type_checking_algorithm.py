from typing import List, Dict, Tuple

from DataStructures import Stack


# TODO differentiate list reference from a new list definition (e.g. arr: List[int] = [] and arr[0] = 4 is still the same list
# TODO new idea for keeping track of the scopes - for each one remember at which line the scope began and ended,
# in each scope store the their children in a list
# Idea #2:
# Don't keep track of the scopes, analyze the code line by line,
# looking how each variable is referenced and used on each line
# TODO if possible, replace all string with string TOKENS --> youll never have to worry about them again!

class Scope:
    def __init__(self, parent=None, scopeBeginning: int=0):
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

    def getSubscopesBeginning(self, result: str=''):
        result += 'b' + str(self.scopeBeginning)
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


class TCA:
    def __init__(self):
        # List of all scopes, each scope points to their parent
        # self._scopes: List[Scope] = []
        self._scopes: Scope = Scope()
        self._tokens: List[str] = []  # Keeps track of all INDENT and DEDENT tokens and other tokens
        # token list: i indent token, d dedent token, c comparison token, f definition token, v var token followed by
        # var name and ; sign indicating end of var name
        self._variableUseTokens: List[str] = []  # This list keeps track of all variable usage in this format:
        # index i: VariableName;VariableType;Variable2Name;Variable2Type;
        self._operators: Tuple[str, ...] = ('+', '-', '*', '**', '/', '//', '%')
        self._comparisonOperators: Tuple[str, ...] = ('==', '!=', '>', '<', '<=', '>=')
        self._errors: List[str] = []
        self._linesChecked: List[bool] = []
        self._lines: List[str] = []
        self._numLines: List[int] = []

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

    def getVariableUseToken(self) -> List[str]:
        return self._variableUseTokens

    def addErrorMessage(self, line: int, error: str) -> None:
        self._errors.append("Line " + str(line) + ": " + error)

    def addToken(self, token: str, lineIndex) -> None:
        self._tokens[lineIndex] += token

    def addVariableUseToken(self, lineIndex: int, variableName: str, variableType: str):
        self._variableUseTokens[lineIndex] += variableName + ';' + variableType + ';'

    def setInitialLinesChecked(self, lenLines: int):
        self._linesChecked = [False for i in range(lenLines)]

    def setInitialVariableUseTokens(self, lengthOfFile: int):
        self._variableUseTokens = ['' for _ in range(lengthOfFile)]

    def setLines(self, lines: List[str]):
        self._lines = lines

    def setNumLines(self, numLines: List[int]):
        self._numLines = numLines

    def cleanAttributes(self) -> None:  # TODO keeping some of these values might be useful
        # (quicker runtime for multiple checks)
        self._scopes = Scope()
        self._tokens = []
        self._errors = []

    def removeComments(self, lines: List[str]) -> List:
        # Iterates over every line
        for i, line in enumerate(lines):
            apostrophes: int = 0
            speechmarks: int = 0
            # Iterates over every element of each line, with enumerate,
            # so I have the index as well as the value thanks to
            # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
            for j, character in enumerate(lines[i]):
                if character == '\'':   # The part below ensures that no string literals containing
                    if j > 0:           # '#' signs will be cut off
                        if not self.checkForEscapeChar(lines[i], j-1):
                            apostrophes += 1
                    else:
                        apostrophes += 1

                elif character == '\"':
                    if j > 0:
                        if not self.checkForEscapeChar(lines[i], j-1):
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
            i += 1

        return lines, numLines

    def isAnAllowedCharacterInVarName(self, character: str) -> bool: # TODO currently added an option to allow . sign
        # might need to remove later one
        if ord('a') <= ord(character) <= ord('z') or ord('A') <= ord(character) <= ord('Z') or ord('0') <= ord(character) <= ord('9') or character in ('.','_'):
            return True
        return False

    def sortScopes(self, lines: List[str], numLines: List[int]) -> None:
        # Prep the variable use tokens for future use:
        self.setInitialVariableUseTokens(len(lines))
        currentScope = self._scopes
        self._scopes.setScopeEnding(len(lines)-1)
        # TODO sort all scopes according to their indentation, FIX
        #  use: https://docs.python.org/3/reference/lexical_analysis.html#indentation
        # create a stack to keep track of INDENT/DEDENT Tokens
        indents: Stack = Stack(len(lines) + 1)  # The '+1' is required because there is a 0 at the start
        self._tokens = ['' for _ in range(len(lines))]
        indents.push(0)  # Initial 0, to indicate that there is no indentation at the start of the file
        for i in range(len(lines)):  # iterate over every line:
            for j, char in enumerate(lines[i]):  # and over every character
                # if it's a space and the indentation is greater than previously,
                # generate indent token and push the new indentation on top of the stack,
                # (also create a new scope), if its smaller than current indent, keep popping,
                # (and adding dedent tokens) until its at the same level
                if char != ' ':
                    if j > indents.peek():
                        indents.push(j)
                        currentScope.addSubscope(i)
                        self.addToken('i', i)
                        currentScope = currentScope.getMostRecentScope()
                    elif j < indents.peek():
                        while j < indents.peek():
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

    def identifyVariable(self, line: str, signLoc: int, numLine: int) -> Tuple[str, str]:
        # This function is called whenever a variable definition is found, it returns
        # the name and the type of this variable
        varType: str = ''
        varName: str = ''
        whitespaceOccurred: bool = False
        # The above variable is necessary, because if there are any non-whitespace characters
        # before the var definition, they might get included in the varType
        openingBrackets: int = 0    # Used to keep track of opening brackets, allows the use of Complex types,
        # such as Tuple[str, ...]
        closingBrackets: int = 0
        for i in range(signLoc - 1, -1, -1):
            # If it's a colon, that means the type definition happened before
            if line[i] == ':':
                j = i - 1  # omit colon
                while j >= 0:
                    if line[j] == ' ':  # if end of the definition, break
                        break
                    if self.isAnAllowedCharacterInVarName(line[j]): # omits characters not valid for var definition
                        varName += line[j]  # add all characters to the varName until a space appears
                    elif line[j] == '[' or line[j] == ']':
                        return '', ''
                    else:
                        self.addErrorMessage(numLine, "This is not a valid variable name. Variables can only consists "
                                                      "of characters a-z, A-Z, _ and 0-9 (starting with a letter or _)")
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
        return varName, varType

    '''def findVariables(self, lines: List[str], numLines: List[int], currentScope: Scope, start: int = -1, end: int = -1) -> None:
        if not (start == -1 and end == -1):
            lines = lines[start:end+1]
        # TODO change it so that it looks for variables in certain intervals, and run it alongside with sortScopes
        # this way the variables will be sorted in all scopes already
        skipNext = False
        newVar: tuple
        for i, line in enumerate(lines):
            for j in range(0, len(line)):
                if not skipNext:
                    if line[j] == '=':
                        if j > 0:
                            if line[j - 1] in self._operators:
                                # if ^ true, a variable is used here, check its value
                                print("Variable use on line: " + str(numLines[i]) + ", : " + line) # TODO when working
                                # TODO run value checking here
                                break

                            elif (line[j - 1] + line[j]) in self._comparisonOperators:
                                # ^ if true a variable is used here for comparison
                                print("Variable comp on line: " + str(numLines[i]) + ", : " + line)  # TODO when working
                                break

                        if j < len(line) - 1:
                            if line[j + 1] == '=':
                                # two equal signs - comparison operator
                                skipNext = True

                            else:
                                print("Variable found on line: " + str(numLines[i]) + ", : " + line)
                                newVar = self.identifyVariable(line, j, numLines[i])
                                if newVar != ('',''):
                                    if self.checkVariableDefinition(newVar, numLines[i], currentScope):
                                        self._scopes.addVariable(newVar[0], newVar[1])
                                break

                        else:
                            print("Incomplete Variable definition on line: " + str(numLines[i]))
                else:
                    skipNext = False'''

    def findVariableDefinitionsOnLine(self, line: str, index: int, currentScope: Scope) -> List[Tuple[str, str]]:
        skipNext: bool = False
        newVars: List[Tuple[str, str]] = []
        for j in range(0, len(line)):
            if not skipNext:
                if line[j] == '=':
                    if not self.checkIfString(line, j):  # TODO FINISH
                        if j > 0:
                            if line[j - 1] in self._operators:
                                # if ^ true, a variable is used here, check its value
                                print("Variable use on line: " + str(
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
                                    if self.checkVariableDefinition(newVar, index, currentScope):
                                        newVars.append(newVar)
                                        self.addToken('f', index)
                                break

                        else:
                            print("Incomplete Variable definition on line: " + str(index))
            else:
                skipNext = False
        return newVars

    def checkIfVarReference(self, line: str, varName: str, varID: int) -> bool:
        if varID > 0:
            if self.isAnAllowedCharacterInVarName(line[varID-1]):
                return False
        if varID+len(varName) < len(line):
            if self.isAnAllowedCharacterInVarName(line[varID+len(varName)]):
                return False
        return True

    def findVariablesUsage(self, lines: List[str], numLines: List[int], scope: Scope):
        codeLines: List[str] = lines[:]
        for var in scope.variables:
            searchStart = scope.getScopeBeginning()
            searchEnd = scope.getScopeEnding()+1
            i: int = searchStart
            while i < searchEnd:
                if self._linesChecked[i]:
                    i += 1
                    continue
                varIndex = codeLines[i].find(var)
                if varIndex == -1:
                    i+=1
                    continue
                if not self.checkIfString(lines[i], varIndex):
                    if not self.checkIfVarReference(lines[i], var, varIndex):
                            codeLines[i] = codeLines[i][varIndex + len(var):]
                            continue
                    # TODO HERE IS WHERE THE IMPORTANT BIT STARTS: ADD A NEW LIST, KEEPING TRACK OF ALL VAR USAGES, BASED ON WHICH THEY WILL BE CHECKED BOIII!
                    self.addVariableUseToken(i, var, scope.getScopeVariableTypeByKey(var))
                    print("Var", var ," found on line: ", i, ". start index: ", varIndex)
                i += 1

    def findVariableReferenceOnLine(self, line: str, variable: Tuple[str, str]) -> List[int]:
        # TODO use this function in the function above
        # Returns all occurrences of a variable on a line
        myLine = line
        delLine = ''
        varReference: List[int] = []
        variableName = variable[0]
        variableType = variable[1]
        while True:
            varID = myLine.find(variableName)
            if varID == -1:
                break
            if not self.checkIfString(line, varID):
                if self.checkIfVarReference(myLine, variableName, varID):
                    varReference.append(varID + len(delLine))

            delLine += myLine[:varID + len(variableName)]
            myLine = myLine[varID + len(variableName):]

        return varReference

    def checkVariableUsage(self, line: str, lineNo: int, variable: Tuple[str, str]):
        pass # Checks if the variable was used correctly here

    def checkIfString(self, line: str, signIndex: int) -> bool:
        # This function checks if a particular part of code is within a string, or not (mainly used to check whether
        # an = sign is used in a string or not. It achieves that by counting how many ' or " are found on the right
        # of it, if it's odd, then it already knows that it must be in a string. If its even, it makes sure whether
        #  there is an even number of those signs on the left as well
        apostrophes: int = 0
        speechmarks: int = 0
        for i in range(signIndex, len(line)):
            if line[i] == '\'':
                if not self.checkForEscapeChar(line, i-1):
                    apostrophes += 1
            elif line[i] == '\"':
                if not self.checkForEscapeChar(line, i-1):
                    speechmarks += 1
        if (speechmarks+apostrophes) % 2 != 0:
            for i in range(0, signIndex):
                if line[i] == '\'':
                    if not self.checkForEscapeChar(line, i - 1):
                        apostrophes += 1
                elif line[i] == '\"':
                    if not self.checkForEscapeChar(line, i - 1):
                        speechmarks += 1
            if not speechmarks and not apostrophes:
                return False
            return (speechmarks+apostrophes) % 2 == 0
        elif not speechmarks and not apostrophes:
            return False
        return (speechmarks+apostrophes) % 2 != 0

    def checkForEscapeChar(self, line, index):   # Checks whether there is an escape character, or is it just a
        # backslash
        backslashes = 0
        for i in range(index, -1, -1):
            if line[i] == ' ':
                break
            if line[i] == '\\':
                backslashes += 1
        if backslashes == 0:
            return False
        return backslashes % 2 != 0

    # This function will check if all variables were defined correctly (were given a type)
    def checkVariableDefinition(self, variable: Tuple[str, str], lineNo: int, currentScope: Scope) -> bool:
        varName: str = variable[0]
        varType: str = variable[1]
        thisScope: Scope = currentScope
        if varName in thisScope.getScopeVariables().keys():
            if varType == '':
                if thisScope.getScopeVariables()[varName] != '':
                    return False
                # no errors, type hasn't been retyped, but the variable has a type
                # No need to put an else here, if the variable wasn't assigned a type before, this error was
                # already returned
            elif varType == thisScope.getScopeVariables()[varName]:
                self.addErrorMessage(lineNo, " The type of the variable " + varName +
                                     " was unnecessarily reassigned (it was already assigned in this program)")
                return False
            else:
                self.addErrorMessage(lineNo, " The type of the variable " + varName + " was changed.")
                return False

        elif varType == '': # if the var isn;t in this scope, and it has no type, check if its in the scope above
            if thisScope.getScopeParent():
                return self.checkVariableDefinition(variable, lineNo, thisScope.getScopeParent())
            else:
                self.addErrorMessage(lineNo, " No type assigned for variable " + variable[0])
                return True
        elif thisScope.getScopeParent(): # otherwise, simply check if its in the scope above
            return self.checkVariableDefinition(variable, lineNo, thisScope.getScopeParent())

        else: # otherwise, it hasn't appeared in the scopes above and it has a type => is a correct variable def
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
                                      ' ', 'General Kenobi!'], [0, 1, 2, 3, 4, 5, 6]) == (['Hello There!', ' ',
                                                                                           'General Kenobi!'],
                                                                                          [2, 5, 6]), (
            'Removing empty lines for TCA failed!',)

        assert self.identifyVariable('bazinga auauu:  myGuy  = wowza', 23, 1) == ('auauu', 'myGuy'), (
            'Identifying variables for TCA failed! - (name and type)',
        )

        assert self.identifyVariable('kupa  wowza  = thats pretty epic', 13, 1) == ('wowza', ''), (
            'Identifying variables for TCA failed! - (name)',
        )

        assert self.identifyVariable('myString:Tuple[str, int, ...] = \'#nice\'', 30, 1) == ('myString', 'Tuple[str,int,...]'), (
            'Identifying variables for TCA failed! - (name and type)',)

        assert self.findVariableReferenceOnLine("ooga += 2 - 3*ooga", ("ooga", "int")) == [0, 14], ("Finding variable "
                                                                                                    "references on a "
                                                                                                    "specific line "

                                                                                                    "failed!",)
        assert self.findVariableReferenceOnLine("self._myString -= self._myString + str(ooga)",
                                                ("self._myString", '')) == [0, 18], (
            " Finding variable references on a specific line failed!",)

        assert self.findVariableReferenceOnLine("thisVar >= smallVar", ("smallVar", "int")) == [11], (
            "Finding variable references on a specific line for a comparison failed!",)
