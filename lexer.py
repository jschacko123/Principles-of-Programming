import re
import itertools

# Define token patterns
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(int|bool|float|char|if|else|while|true|false)\b'),
    ('PLUS', r'\+'), ('MINUS', r'-'), ('MULTIPLY', r'\*'), ('DIVIDE', r'/'),
    ('ASSIGN', r'='), ('EQUAL', r'=='), ('NOT_EQUAL', r'!='), ('LESS_THAN', r'<'),
    ('GREATER_THAN', r'>'), ('LESS_EQUAL', r'<='), ('GREATER_EQUAL', r'>='),
    ('LOGICAL_AND', r'&&'), ('LOGICAL_OR', r'\|\|'), ('NOT', r'!'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'), ('FLOAT', r'\b\d+\.\d+\b'),
    ('INTEGER', r'\b\d+\b'), ('CHAR', r"\'[^\']\'"), ('BOOLEAN', r'\b(true|false)\b'),
    ('LPAREN', r'\('), ('RPAREN', r'\)'), 
    ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('LBRACKET', r'\['), ('RBRACKET', r'\]'),  # Ensure both brackets are here
    ('SEMICOLON', r';'), ('COMMA', r','),
    ('NEWLINE', r'\n'), ('SKIP', r'[ \t]+'), ('MISMATCH', r'.')
]

compiled_token_regex = re.compile('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION))
symbol_table = []
current_type = None
scope_stack = ['Global']  # Start with global scope


def default_value(data_type):
    return {'int': '0', 'float': '0.0', 'bool': 'false', 'char': "''"}.get(data_type, "0")

def add_to_symbol_table(lexeme, token_class, symbol_type, data_type=None, value=None, scope='Global'):
    symbol_table.append({
        'lexeme': lexeme,
        'token_class': token_class,
        'symbol_type': symbol_type,
        'data_type': data_type if data_type else "None",
        'value': value if value is not None else "0",
        'scope': scope,  # Use the passed scope
    })


# Initialize the scope stack with 'Global' as the default scope
scope_stack = ['Global']

def process_token(token_type, lexeme):
    global current_type

    if token_type == 'KEYWORD' and lexeme == 'main':
        current_type = lexeme
        add_to_symbol_table(lexeme, 'TokKeyword', 'Keyword', None, "0", scope_stack[-1])
        
    elif token_type == 'KEYWORD':
        # Use current scope from the stack (Global or Local as appropriate)
        scope = scope_stack[-1]
        current_type = lexeme
        add_to_symbol_table(lexeme, 'TokKeyword', 'Keyword', None, "0", scope)

    elif token_type == 'IDENTIFIER':
        # Use the current scope for identifiers based on `scope_stack`
        scope = scope_stack[-1]
        data_type = current_type if current_type else None
        add_to_symbol_table(lexeme, 'TokIdentifier', 'Variable', data_type, "0", scope)
        current_type = None  # Reset type

    elif token_type == 'ASSIGN':
        # Use current scope for assignment operators
        scope = scope_stack[-1]
        add_to_symbol_table(lexeme, 'TokAssign', 'Operator', None, "0", scope)

    elif token_type in ['INTEGER', 'FLOAT', 'CHAR', 'BOOLEAN']:
        # Use current scope for literals
        scope = scope_stack[-1]
        data_type = token_type.lower()
        add_to_symbol_table(lexeme, 'Tok' + token_type.capitalize(), 'Literal', data_type, lexeme, scope)

    elif token_type == 'LBRACE':
        # Enter a new Local scope when `{` is encountered
        scope_stack.append('Local')

        # Add the brace to the symbol table with the current scope
        add_to_symbol_table(lexeme, 'TokLbrace', 'Symbol', None, "0", scope_stack[-1])

    elif token_type == 'RBRACE':
        # Exit the current Local scope when `}` is encountered, if not in the global scope
        if len(scope_stack) > 1:
            scope_stack.pop()

        # Add the brace to the symbol table with the current scope
        add_to_symbol_table(lexeme, 'TokRbrace', 'Symbol', None, "0", scope_stack[-1])

    elif token_type in ['LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON']:
        # Handle other symbols like parentheses, brackets, comma, and semicolon
        scope = scope_stack[-1]
        add_to_symbol_table(lexeme, 'Tok' + token_type.capitalize(), 'Symbol', None, "0", scope)

    else:
        # Default case for other symbols
        scope = scope_stack[-1]
        add_to_symbol_table(lexeme, 'Tok' + token_type.capitalize(), 'Symbol', None, "0", scope)



def peek_next_token(iterator):
    iterator, peek_iter = itertools.tee(iterator)
    try:
        return next(peek_iter).lastgroup
    except StopIteration:
        return None

def get_assigned_value(iterator):
    value = []
    try:
        while True:
            next_match = next(iterator)
            if next_match.lastgroup == 'SEMICOLON':
                break
            value.append(next_match.group(next_match.lastgroup))
    except StopIteration:
        pass
    return ' '.join(value)

def remove_comments(code):
    lines = code.splitlines()
    return '\n'.join(line.split('//')[0] for line in lines)

def tokenize(code):
    tokens = []
    iterator = compiled_token_regex.finditer(code)
    for match in iterator:
        token_type = match.lastgroup
        lexeme = match.group(token_type)
        if token_type == 'NEWLINE' or token_type == 'SKIP':
            continue
        elif token_type == 'MISMATCH':
            print(f"Warning: Unexpected character {lexeme!r}")
        else:
            tokens.append((token_type, lexeme))
            process_token(token_type, lexeme)  # Process every token without advancing iterator here
    return tokens


def write_symbol_table_to_file():
    with open('symbol_table.txt', 'a') as f:  # Use 'a' mode for appending
        f.write("Lexeme         Token Class     Symbol Type     Data Type     Value    Scope\n")
        f.write("--------------------------------------------------------------------------\n")
        for entry in symbol_table:
            data_type = entry["data_type"] if entry["data_type"] is not None else "None"
            value = entry["value"] if entry["value"] is not None else "0"
            f.write(f'{entry["lexeme"]:<14} {entry["token_class"]:<14} {entry["symbol_type"]:<14} '
                    f'{data_type:<12} {value:<8} {entry["scope"]:<8}\n')
        f.write("\n")  # Add a newline for separation between runs


# Read and clean code by removing comments
with open('sample_input.txt', 'r') as file:
    code = file.read()

code = remove_comments(code)

try:
    tokenize(code)
    write_symbol_table_to_file()
    print("\nSymbol table has been written to 'symbol_table.txt'.")
except RuntimeError as e:
    print(e)
