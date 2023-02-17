import sys
import tpg
class EvalError(Exception):
    """Class of exceptions raised when an error occurs during evaluation."""


# These are the classes of nodes of our abstract syntax trees (ASTs).

class Node(object):
    """Base class of AST nodes.  May come in handy in the future."""
    
    def eval(self):
        """Evaluate the AST node, called on nodes of subclasses of Node."""
        raise Exception("Not implemented.")

class Int(Node):
    """Class of nodes representing integer literals."""

    def __init__(self, value):
        self.value = int(value)
    
    def eval(self):
        return self.value
class String(Node):
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        return self.value
class String(Node):
    def __init__(self, value):
        self.value = value.strip('"')
    
    def eval(self):
        return self.value
class Add(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if (isinstance(left,int) and isinstance(right,int)) or (isinstance(left,str) and isinstance(right,str)):
            return left + right
        raise EvalError()
class Subtract(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        return left - right
class Multiply(Node):
    """Class of nodes representing integer multiplications."""

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left,int): raise EvalError()
        if not isinstance(right,int): raise EvalError()
        return left * right

class Divide(Node):
    """Class of nodes representing integer divisions."""

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left, int): raise EvalError()
        if not isinstance(right, int): raise EvalError()
        if right == 0: raise EvalError()
        return int(left / right)

class Concat(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left, str):
            raise EvalError()
        if not isinstance(right, str):
            raise EvalError()
        return left + right
class List(Node):
    def __init__(self, elements):
        self.elements = elements
    

    def eval(self):
        return [e.eval() for e in self.elements]
class Lessthan(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        return 1 if left < right else 0
class Greaterthan(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        return 1 if left > right else 0
class Equal(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        return 1 if left == right else 0
class Not(Node):
        def __init__(self, condition):
            self.condition = condition
        def eval(self):
            condition = self.condition.eval()
            if not isinstance(condition, int): raise EvalError()
            return 1 if not condition != 0 else 0
class And(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left, int): raise EvalError()
        if not isinstance(right, int): raise EvalError()
        return 1 if left != 0 and right != 0 else 0
class Or(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if not isinstance(left, int): raise EvalError()
        if not isinstance(right, int): raise EvalError()
        return 1 if left != 0 or right != 0 else 0
class Index(Node):
    def __init__(self, left, right):
        # The nodes representing the left and right sides of this operation.
        self.left = left
        self.right = right
    def eval(self):
        left = self.left.eval()
        if not isinstance(left, str) and not isinstance(left, list):
            raise EvalError()
        right = self.right.eval()
        if not isinstance(right, int):
            raise EvalError()
        if right >= len(left) or right < 0:
            raise EvalError
        return left[right]
# This is the parser using TPG for parsing expressions and building an AST.
class Parser(tpg.Parser):
    r"""
    token int:         '\d+' ;              # 1+ (1 or more) decimal digits
    token string:      '\"[^\"]*\"' ;       # ", then 0+ non-", then "
    separator spaces:  '\s+' ;              # 1+ white space/tab/return chars


    START/s -> Pick/s;
    Pick/e -> ExpList/e | Exp/e;
    ExpList/e -> Index/e;
    Exp/e   -> Or/e;
    Or/e -> And/e ('or' And/e2 $e=Or(e, e2)$)*;
    And/e -> Not/e ('and' Not/e2 $e=And(e2, e)$)*;
    Not/e -> ('not' Not/e $e=Not(e)$) | Comp/e;
    Comp/e -> Sum/e ('\<' Sum/e2 $e=Lessthan(e, e2)$ | '\>' Sum/e2 $e=Greaterthan(e, e2)$ | '\==' Sum/e2 $e=Equal(e,e2)$)*;
    Sum/e -> Mul/e ( '\+' Mul/e2 $e=Add(e,e2)$ | '\-' Mul/e2 $e=Subtract(e,e2)$ )* ;
    Mul/e   -> StringIndex/e ( '\*' StringIndex/e2 $e=Multiply(e,e2)$
                      | '/'  StringIndex/e2     $e=Divide(e,e2)$  )*;
    StringIndex/e -> Atom/e ('\[' Exp/e2 '\]' $e=Index(e, e2)$)* | Atom/e;
    Atom/e  -> '\(' Exp/e '\)'
             | int/i  $e=Int(int(i))$
             | string/s $e=String(s)$;
    Index/e -> List/e ('\[' Exp/e2 '\]' $e=Index(e, e2)$)* | List/e;
    List/l  -> 
            '\['        $l = []
                (  Pick/e  $l.append(e)
                ( ','  Pick/e $l.append(e)
                )*
                )?
            '\]' $l=List(l)
            ;

    """
# This makes a parser object, which acts as a parsing function.
parser = Parser()


# Below is the driver code, which reads in lines, deals with errors, and
# prints the evaluation result if no error occurs.

# Open the input file, and read in lines of the file.
lines = open(sys.argv[1], 'r').readlines()

# For each line in the input file
for l in lines:
    # Uncomment the next line to help testing.  Comment it for submission.
    # print(l, end="")
    try:
        # Try to parse the expression.
        node = parser(l)
        # Try to evaluate the expression.
        result = node.eval()

        # Print the representation of the result.
        print(repr(result))

    # If an exception is rasied, print the appropriate error.
    except tpg.Error:
        print('Parsing Error')

        # Uncomment the next line to re-raise the parsing error,
        # displaying where the error occurs.  Comment it for submission.

        #raise

    except EvalError:
        print('Evaluation Error')

        # Uncomment the next line to re-raise the evaluation error, 
        # displaying where the error occurs.  Comment it for submission.

        # raise
