import ox
import click
import pprint

lexer_tokens = [
    'NUMBER',
    'DO',
    'PRINT',
    'ADD',
    'LOOP',
    'L_PAR',
    'R_PAR',
    'DO_BEFORE',
    'DO_AFTER',
    'INC',
    'DEC',
    'READ',
    'RIGHT',
    'LEFT',
    'SUB',
    'COMMENT',
    'BREAK_LINE',
    'SPACE',
]

lexer_rules = ox.make_lexer([
    ('NUMBER', r'[0-9]+'),
    ('DO', r'do'),
    ('PRINT', r'print'),
    ('ADD', r'add'),
    ('LOOP', r'loop'),
    ('L_PAR', r'\('),
    ('R_PAR', r'\)'),
    ('DO_BEFORE', r'do-before'),
    ('DO_AFTER', r'do-after'),
    ('INC', r'inc'),
    ('DEC', r'dec'),
    ('READ', r'read'),
    ('RIGHT', r'right'),
    ('LEFT', r'left'),
    ('SUB', r'sub'),
    ('ignore_COMMENT', r';[^\n]*'),
    ('ignore_BREAK_LINE', r'\n'),
    ('ignore_SPACE', r'\s+'),
])
parser_rules = [
    ('expr : L_PAR R_PAR', lambda x, y: '()'),
    ('expr : L_PAR term R_PAR', lambda x, y, z: y),
    ('term : atom term', lambda x, y: (x,) + y),
    ('term : atom', lambda x:(x,)),
    ('atom : expr', lambda x:x),
    ('atom : DEC', lambda x:x),
    ('atom : INC', lambda x:x),
    ('atom : LOOP', lambda x:x),
    ('atom : RIGHT', lambda x:x),
    ('atom : LEFT', lambda x:x),
    ('atom : PRINT', lambda x:x),
    ('atom : READ', lambda x:x),
    ('atom : DO', lambda x:x),
    ('atom : DO_AFTER', lambda x:x),
    ('atom : DO_BEFORE', lambda x:x),
    ('atom : ADD', lambda x:x),
    ('atom : SUB', lambda x:x),
    ('atom : NUMBER', int),
]

parser = ox.make_parser(parser_rules, lexer_tokens)


def do_after(op, source):

    array = []
    index = 0
    array_size = len(source)

    while index < array_size:
        if source[index] == 'add' or source[index] == 'sub':
            array.append(source[index])
            index += 1

        array.append(source[index])
        array.append(op)

        index += 1

    return array


def do_before(op, source):

    array = []
    index = 0
    array_size = len(source)

    while index < size:
        array.append(op)
        array.append(source[index])

        if source[index] == 'add' or source[index] == 'sub':
            index += 1
            array.append(source[index])

        index += 1

    return array


def interpreter(ast, source, position):
    in_loop = False
    index = 0

    while index < len(ast):

        if isinstance(ast[index], tuple):
            source, position = interpreter(
                ast[index], source, position)

        elif ast[index] == 'do-before':
            index += 1
            op = ast[index]
            index += 1
            array = do_before(op, list(ast[index]))
            interpreter(array, source, position)

        elif ast[index] == 'do-after':
            index += 1
            op = ast[index]
            index += 1
            array = do_after(op, list(ast[index]))
            interpreter(array, source, position)

        elif ast[index] == 'inc':
            source[position] += 1

        elif ast[index] == 'dec':
            source[position] -= 1

        elif ast[index] == 'right':
            position += 1
            if len(source) - 1 < position:
                source.append(0)

        elif ast[index] == 'left':
            position -= 1
            if position < 0:
                source.append(0)

        elif ast[index] == 'add':
            index += 1
            source[position] += ast[index]

        elif ast[index] == 'sub':
            index += 1
            source[position] -= ast[index]

        elif ast[index] == 'print':
            print('')
            print(chr(source[position]), end='')

        elif ast[index] == 'read':
            source[position] = input()

        elif ast[index] == 'loop':
            if source[position] == 0:
                in_loop = False
                break
            else:
                in_loop = True

        # Run again
        if in_loop is True and index == len(ast) - 1:
            index = -1

        index += 1

    return source, position

def evaluator(ast):
    array = [0]
    position = 0
    array, position = interpreter(ast, array, position)

@click.command()
@click.argument('lispf_ck_file', type=click.File('r'))

def run(lispf_ck_file):
    source = lispf_ck_file.read()
    tokens = lexer_rules(source)
    print('')
    print('List of tokens: \n\n', tokens)
    print('')
    tree = parser(tokens)
    print('\nSyntax Tree:')
    print('')
    pprint.pprint(tree)
    evaluator(tree)
    print('')


if __name__ == '__main__':
    run()
