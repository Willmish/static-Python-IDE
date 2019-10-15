from typing import List, Dict
from DataStructures import Stack


# TODO new idea for keeping track of the scopes - for each one remember at which line the scope began and ended,
# in each scope store the their children in a list
# Idea #2:
# Don't keep track of the scopes, analyze the code line by line,
# looking how each variable is referenced and used on each line

class Scope:
    def __init__(self, parent=None, scopeBeginning=0):
        self.scopeBeginning = scopeBeginning
        self.scopeEnding = None
        # a dictionary with all variables in a certain scope,
        # [key: variable name, value: variable type]
        self.variables: Dict[str: str] = {}
        # if there are functions within the scope, it will be
        # defined as a new scope within the scope (checked separately)
        # [key: function, value: return type]
        # self.subscopes: Dict[str: str] = {}
        self.subscopes = []
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

    def getMostRecentScope(self):
        return self.subscopes[-1]

    def getScopeBeginning(self) -> int:
        return self.scopeBeginning

    def getSubscopesBeginning(self, result=''):
        result += 'b' + str(self.scopeBeginning)
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
        self._tokens: List[str] = []  # Keeps track of all INDENT and DE
        self._operators: tuple = ('+', '-', '*', '**', '/', '//', '%')
        self._comparisonOperators: tuple = ('==', '!=', '>', '<', '<=', '>=')
        self._errors: List[str] = []

    def cleanAttributes(self) -> None:  # TODO keeping some of these values might be useful
        # (quicker runtime for multiple checks)
        self._scopes = Scope()
        self._tokens = []
        self._errors = []

    def sortScopes(self, lines, numLines) -> None:
        currentScope = self._scopes
        # TODO sort all scopes according to their indentation, FIXXXX
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
                        currentScope.addSubscope(numLines[i])
                        self._tokens[i] += 'i'
                        currentScope = currentScope.getMostRecentScope()
                        break
                    elif j < indents.peek():
                        while j < indents.peek():
                            self._tokens[i] += 'd'
                            currentScope.setScopeEnding(numLines[i])
                            currentScope = currentScope.parent
                            indents.pop()
                        break
                    else:
                        break
                        # TODO pop until the same indent, add INDENT/DEDENT TAGS
        print(self._tokens)
        print(self._scopes)

    def identifyVariable(self, line, signLoc: int) -> tuple:
        # This function is called whenever a variable definition is found, it returns
        # the name and the type of this variable
        varType: str = ''
        varName: str = ''
        whitespaceOccurred: bool = False
        # The above variable is necessary, because if there are any non-whitespace characters
        # before the var definition, they might get included in the varType
        for i in range(signLoc - 1, -1, -1):
            # If it's a colon, that means the type definition happened before
            if line[i] == ':':
                j = i - 1  # omit colon
                while j >= 0:
                    if line[j] == ' ':  # if end of the definition, break
                        break
                    varName += line[j]  # add all characters to the varName until a space appears
                    j -= 1
                break

            if line[i] != ' ':  # if the above hasn't occurred, than all non-whitespace
                # characters are part of the var type
                if not whitespaceOccurred:  # If a whitespace appeared before, and it's still varType,
                    # break the loop
                    varType += line[i]
                else:
                    break
            elif varType != '':  # If it's not the whitespace between '=' sign and the varType,
                # this is the end of the variable type
                whitespaceOccurred = True

        varType = varType[::-1]
        varName = varName[::-1]
        if varName == '':  # If the user hasn't assigned a type, then the var name got stored in varType
            varName = varType
            varType = ''
        return varName, varType

    def findVariables(self, lines, numLines: List[int]) -> None:
        skipNext = False
        newVar: tuple
        for i, line in enumerate(lines):
            for j in range(0, len(line)):
                if not skipNext:
                    if line[j] == '=':
                        if j > 0:
                            if line[j - 1] in self._operators:
                                # if ^ true, a variable is used here, check its value
                                # TODO run value checking here
                                break

                            elif (line[j - 1] + line[j]) in self._comparisonOperators:
                                # ^ if true a variable is used here for comparison
                                break

                        if j < len(line) - 1:
                            if line[j + 1] == '=':
                                # two equal signs - comparison operator
                                skipNext = True

                            else:
                                print("Variable found on line: " + str(numLines[i]) + ", : " + line)
                                newVar = self.identifyVariable(line, j)
                                self.checkVariableDefinition(newVar, numLines[i])
                                self._scopes.addVariable(newVar[0], newVar[1])
                                break

                        else:
                            print("Incomplete Variable definition on line: " + str(numLines[i]))
                else:
                    skipNext = False

    def findVariablesUsage(self):
        pass

    def checkForEscapeChar(self, line, index):
        backslashes = 0
        for i in range(index, -1, -1):
            if line[i] == ' ':
                break
            if line[i] == '\\':
                backslashes += 1
        if backslashes == 0:
            return False
        return backslashes % 2 != 0

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

    def removeEmptyLines(self, lines, numLines: List[int]) -> tuple:
        # Iterate over every element of the list, if empty, remove it
        i = 0
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

    # This function will check if all variables were defined correctly (were given a type)
    def checkVariableDefinition(self, variable: tuple, lineNo: int) -> None:
        # TODO check if this variable already exists in this scope
        varName = variable[0]
        varType = variable[1]
        if varName in self._scopes.variables.keys():
            if varType == '':
                if self._scopes.variables[varName] != '':
                    pass  # no errors, type hasn't been retyped, but the variable has a type
                # No need to put an else here, if the variable wasn't assigned a type before, this error was
                # already returned
            elif varType == self._scopes.variables[varName]:
                self._errors.append("Line: " + str(lineNo) + " The type of the variable " + varName +
                                    " was unnecessarily reassigned (it was already assigned in this file)")
            else:
                self._errors.append("Line: " + str(lineNo) + " The type of the variable " + varName + " was changed.")

        elif variable[1] == '':
            self._errors.append("Line: " + str(lineNo) + " No type assigned for variable " + variable[0])

    def printErrors(self):
        for line in self._errors:
            print(line)

    def unitTests(self):
        assert self.removeComments(['#dupadupa', '', 'def hi: # this is a comm']) == ['',
                                                                                      '', 'def hi: '], (
            'Removing comments for TCA failed!',)

        assert self.removeEmptyLines(['', '', 'Hello There!', '', '',
                                      ' ', 'General Kenobi!'], [0, 1, 2, 3, 4, 5, 6]) == (['Hello There!', ' ',
                                                                                           'General Kenobi!'],
                                                                                          [2, 5, 6]), (
            'Removing empty lines for TCA failed!',)

        assert self.identifyVariable('bazinga auauu:  myGuy  = wowza', 23) == ('auauu', 'myGuy'), (
            'Identifying variables for TCA failed! - (name and type)',
        )

        assert self.identifyVariable('kupa  wowza  = thats pretty epic', 13) == ('wowza', ''), (
            'Identifying variables for TCA failed! - (name)',
        )

# TODO check alt+~ (`)
