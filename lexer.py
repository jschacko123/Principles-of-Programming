import re # regular expressions

""" r means the start of the raw string and allows the use of backslash"""
""" b indicates word boundaries / identifiers seperated from other characters."""

# Define token patterns based on Clite grammar
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(int|bool|float|char|if|else|while|true|false)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),   # lower or upper case or underscore followed by lower or upper case or number 0 or more times.
    ('FLOAT', r'\b\d+\.\d+\b'),        # floating-point numbers
    ('INTEGER', r'\b\d+\b'),           # integers
    ('CHAR', r"\'[^\']\'"),            # single characters in single quotes
    ('BOOLEAN', r'\b(true|false)\b'),  
    ('OPERATOR', r'[+\-*/%]'),         # arithmetic operators
    ('ASSIGN', r'='),
    ('EQUAL', r'=='),
    ('NOT_EQUAL', r'!='),
    ('LESS_THAN', r'<'),
    ('GREATER_THAN', r'>'),
    ('LESS_EQUAL', r'<='),
    ('GREATER_EQUAL', r'>='),
    ('LOGICAL_OR', r'\|\|'),
    ('LOGICAL_AND', r'&&'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),               # Skip over spaces and tabs
    ('COMMENT', r'//.*'),              # Single-line comment
    ('MISMATCH', r'.'),                # Any other character
]

# Compile the token specification into a regular expression pattern
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
compiled_token_regex = re.compile(token_regex)

# Initialize a symbol table
symbol_table = {}
current_type = None  

def add_to_symbol_table(token, lexeme):
    """Adds identifiers to the symbol table with the detected type."""
    global current_type
    if token == 'KEYWORD' and lexeme in ['int', 'bool', 'float', 'char']:
        current_type = lexeme  # Set the current type for following identifiers
    elif token == 'IDENTIFIER' and current_type:
        if lexeme not in symbol_table:  # if not already in the symbol table
            symbol_table[lexeme] = {'type': current_type, 'scope': 'global'}
    elif token == 'SEMICOLON':
        current_type = None  # Reset the current type after the end of a declaration

def tokenize(code):
    """Tokenizes the code based on Clite grammar."""
    tokens = []
    line_num = 1
    for match in compiled_token_regex.finditer(code): 
        token_type = match.lastgroup
        lexeme = match.group(token_type)
        if token_type == 'NEWLINE':
            line_num += 1
        elif token_type == 'SKIP' or token_type == 'COMMENT':
            continue
        elif token_type == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {lexeme!r} on line {line_num}')
        else:
            tokens.append((token_type, lexeme))
            add_to_symbol_table(token_type, lexeme)
    return tokens

def write_symbol_table_to_file():
    """Writes the symbol table to a file named 'symbol_table.txt'."""
    with open('symbol_table.txt', 'w') as f:
        f.write("Identifier     Type     \n")
        f.write("------------------------------\n")
        for identifier, properties in symbol_table.items():
            f.write(f'{identifier:<14} {properties["type"]:<8}\n') # writing text to the file and aligning it

# Read from the sample input file
with open('sample_input.txt', 'r') as file:
    code = file.read()

# Tokenize the code
try:
    tokens = tokenize(code)
    print("Tokens and Lexemes:")
    for token, lexeme in tokens:
        print(f'{token:<12} {lexeme}')
    
    # Write symbol table to a file
    write_symbol_table_to_file()
    print("\nSymbol table has been written to 'symbol_table.txt'.")

except RuntimeError as e:
    print(e)
