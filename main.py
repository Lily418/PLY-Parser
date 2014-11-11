import os
import ply.lex as lex
import ply.yacc as yacc
import pydot


tokens = ('ID', 'INT', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'OPENPAREN', 'CLOSEPAREN')

t_ID         = r'[a-z]+'
t_PLUS       = r'\+'
t_MINUS      = r'\-'
t_MULTIPLY   = r'\*'
t_DIVIDE     = r'\/'
t_OPENPAREN  = r'\('
t_CLOSEPAREN = r'\)'

def t_INT(t):
    r'([1-9][0-9]*)|0'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Error at " + t.value[0])

t_ignore = ' '

counter = 0
def add_id(value):
    global counter
    counter += 1
    return {'id':counter, 'value':value}



def p_E_E_plus_T(t):
    'E : E PLUS T'
    t[0] = add_id(("+", t[1], t[3]))

def p_E_E_minus_T(t):
    'E : E MINUS T'
    t[0] = add_id(('-', t[1], t[3]))

def p_E_T(t):
    'E : T'
    t[0] = add_id(('E', t[1]))

def p_T_T_mul_F(t):
    'T : T MULTIPLY F'
    t[0] = add_id(('*',t[1], t[3]))

def p_T_T_div_F(t):
    'T : T DIVIDE F'
    t[0] = add_id(('/', t[1], t[3]))

def p_T_F(t):
    'T : F'
    t[0] = add_id(('T', t[1]))

def p_F_bracketed_expression(t):
    'F : OPENPAREN E CLOSEPAREN'
    t[0] = add_id(('F', t[2]))

def p_F_identifier(t):
    'F : ID'
    t[0] = add_id(('ID', t[1]))

def p_F_int(t):
    'F : INT'
    t[0] = add_id(('INT', t[1]))

def p_error(t):
    if t == None:
        print("Unexpected end of input")
    else:
        print("Syntax error at position: " + str(t.lexpos))

lex.lex()
yacc.yacc()

s = raw_input('Enter an expression: ')




tree = pydot.Dot(graph_name="Parse")
def draw_tree(yacc_output, parent_node):
    global tree
    symbol = yacc_output['value'][0]
    node_id = "id" + str(yacc_output['id'])

    if symbol in ["INT", "ID"]:
        node_label = node_id + " " + str(yacc_output['value'][1])
        tree.add_node(pydot.Node(node_label))
        if parent_node != None: tree.add_edge(pydot.Edge(node_label, parent_node))
    elif symbol in ["+", "-", "*", "/"]:
        node_label = node_id + " " + symbol
        tree.add_node(pydot.Node(node_label))
        draw_tree(yacc_output['value'][1], node_label)
        draw_tree(yacc_output['value'][2], node_label)
        if parent_node != None: tree.add_edge(pydot.Edge(node_label, parent_node))
    elif symbol in ['E', 'T', 'F']:
        #node_label = node_id + " " + symbol
        #tree.add_node(pydot.Node(node_label))
        draw_tree(yacc_output['value'][1], parent_node)
    else:
        raise Exception("No draw rule for " + symbol)

draw_tree(yacc.parse(s), None)

#tree.add_edge(pydot.Edge('123', '456'))
tree.write_png('graph.png')
os.system('open graph.png')
