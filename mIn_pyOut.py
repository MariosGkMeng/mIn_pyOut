# =================================================================================
# =================================================================================
#
# Version 2 (Created in 10.2021 by Marios Gkionis)
#   Differences with previous version: This one uses decorators
# NOTES: 
# 
# Solving code problems: 
#   - search for "PROBLEM i", i=number of the problem. 
#   - search for word "weakness" --> when solved, delete the word "weakness"
# 
# TODO: 
# # TODO! FROM PREVIOUS TIME. get word before parenthesis (SEARCH THIS EXACT TEXT: "get word before parenthesis")
# 1. Solve problem 5
# 2. SEARCH "PROBLEM 1"
#
#
# List of bugs-problems-things that can be optimized
# =================> Test script "plant_model_1.m". Has many mistakes! <=======================
# 1. ✔ Add exception for index that is looped starting from 0 and do not add "-1"
#   b. TODO Avoid confusion (sometimes that index is not looped, but user-set)
# 2. CORR: Conditional operations with <>=. DO they need change in indexing?
# 3. CORR: Changing vectors ("[a b c] to [a,b,c]" does not work for all cases!)
# 4. CORR: deal with nested vectors 
#           |
#           ---> remove PATCH. 1 after that
# 5. CORR: Broken lines that are fixed again have problems
# 6. CORR: Separate list of functions that are true for every script from script-dependent functions
# 7. CORR: "zeros" functions cannot have two arguments!!
# 8. ✔ Sometimes MATLAB comment lines miss the "\n" at the end of the line
#       They seem to loose it when handling the switch-case statement
# 9. ✔ command: "is_for_loop = ln1.startswith(loopSyntax)" is incorrect!
# 10. CORR: switch-case statement in plant_model_1.py has indentation problem
# 11. CORR: decoding problem for "RUN_SIMULATION.m"
# 12. ✔ in Sec. 2: Identation problem for ln1 and ln2!
#     |__ Solved by identifying any potential identation on the existing line
# 13. ✔ In Sec. 7, expressions such as "aa==max" are taken as a single variable!
#     |__ Solved by adding "=" to list of math operators
# 14. ✔  "[i for i in x]" operations are inserted in vector transformations!!
# 15. ✔ MATLAB lines that are not separated by line break don't have their ";" end removed!
# 16. CORR: Variables need to be defined in Python!
# 17. CORR: Problem in Sec. 7: 
#           |__ 'f_get_Q_r_i = @(Ux)(sum(Ux(d.i_U_fQr)));' ---mat2py---> sum(Ux[d['i_U_fQr'] - 1] 1](sum(Ux(d['i_U_fQr'])))
#           |__ 'f_get_Q_r_i =(sum(Ux(d.i_U_fQr)));' is correctly converted!
# 18. CORR: 'GHG_CASADI_new_check_units' has many mistakes 
# 19. CORR: When MATLAB line doesn't end with ";", it is not treated as a full line and is merged with the next!! 
# 20. OPT: get_word_before_par ---> perhaps can make it more efficient via regex
# 21. ✔ get_word_before_par: does not recognise existence of dict
#     |__ SOLVED: by regex search  
# 22. ✔ in Sec. 4: when I declear a dict variable, I have to be carefull not to declare it inside broken lines!
# 23. CORR: a variable with name "norm__something" is replaced with "np.norm__something"
# 24. CORR: Confusion of %f.%f for f['f'], wherein by "%f" we mean "int"
# 25. CORR: Sec. 7, convMode = 1: "e = (z - theta(:, n)'*phi)": theta(:, n) not converted, but when line is: 
#                                 "e = z - theta(:, n)'*phi", then theta(:, n) is converted correctly
# 26. DEV: Sec. 15: convert slice to linspace --> check example at beginning of "playground". Solved most of it,
#       but have to exclude the case of the slice being inside a variable. 
#                  
# =================================================================================
# =================================================================================

from itertools import cycle
import numpy as np
import re
from numpy.lib.arraysetops import unique
from my_array import my_array
from get_scaled_time import get_scaled_time
from findOccurrences import findOccurrences
# import tkinter
vec = lambda x: np.array(x)    

for i in range(15): print("      ")


# UNDER DEVELOPMENT: Define decorator that prints erratically converted lines:
def check_if_erratic_conversion(func):

    def wrapper(*args, **kwargs):

        # funLst = ['get_vector_elements']
        funNm = func.__name__
        # print(funNm)
        
        # print(wrapper.calls)
        wrapper.error_msg = ''
        
        if funNm == 'get_vector_elements':
            wrapper.calls += 1
            c_in = args[0]
            cond1 = c_in.count('[') == 1
            cond2 = c_in.count(']') == 1
            no_nested_vec = cond1 and cond2
            if not no_nested_vec:
                # wrapper.error_msg = 'Line with type of weakness: 1'
                wrapper.error_msg = ''
            result = func(*args, **kwargs)

        elif funNm == 'store_line':
            result = func(*args, **kwargs)
            get_vector_elements.error_msg = ''
            wrapper.error_msg = ''

        return result 

    wrapper.error_msg = ''
    wrapper.calls = 0

    return wrapper

class parenthesis_cls():
    # A class, in which one can extract:
    #   1. Contents between parentheses and brackets
    #   2. Contents before and after parentheses and brackets

    y = []


    def get_word_before_par(self, s_in, lst_operators, idx0):
        # get a word before the beginning of a parenthesis


        # recognise dict variable
        # \==================================================
        
        patt = r"[\['\w+'\]+]*"
        
        # patt = r"\w+\['\w+'\]" # (word, followed by word in "['']") 
        lstDicts = re.findall(patt, s_in)
        lstDicts = [x for x in lstDicts if len(x)>0]
        lstDicts = [x for x in lstDicts if "['" in x]
        lstDicts_converted = []
        for l in lstDicts:
            l_conv = l.replace("['", '__').replace("']", '')
            lstDicts_converted.append(l_conv)
            s_in = s_in.replace(l, l_conv)
        
        # \==================================================

        word_before_par = ''
        if not ('#' in s_in): # non commented line
            p11 = []
            for ltr in lst_operators:
                xx = findOccurrences(s_in, ltr)       
                idx = xx.y
                if  (len(idx) > 0): p11.append(idx[-1])
            if len(p11) > 0:
                p1 = max(p11)
            else:
                p1 = -1  
            
            
            if  str(idx0) == idx0:
                word_before_par = s_in[p1+1:]
            else:
                if p1+1>idx0:      
                    word_before_par = s_in[p1+1:] 
                else:
                    word_before_par = s_in[p1+1:idx0] 
        
        word_before_par = word_before_par.replace(' ', '')
        
        for iL, l in enumerate(lstDicts):
            word_before_par = word_before_par.replace(lstDicts_converted[iL], l)
                
        # return word_before_par
        
        self.y.append(word_before_par)
        self.word_before_par = word_before_par

    def get_par_content(self, ln1, idx0, i_pr, ln_after_par,\
         word_before_par, list_py_funcs, par_type):
        
        par_type_open = par_type
        if par_type_open == '(': par_type_cl = ')'
        if par_type_open == '{': par_type_cl = '}'
        if par_type_open == '[': par_type_cl = ']'

        idx00 = 0
        par_content = ''
        txt_after_par_closed = ''
        jj = 0
        cnd1 = not (word_before_par in list_py_funcs)
        if cnd1:
            for jj in range(len(ln_after_par)):
                ln11 = ln_after_par[idx00:idx00+jj+1]
                # print(ln11)
                num_parenthesis_open = ln11.count(par_type_open) + 1
                num_parenthesis_close = ln11.count(par_type_cl) 
                if (num_parenthesis_open - num_parenthesis_close)==0:
                    # parenthesis closed
                    break
            par_content = ln_after_par[idx00:idx00+jj]
        self.par_content = par_content
        # txt_after_par_closed = ln1[idx0+jj+(i_pr-1)+2:]
        if jj > 0: txt_after_par_closed = ln1[(idx0+1)+(jj+1):]
        self.txt_after_par_closed = txt_after_par_closed

    def change_slice_content(self, par_content, had_comma, exception_indexes):

        if had_comma == 1:
            dum0 = ' - 1'
            dum1 = ''
            dum12 = ''
            dum22 = ''
        else:
            dum0 = ''
            dum1 = ' - 1'
            dum12 = ' - 1'
            dum22 = ' - 1'

        if (':' in par_content) and (had_comma == 0): 
            had_slice = 1
            idx_slice = par_content.find(':')    
            before_slice = par_content[:idx_slice]# + dum1
            after_slice = par_content[idx_slice+1:]# + dum1
            

            if 'end' in before_slice: 
                before_slice = before_slice.replace('end', '')    
                dum12 = ''
            if 'end' in after_slice: 
                after_slice = after_slice.replace('end', '')    
                dum22 = ''
                
            if len(before_slice.replace(' ', ''))==0: 
                dum12 = ''
            if len(after_slice.replace(' ', ''))==0: 
                dum22 = ''

            dumv1 = before_slice.split() # split based on blanks
            for ch in dumv1:
                if (ch in exception_indexes):
                    dum0 = ''
                    dum1 = ''      
                    break             

            slice_content = before_slice + dum12 + ':' +  after_slice + dum22 + dum0
        else:
            slice_content = par_content
            had_slice = 0
            
        self.slice_content = slice_content
        # print(slice_content)
        self.had_slice = had_slice

# def split(word, lst):
#     spl_word = []
#     for char in word:
#         if not (char in lst):
#             spl_word.append(char)

#     return spl_word
@check_if_erratic_conversion
def get_vector_elements(c_in):
    # Identifies if the current line contains a vector assignment 
    # and then converts to Python syntax
    # If it is a Matrix, then the conversion is handled inside the script


    # List of math operations to NOT be confused with vector elements
    lst_operators = ['+', '-', '*', '/', '^']
    

    # Weakness - Start: nested vectors ================================================
    # ==================================================================================
    #  ✔ Does not work on assignments such as
    #       - d['field'] = [1;2;3]
    #       - h = [d['field'];2;3] 
    # cond1 and cond2 are only here for now, so that we do not deal with nested vectors !
    cond1 = c_in.count('[') == 1
    cond2 = c_in.count(']') == 1
    no_nested_vec = cond1 and cond2
    # ==================================================================================
    # Weakness - end: nested vectors ==================================================

    ln_args = []
    inhalt_urspr = ''
    inhalt = ''
    is_matrix = False
    if no_nested_vec:
        pos1 = c_in.find('[')+1
        pos2 = c_in.find(']')
        inhalt = c_in[pos1:pos2] # get content from: "[content]" 
        inhalt_urspr = inhalt

        # replace spaces only before and after the operators 
        # (not all spaces obviously)
        for op in lst_operators:
            op0r = ' ' + op
            op0l = op + ' '
            inhalt = inhalt.replace(op0r, op)
            inhalt = inhalt.replace(op0l, op)

        # Identify if is matlab matrix ===============================================
        n_q = c_in.count(';')
        
        inhalt = inhalt.replace(',', ' ')
        inhalt0 = inhalt
        inhalt0 = inhalt0.replace(';', ' ')
        ln_args0 = inhalt0.split()
        is_matrix = len(ln_args0)-1 > n_q
        # ============================================================================

        if is_matrix:
            inhalt = inhalt.replace(';', '], [')
            # # Replace '\n' and '\\' =====================================================
            # inhalt = inhalt.replace('\n', 'new_line')
            # inhalt = inhalt.replace('\\', 'line_break')
            # # ===========================================================================
            inhalt = '[' + inhalt + ']'
        else:
            inhalt = inhalt.replace(';', ' ')
        ln_args = inhalt.split()
    return ln_args, inhalt_urspr, is_matrix, inhalt

def extract_from_line_breaks(c_in):
    # merge line breaks into one line
    # HINTS:
    #  - By "broken_lines", we refer to the signular command line that has been broken
    #    into multiple ones, due to its length


    # Loop through lines
    # \==================================================    
    for z, ch in enumerate(c_in):
        if ch.endswith("\n"):
            ch = ch[:-2].replace(' ', '')
            if not ch.endswith('\\'):
                break
    # \==================================================        
    
    ln = ''       
    n_dum = 4   
    if z>0:
        broken_lines = c_in[:z+1]
        for i_ln, ch in enumerate(broken_lines):
            if i_ln > 0:
                if ch.startswith(n_dum*' '): # do not "shift-tab" if there is text
                    ch = ch[n_dum:]
            ch = ch.replace('\n', '')
            ch = ch.replace('\\', '')    
            ln += ch

        ln += '\n'  
    return ln, z

@check_if_erratic_conversion
def store_line(Ln1, ln1, err_msg_4user, lnIdx):
    # store modified line 
    if err_msg_4user:
        ln1 = ln1.replace('\n', '')
        ln1 += ' # ' + err_msg_4user + '\n'

    if lnIdx == -1:
        Ln1.append(ln1)
    elif lnIdx >= 0:
        Ln1.insert(lnIdx+1, ln1)
    elif lnIdx == -np.inf:
        Ln1.insert(0, ln1)
    else:
        raise('Nothing coded for this case')
    
    get_vector_elements.error_msg = ''
    return Ln1

def is_broken_line(ln):
    lnbr = re.findall(r"[\\][\s]*\n$", ln)
    y = len(lnbr)>0
    return y


def change_struct(l, LIST):
    
    l = l.replace('\n','')
    
    lst = LIST['operators'] + LIST['special_chars']
    delimiters = tuple([x for x in lst if x!='.'])
    regex_pattern = '|'.join(map(re.escape, delimiters))

    l1 = re.split(regex_pattern, l)
    l1 = [x for x in l1 if len(x)>0]
    lcp = l
    lines_new_dicts = ''
    quick_exclusion_condition = (not '.' in  l)
    
    
    if not quick_exclusion_condition:
    
        new_dicts_to_declare = []
        for l1i in l1:
            l1is = l1i.split('.')
            l1is = [x for x in l1is if len(x)>0]
            if len(l1is) > 1:
                
                x_bad = [x for x in l1is if not x[0].isalpha()]
                
                if len(x_bad) == 0:
                
                    
                    # print(x_bad)
                    ln1s_transformed = l1is[0]
                    new_dicts_to_declare.append(l1is[0])
                    ln1s_transformed += ''.join(["['" + x + "']" for x in l1is[1:]])
                    
                    lcp = lcp.replace(l1i, ln1s_transformed)


        lines_new_dicts = ''.join([x+' = dict() \n' for x in new_dicts_to_declare if not x in LIST['declared_dicts']])
        LIST['declared_dicts'] += new_dicts_to_declare
    # LIST['declared_dicts'] = unique(LIST['declared_dicts'])
    return LIST, lines_new_dicts + lcp+' \n'

def print_dict_beautifully(d, lvl):
    # Prints dictionary in the bulleted list form:
    # Example:
    #   d['Food']['Fruits']['I_like'] = ['Apples', 'Oranges']
    #   d['Food']['Fruits']['I_not_like'] = ['Grapefruits', 'Mandarine']
    #   print_dict_beautifully(d)
    #
    #   Console:
    #       d:
    #           - Food
    #               - Fruits
    #                   - I_like 
    #                       - ['Apples', 'Oranges'] 
    #                   - I_not_like
    #                       - ['Grapefruits', 'Mandarine']
    
    key_lvl = []
    i = 0
    dc = d
    LinesPrint = []
    str_align = '|'
    
    
    
    if isinstance(dc, dict):
        # key_lvl.append(list(dc.keys()))
        keys = list(dc.keys())
        
        dn = dict('')
        for kk in keys:
            LinesPrint.append(4*lvl*' ' + str_align + kk)
            LinesPrint.append(4*lvl*' ' + str_align + '-'*len(kk))
            dn = dc[kk]
            # print(lvl+1)
            LinesPrint_1 = print_dict_beautifully(dn, lvl+1) 
            LinesPrint += LinesPrint_1


    elif isinstance(dc, list):
        
        for kk in dc:
            if isinstance(kk, list):
                # K = ''
                # for kkk in kk:
                #     K += kkk + ' '
                # LinesPrint.append(4*lvl*' ' + K)
                
                LinesPrint.append(4*lvl*' ' + str_align + str(kk))
                
            else:
                LinesPrint.append(4*lvl*' ' + str_align + kk)

        LinesPrint.append(4*lvl*' ' + str_align)

    elif isinstance(dc, str):
        LinesPrint.append(4*lvl*' ' + str_align + dc)
        LinesPrint.append(4*lvl*' ' + str_align)
    else:
        raise('NOTHING CODED HERE')

    
    return LinesPrint    
           
        # dc = dn    
        # i+=1
        
def remove_group(s, group):
    for g in group:
        s = s.replace(g, '')
        
    return s
    
# Helper functions =================================================================

enum = lambda x: enumerate(x)


# ===================================================================================

# Read the .m file ===============================================================
filePath = 'C:\\Users\\mario\\Downloads' #'C:\\Users\\mario\\Dropbox\\migration'
# Add the matlab files (without the extension) below. You can add more than one
# In case you want to convert only one file, please keep the matFileNms as a list object
matFileNms = ['assignment4_sol']   
# ================================================================================

# Direct text substitutions (that do NOT contain '.') =================================================
# init_text final_text position_mode
# list_mat_py_funcs = [\
# List of MATLAB functions, so that the function names are not treated as variable names
LIST = dict()
LIST['functions'] = [\
    'zeros', 'ones', 'get_scaled_time', 'range',\
    'reshape', 'polyval', 'len', 'length', 'eval',\
    'exec', 'error', 'print', 'disp', 'warning', 'any', 'all',\
    'obstacle_generator', 'IPOPT_SOLVE', 'exist', \
    'ipopt_initial_condition', 'switch_controller_mode',\
    'targetStatesInputs', 'full', 'isfield', 'abs',\
    'find', 'size', 'sin', 'cos', 'num2str', 'str',\
    'make_signals_continuous', 'strcmp', 'min',\
    'max', 'norm', 'eval_g', 'reshape', 'tan', 'plant_model',\
    'update_problem_CASADI', 'jacobian', 'vertcat', 'Function',\
    'enumerate', 'ctr_memory', 'distance_from_obstacle', 'dict', 'tf2ss', 'save']
# ==================================================================================================

# List of operators
LIST['operators'] = [' ', '+', '-', '*', '/', ':', ';',\
                 '.', ',', '(', ')', '[', ']', "'", '=', 'or', 'and',\
                 '>', '>=', '<', '<=', '==', 'if', 'for', 'not']

# not sure why I did not have it in advance, but:
LIST['operators'].append('^')


LIST['operators_double_whitespace'] = ['+', '-', '*', '/', ':',\
                '=', 'or', 'and', '>', '>=', '<', '<=', '==', 'not']

LIST['operators_at_right_whitespace'] = ['if', 'for']

LIST['special_chars'] = ['#']

LIST['declared_dicts'] = [] # Dictionary variables decleared while converting structs to dicts (see corresponding section)

 #['function ',   '#function ',        'any',         'below'] ,\
# , 'below' ['~=',          '!=',                'any'],\


# Explicit text substitutions ===========================================================
# =======================================================================================
# ⚠ NOTE: comment symbols should always be the first to be replaced!
#   [char0,         char_replace,        type_of_replacement]
#     The parameter type_of_replacement can get the following values:
#     ---------------------------------------------------------------------- 
#     |      Value | Meaning                                           |
#     | ----------:|:------------------------------------------------- |
#     |      'any' | Replace char in any position of the line          |
#     |      'end' | Replace char if it's at the end of the line       |
#     |    'start' | Replace char if it's at the beginning of the line |
#     | 'function' | Replace char as a function                        |
#     |            |                                                   |
# 👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼👇🏼
MAP_txt_subst = [\
    ['%',           '#',                 'any'] ,\
    [' ;',          '',                  'end'] ,\
    [';',           '',                  'end'] ,\
    ['...',         '\\',                'any'],\
    ['end',         '# end',             'start' ] ,\
    ['clc',         '# clc',             'start' ],\
    ['clear',       '# clear',           'start' ],\
    ['elseif',      'elif',              'any'] ,\
    ['else',        'else:',             'any'] ,\
    ['length',      'len',               'function'],\
    ['eval',        'exec',              'function'],\
    ['~=',          '!=',                'any'],\
    ['~',           'not ',              'any'],\
    ['clear',       '# clear',           'any'],\
    ['len',         'len',               'function'],\
    ['switch ',     'var_sw_cs = ',      'any'],\
    ['case ',       'elif var_sw_cs ==', 'any',       'case'],\
    ['otherwise',   ' else:',             'start'],\
    ['&&',          'and',               'any'],\
    ['||',          'or',                'any'],\
    ['disp',        'print',             'function'],\
    ['num2str',     'str',               'function'],\
    ['true',        'True',              'any'],\
    ['false',       'False',             'any']] 

# =======================================================================================
# =======================================================================================

# Substitutions that need "np."
txt_subst_dot = [\
    ['zeros(',   'np.zeros('] ,\
    ['ones(',    'np.ones('] ,\
    ['polyval(', 'np.polyva(l'],\
    ['reshape(', 'np.reshape('],\
    ['&',       'and'] ,\
    ['cos(',    'np.cos('],\
    ['sin(',    'np.sin('],\
    ['size(',    'np.shape('],\
    ['norm(',    'np.norm('],\
    ['tan(',    'np.tan('],\
    ['diag(',   'np.diag(']]

str_ends_with = [['[', 'ends'],\
                [']', 'is'],\
                ['],', 'ends']]

# Modules to load in the converted file =====================================================================================
modules2load = [\
    'import numpy as np',\
    'vec = lambda x: np.array(x)',\
    'import re',\
    'from get_scaled_time import get_scaled_time',\
    'from numpy.lib.arraysetops import unique',\
    'for i in range(15): print("      ")']
# ========================================================================================================================

loopSyntax = 'for '
inRngCmd = 'in range('
# myTab = '\t'[0:-1]
special_functions =[\
    ['strcmp', '(a,b)', 'a==b']
    ]




is_playtime = False
if is_playtime:
    # # PLAYGROUND \==================================================
    # # \==================================================
    
    
    
    
    #  Sec. 15: convert slice to linspace ============================================================
    
    l = " x= g(10:h)+ 5:h"
    
    popo = re.findall(\
        r"[ =+]\w+:\w+:\w+",\
        l)
    
    crs = [' ','=','+','-']
    patt = '[' + ''.join(crs) + ']' + "*\w+:\w+"
    popo = re.findall(\
        patt,\
        l)   
    
    popo = [remove_group(x, crs) for x in popo]
    
    for pp in popo:
        nums = pp.split(':')
        lpp = 'np.linspace(' + nums[0] + ', ' + nums[1]
        if len(nums) == 3:
           lpp += ', ' * nums[2]
           
        lpp += ')'
    
        l = l.replace(pp, lpp)
    print(l)
    
    
    # ===============================================================================================

    
    
    # Find pattern for programming variable
    
    patt1 = r"[a-z, A-Z, 0-9,_]*"
    patt1 = r"[\ba-z, A-Z,\_,0-9]+"
    wrd = "d.Var1.1per_1=1"
    patt1 = r"\b[a-zA-Z]\w*"
    popo = re.findall(patt1, wrd)
    # print(popo)
    print('')
    
    
    wrd = " d.Var1.per_1.per2=1"
    patt = r"\b[a-zA-Z]\w*[\.[a-zA-Z]\w*]*"
    
    popo = re.findall(\
        r"^[a-zA-Z]\w*[\.[a-zA-Z]\w*]*",\
        "d1.Var1.per_1.per2=1")
    
    print(popo)

    
    #
  
    
    lstp = ['a', 'c', 'd', 'e']
    
    lstp.insert(0+1, 'b')
    print(lstp)
    
    i=0
    perp = i^2+\
        5
    print('')
    # wrd = " This is a dd1s['special'] word yall "

    # patt1 = r"\w+\['\w+'\]"
    # popo = re.findall(patt1, wrd)

    # print('')

    # patt = r"\w+(\.\w+)*" # (word, followed by word in "['']")
    # patt1 = r"[\.\w+]*"
    # wrd = 'd.fld.pip'
    # popo = re.findall(patt1, 'x = d.fld1.fld2')
    # print(popo)
    # x_dot = d.init_cond(4);


    wrds = [[   'x = y(idx(1+2^4):idx(11+2^4))', 'simple numerical indexing'],\
            [                      'd = dict()', 'python function'],\
            ['d = y(15 + isfield(p, "zombie"))', 'combination of: python function and numerical indexing']    ]
    parenthesis_counter = []

    for W in wrds:
        wrd = W[0]
        pMode = 2
        if pMode == 1:
            wrd = wrd.replace('(',' [ ').replace(')',' ] ').replace(':', ' : ')
            patt1 = r"[a-z,0-9,\+,\-,\/,\*,\^,=,\[,\],\:]*"
        elif pMode == 2:
            wrd = wrd.replace('(',' ( ').replace(')',' ) ').replace(':', ' : ')
            patt1 = r"[a-z,0-9,\+,\-,\/,\*,\^,=,\(,\),\:]*"
            
        patt2 = r"[(,)]*"
        popo = re.findall(patt1, wrd)
        popo = [x for x in popo if len(x)>0]
        print(popo)
        L = ''
        p0 = ''
        for p in popo:
            
            if '(' in p:
                parenthesis_counter = [[x[0]+1, x[1]] for x in parenthesis_counter]
            elif ')' in p:
                parenthesis_counter = [[x[0]-1, x[1]] for x in parenthesis_counter]
                xlast = parenthesis_counter[-1]
                if xlast[0]==0:
                    # parenthesis closed
                    if xlast[1]==0: 
                        p = p.replace(')', ']')
                    parenthesis_counter = parenthesis_counter[:-1]
                        
            
            if not p0 in LIST['functions']:
                if '(' in p: parenthesis_counter.append([1, 0])
                pNew = p.replace('(', '[-1+').replace(':', ':-1+') #.replace(')', ']')
            else:
                if '(' in p: parenthesis_counter.append([1, 1])
                pNew = p
            L += pNew
            p0=p
            
        # popo = re.findall(patt2, wrd)
        print(W[1]+': ')
        print(L)
        print('===============================\n')

    wrd = 'd = dict()'
    parenthesis_counter = []
    for W in wrds:
        wrd = W[0]
        popo = re.findall(r"[a-z, A-Z]\w*\(", wrd)
        # print(popo)
        L = ''
        p0 = ''
        for p in enum:
            if not p0 in LIST['functions']:
                L += p.replace('[', '[-1+').replace(':', ':-1+')
            else:
                # parenthesis_counter = [x for x in parenthesis_counter x+1]
                    
                
                
                parenthesis_counter.append([1, 1])
            p0 = p
            
        # popo = re.findall(patt2, wrd)
        print(W[1]+': ')
        print(L)
        print('\n')

    # TODO! FROM PREVIOUS TIME. get word before parenthesis
    txt = "y(isfield(d,d))"
    x = re.findall(r"[a-z, A-Z]\w*\(", txt)
    print(x)
##

# patt = dict()
# patt['pre_parenthesis'] = r"^\w,\w,\("
# popo = re.findall(patt['pre_parenthesis'], wrd)

# # \==================================================


for matFileNm in matFileNms:
    # Loop through all files to convert
    i_ln = 0
    comm_below = False
    n_sw_c_detected = 0
    n_sw_c_converted = 0
    rng_shift_indent0 = range(-1)

    exception_indexes = ['end']
    rngs_shift_indent = []
    rngs_shift_indent_type = [] # Type of identation shift. Contains only integer numbers. 
    txt_subst = MAP_txt_subst
    Lsubs = len(MAP_txt_subst)
    flNm = filePath + '\\' + matFileNm + '.m'
    file1 = open(flNm, 'r', encoding='UTF-8') #
    
    # 👇🏼  Get lines of the current MATLAB file
    try:
        Lines = file1.readlines()
    except UnicodeDecodeError:
        raise Exception('The file: ' + matFileNm + '.m cannot be decoded. Please make sure to check for errors therein.') 

    # 👇🏼 Denote the list of code lines that have undergone a modification with "Line1": 
    Lines1 = [] 
    
    print('Converting ' + flNm + '\n'*2)
    decorator_calls = 0
    # print(get_vector_elements.calls) 
    # print(get_vector_elements.error_msg)

    logProg = dict()

    # Sec. 0: Split MATLAB lines that are stacked in the same text line ================================================================
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        if ';' in ln1:
            lns = ln1.split(';')
            # Make sure that we are not dealing with vector or matrix
            
            if lns[-1].replace(' ', '') == '\n':
                lns = lns[:-1]
            cnd_more_than_one_cmd = True
            
            for lln in lns:
                cnd_more_than_one_cmd *= ((len(lln)>0) and '=' in lln)
            cnd = cnd_more_than_one_cmd and (len(lns) > 1)
            # 👆🏼 So far this is the only definite condition we can use. If we have to deal with methods (OOP in MATLAB, this conditional will have to be modified)
            if cnd:
                n_blanks = 0
                if len(ln1) > 0: 
                    while (ln1[n_blanks] == ' ') and n_blanks<100: 
                        n_blanks += 1
                for lln in lns:
                    n_blanks1 = 0
                    if len(lln) > 0: 
                        while (lln[n_blanks1] == ' ') and n_blanks1<100: 
                            n_blanks1 += 1
                    Lines1.append(n_blanks*' ' + lln[n_blanks1:] + ';\n')
            else:
                Lines1.append(ln1)
        else:
            Lines1.append(ln1)

    Lines = Lines1
    # ================================================================================================================================
    
    # # Sec. 0.1: Clean blanks that are not tabs:==========================================================================================================================================================
    # Lines1 = []
    # for ln in Lines:
    #     ln1 = ln
    #     n_blanks = 0
    #     if len(ln1) > 0: 
    #         while (ln1[n_blanks] == ' ') and n_blanks<100: 
    #             n_blanks += 1
                
    #     if n_blanks > 98:
    #         print('')        
    #     shft = np.mod(n_blanks, 4)
    #     ln1 = ln1[shft+1:]
    #     Lines1.append(ln1)
        
    # Lines = Lines1
    # # ================================================================================================================================



    # Sec. 1: 👇🏼 Character substitutions ================================================================
    Lines1 = []
    for ln in Lines:
        i_ln += 1
        ln1 = ln
        # print(ln1)
        if comm_below:
            ln1 = '#' + ln1# + '\n'
            comm_below = False

        else:
            for i in range(Lsubs):
                txti = txt_subst[i]
                Lt = len(txti)
                txt0 = txti[0]
                txt1 = txti[1]
                
                # 👇🏼 text mode
                text_mode = txti[2] 
                
                if text_mode == 'any':     
                    ln10 = ln1
                    ln1 = ln1.replace(txt0, txt1)

                    if ln10 != ln1: # something was actually replaced
                        
                        # if txt0 == '...':
                        #     print('')

                        if Lt > 3:
                            if txti[3] == 'below': 
                                comm_below = True

                        if txt0 == 'switch ': 

                            # n_sw_c_converted: Count of already converted switch-case statements
                            # n_sw_c_detected: Count of switch-case statements detected so far

                            n_sw_c_converted = n_sw_c_detected
                            n_sw_c_detected += 1    


                            # 👇🏼 find the "end" of current "switch-case" statement =========================
                            iLnSwCase = 0
                            for ii0 in range(10000):
                                lnd = Lines[ii0+i_ln]
                                lnd_no_bl = lnd.replace(' ', '')
                                if lnd_no_bl.startswith('end'):
                                    break
                            iLnSwCase = ii0+1
                            # 👆🏼 ===========================================================================    
                            
                            # # 👇🏼 find the "otherwise" of current "switch-case" statement =========================
                            # iLnOtherwise = 0
                            # for ii0 in range(10000):
                            #     lnd = Lines[ii0+i_ln]
                            #     lnd_no_bl = lnd.replace(' ', '')
                            #     if lnd_no_bl.startswith('otherwise'):
                            #         break
                            # iLnOtherwise = ii0+1
                            # # 👆🏼 ===========================================================================    


                            
                            # get all lines that should have their identation changed
                            rng_shift_indent0 = range(i_ln+1, i_ln+iLnSwCase+0)
                            rngs_shift_indent.append(rng_shift_indent0)
                            rngs_shift_indent_type0 = np.ones(len(rng_shift_indent0)) * int(-1)
                            rngs_shift_indent_type.append(rngs_shift_indent_type0)
                            # =======================================================


                        if txt0 == 'case ': 
                            if n_sw_c_converted != n_sw_c_detected:
                                n_sw_c_converted = n_sw_c_detected

                                # 👇🏼 Change 'elif' to 'if', because "case" has been replace with "elif:",
                                # 👇🏼 which means that the first "elif:" should be corrected
                                ln1 = ln1.replace('elif', 'if')      
                                # 

                elif text_mode == 'start':

                    # 👇🏼 get blanks before any first char ===================================================
                    if txt0 in ln1:
                        idxx1 = ln1.find(txt0)
                        i_b = -1
                        for i_b in range(idxx1):
                            if ln[(i_b)] != ' ': break
                        if i_b == idxx1-1:    
                            ln1 = ' '*i_b + txt1 #+ ln1[idxx1-1:]
                        ln1 = ln1 + '\n'
                        #print(ln1[idxx1-1:])
                    # 👆🏼 ======================================================================================================


                elif text_mode == 'function':
                    #             # not completely correct: 
                    txt01 = txt0 + '('
                    txt11 = txt1 + '('
                    ln1 = ln1.replace(txt01, txt11)
                
                elif text_mode == 'end':
                    
                    if txt0 in ln1:
                        ln1 = ln1.replace('\n', '')
                        i_C = ln1.find('#')
                        if i_C == -1: i_C = len(ln1) # did not find comment
                        ln1nC = ln1[:i_C]
                        if len(ln1nC) > 0:
                            for n_bl_end in range(1,len(ln1nC)+1):
                                dum1 = ln1nC[-n_bl_end]
                                if dum1!=' ': 
                                    break
                        else:
                            ln1 = ln1 + '\n'

                        if n_bl_end != 0: 
                            Ll = len(ln1nC)-n_bl_end+1  
                            ln1nC = ln1nC[0:Ll]   
                        
                        
                        pp=ln1nC[-len(txt0):]
                        ln1_nobl = ln1nC#.replace(' ', '')
                        if len(ln1_nobl)>0:
                            if ln1_nobl.endswith(txt0):
                                ln1 = ln1nC[:-len(txt0)]+ln1[i_C:] + '\n'

        for irng, rng_shft_i in enum(rngs_shift_indent):
            
            rng_shft_type_i = rngs_shift_indent_type[irng]
            iDum =  [jj for jj, x in enum(rng_shft_i) if x==i_ln] 
            if len(iDum)>0: iDum = iDum[0]
            if i_ln in rng_shft_i and rng_shft_type_i[iDum] != 0 and ln1.lstrip() != ln1: 
                # and rng_shft_type_i[i_ln] != 0: 
                n_dum = round(4 *rng_shft_type_i[iDum])
                if n_dum < 0:
                    if ln1.startswith(n_dum*' '): # do not "shift-tab" if there is text
                        ln1 = ln1[(-n_dum):]
                else:
                    print(gay)
                rngs_shift_indent_type[irng][iDum] = 0

        # err_msg_4user = get_vector_elements.msg # can I add it in the function "store_line" for simplicity?
        # store_line(ln1, err_msg_4user, -1)

        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1    
    # ================================================================================

    # Sec. 2:  The "find" function ================================================================================
    # In MATLAB, the "find" function is used as follows:
    # idx = find(condition)
    # for example: idx_max_a = find(a == max(a)) returns the index for which: a(idx_max_a) = max(a)
    # in python, the same result is achieved by:
    # idx = [i for i, x in enum(a) if x==max(a)]
    # This is the substitution we are performing in this section
    
    is_under_dev = False
    if not is_under_dev:
        cmd = 'find'
        lhs_repl = 'dum_cnd'
        Lines1 = []
        
        for iLn, ln in enum(Lines):
            ln1 = ln
            add_line = False
            if cmd+'(' in ln1:
                # function usage found in command
                idx0 = ln1.find(cmd)
                ln1 = ln1.replace(cmd, '')    
                ln_after_cmd = ln1[idx0-len(cmd)+1:]
                idxc = ln_after_cmd.find('#')
                ln_after_cmd = ln_after_cmd[:idxc]
                idxeq = ln1.find('=')
                rhs = ln1[idxeq+1:].replace(' ','') # right-hand side of the equation
                lhs = ln1[:idxeq].replace(' ','') # left-hand side of the equation
                
                # Get any potential identation ======================================================================
                identation_level = 0
                while(ln1.startswith((4*(identation_level+1))*' ')):
                    identation_level += 1
                
                ln1 = 4*identation_level*' ' + lhs_repl + ' = ' + rhs
                ln2 = 4*identation_level*' ' + lhs + ' = [i for i, x in enumerate(' + lhs_repl + ') if x]' + '\n'
                # =========================================================================================================
                
                
                # check if those lines belong in different identation areas ================================
                # for ir in rngs_shift_indent:
                    # if iLn in ir:
                        #  (t_t_ref_y==min[t_t_ref_y - 1]=min[t_t_ref_y - 1]))
                # for irng, rng_shft_i in enumerate(rngs_shift_indent):
                #     rng_shft_type_i = rngs_shift_indent_type[irng]
                #     iDum =  [jj for jj, x in enumerate(rng_shft_i) if x==i_ln] 
                #     if i_ln in rng_shft_i and rng_shft_type_i[iDum] != 0: 
                #         # and rng_shft_type_i[i_ln] != 0: 
                #         n_dum = round(4 *rng_shft_type_i[iDum])
                #         if n_dum < 0:
                #             if ln1.startswith(n_dum*' '): # do not "shift-tab" if there is text
                #                 ln1 = ln1[(-n_dum):]
                #         else:
                #             print('Nothing here yet!')
                #         rngs_shift_indent_type[irng][i_ln] = 0
                # # ==========================================================================================
                
                
                
                
                add_line = True
                exception_indexes = exception_indexes + [lhs]
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
            if add_line: Lines1.append(ln2)

        Lines = Lines1   
    # ================================================================================

    #  Sec. 3:  'elif <expr>' ---> 'elif <expr>' + ':' ===========================================
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        if 'elif' in ln1:
            idxc = ln1.find('#')
            idxe = ln1.find('\n')
            if idxc != -1: 
                ln1 = ln1[:idxc] + ':' + ln1[idxc:]

            ln1 = ln1.replace('\n', ':\n')
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1  
    # ================================================================================


    #  Sec. 4: Handle struct variables ========================================================
    # Basically convert "d.field_1" to "d['field_1']"
    
    Lines1 = []
    dev_use_regex = False # OPT: can just use regex
    dev_use_combination_regex_ifs = True
    if dev_use_regex:
        # patt = r"\w+\['\w+'\]" # (word, followed by word in "['']")
        # patt = r"\w+\.\w+" # (word, followed by word in "['']")
        patt = r"[\.[a-z,A-Z,_]+]*" # pattern for struct variables
        
        
        patt = r"[a-zA-Z]\w*\.[a-zA-Z]\w*"

        DICTS = []
        for ln in Lines:
            ln1 = ln
            lstDS = dict()
            lstDS['struct'] = re.findall(patt, ln)
            
            lstDS['struct'] = [x for x in lstDS['struct'] if len(x)>0]
            lstDS['struct'] = [x for x in lstDS['struct'] if '.' in x]
            
            lstDS['dict'] = []
            for iil, l in enum(lstDS['struct']):
                
                # ⬇ Search for dicts to declare
                words = re.findall(r"\w+", l)
                # ⬆
                
                if len(words) < 2: break
                s = words[0] # HERE1
                
                # ⬇ declare dict
                if iil==0:
                    if not s in DICTS:
                        DICTS.append(s)
                        for illn, lln in enum(ln1):
                            if lln != ' ': break
                            
                        iLn1 = -1
                        ln1_1 = ln1
                        while (is_broken_line(ln1_1)) and (np.abs(-2-iLn1)<=len(Lines1)):
                            iLn1 += 1
                            ln1_1 = Lines1[-1-iLn1]
                                
                        if not (np.abs(-2-iLn1)<=len(Lines1)):
                            idx_insert = -np.inf
                        else:
                            idx_insert = len(Lines1)-iLn1-1
                            
                        Lines1 = store_line(Lines1, (iLn1==-1)*illn*' ' + s + ' = dict()\n', get_vector_elements.error_msg, idx_insert)
                # ⬆
                
                for wi in words[1:]:
                    s += "['" + wi + "']"
                lstDS['dict'].append(s) 
                ln1 = ln1.replace(l, s)

            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
        Lines = Lines1        
    
    elif dev_use_combination_regex_ifs:
        for ln in Lines:
            ln1 = ln
            LIST, ln1 = change_struct(ln1, LIST)
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
        Lines = Lines1
    else:
        for ln in Lines:
            ln1 = ln
            if '.' in ln1:
                flds = []
                xx = findOccurrences(ln1, '.')
                idx_dot = xx.y        
                n_flds = 0
                for inn in range(len(idx_dot)):
                    if inn > 0:
                        # re-do findOccurences because ln1 changes in each iteration
                        xx = findOccurrences(ln1, '.')
                        idx_dot = xx.y        
                    if len(idx_dot) == 0: break
                    i = idx_dot[inn-n_flds]  

                    if inn+1 < len(idx_dot):  
                        i1 = idx_dot[inn+1]+1
                    else:
                        i1 = len(ln1)
                    # check if struct variable is in a comment 
                    ln_before = ln1[:i]
                    xx = findOccurrences(ln_before, '#')       
                    idx = xx.y
                    if np.mod(len(idx), 2) == 0:
                        # is not in comment
                        ln1_after = ln1[i + 1:i1]
                        p1 = len(ln1_after) - 1
                        fldi = ln1_after[0:p1]
                        for ltr in LIST['operators']:
                            xx = findOccurrences(ln1_after, ltr)       
                            idx = xx.y
                            if  (len(idx) > 0):
                                if idx[0] < p1:
                                    p1 = idx[0]
                                # print(ln1_after[0:p1])
                                fldi = ln1_after[0:p1]
                                if len(fldi) > 0:
                                    if fldi[-1] in LIST['operators']:
                                        fldi = fldi[:-1]
                                    elif fldi[0] in LIST['operators']:
                                        fldi = fldi[1:]
                                    # break
                        flds.append(fldi)
                    n_flds = len(flds)
                    for fld in flds:
                        dum0 = '.' + fld
                        dum1 = "['" + fld + "']"
                        is_num = fld.isnumeric()
                        if not is_num: ln1 = ln1.replace(dum0, dum1)
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)

        Lines = Lines1
    # ================================================================================

    #  Sec. 5: Convert "for" loop =======================================================================

    Lines1 = []
    for ln in Lines:
        ln1 = ln
        # xx = findOccurrences(ln1, loopSyntax)
        # ln1_no_bl = ln1.replace(' ', '')
        iDum = 0
        if not ln1: ln1 = '\n'
        while ln1[iDum] == ' ': iDum += 1
        is_for_loop = ln1[iDum:].startswith(loopSyntax)

        # ln1_no_bl[:len(loopSyntax)] == loopSyntax
        if is_for_loop:
            ln1 = ln1.replace('=', 'in')
            if ':' in ln1:
                ln1 = ln1.replace(':', ', ')
                ln1 = ln1.replace('in', inRngCmd)
                xx = findOccurrences(ln1, '#')
                idxx = xx.y
                idx0 = len(ln1)
                if len(idxx) != 0:
                    
                    dum10 = ln1[idxx[0]:]
                else:
                    dum10 = ''
                if True: #len(dum10) > 0: 
                    idx_inRngCmd = ln1.find(inRngCmd)
                    idx_end_inRngCmd = idx_inRngCmd + len(inRngCmd)
                    inRngContent = ln1[idx_end_inRngCmd:idx0-1]
                    inRngContent = inRngContent.replace(' ', '')
                    # print(inRngContent)
                    # print(ln1)
                    if inRngContent[0] == '1':
                        inRngContent = inRngContent[2:]
                        idx0 = ln1.find('for') + len('for')
                        idx1 = ln1.find('in')
                        excp_idx = ln1[idx0:idx1]
                        excp_idx = excp_idx.replace(' ', '')
                        exception_indexes = exception_indexes + [excp_idx]
                    # else:
                    #     inRngContent = str(int(inRngContent[0])-1) +\
                    #          inRngContent[1:]
                    
                ln1 = ln1[:idx_inRngCmd-1] + ' ' + inRngCmd + inRngContent +\
                    '):' + dum10
                ln1 = ln1 + '\n'
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1
    exception_indexes = unique(exception_indexes)

    # ================================================================================


    #  Sec. 6: if-statements: add ":" =========================================================
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        # get blanks before any first char
        txt0 = 'if'
        if txt0 in ln1:
            
            idxx1 = ln1.find(txt0)
            i_b = -1
            for i_b in range(idxx1):
                if ln[(i_b)] != ' ': break
            
            if not('#' in ln1[:i_b+1]):
                if ln1[i_b+1:i_b+len(txt0)+1] == txt0:
                    i_b = i_b + 1
                    xx = findOccurrences(ln1, '#')
                    idxx = xx.y
                    ln1 = ln1.strip()
                    if len(idxx) == 0:
                        ln1 = ln1 + ':'
                    else:   
                        ln1 = ln1[:idxx[0]] + ':' + ln1[idxx[0]+1:]
                    ln1 =  i_b*' ' + ln1 + '\n'
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1    
    # ================================================================================


    #  Sec. 6.1: @ ---> lambda function ======================================================
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        if '@' in ln1:
            idx = ln1.find('@')
            ln11 = ln1[idx:]
            i0 = ln11.find('(')
            i1 = ln11.find(')')
            lambdaVars = ln11[i0+1:i1]
            lhs = ln1[:ln1.find('=')]
            
            ln1 = lhs + ' = lambda ' + lambdaVars + ' : ' + ln11[i1+1:]
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1
    # ============================================================================================================ 


    #  Sec. 7: convert "(" to "["  ============================================================
    Lines1 = []
    secID = 'Sec.7'
    convMode = 1        # 1: the original one, 3: experimental one
    # info_sec = dict()
    # info_sec['ℹ'] = 'deals with broken lines'*(convMode==3)
    logProg[secID] = dict()
    logProg[secID]['ℹ'] = 'deals with broken lines'*(convMode==3)
    
    if convMode==2:
        # Make the conversion using regular expressions
        
        
        # IS UNDER DEV!!!
        print('UNDER DEVELOPMENT:: convMode==2 FOR Sec. 7: convert "(" to "["')
        
        for ln in Lines:
            ln1 = ln
            
            if '(' in ln:
                # for lsti in LIST['functions']:
                # PROBLEM 1: should not replace('(',' [ ') if this is in LIST['functions']
                patt = dict()
                
                
                
                L = ln1.replace('(',' [ ').replace(')',' ] ').replace(':', ' : ')
                patt1 = r"[\w,0-9,\+,\-,\/,\*,\^,=,\[,\],\:]*"
                patt2 = r"[(,)]*"
                popo = re.findall(patt1, L)
                popo = [x for x in popo if len(x)>0]
                # print(popo)
                L = ''
                for ip, p in enum(popo):
                    if '[' in p:
                        if not popo[ip-1] in LIST['functions']:
                            ptmp = p.replace('[', '[-1+').replace(':', ':-1+')
                        else:
                            ptmp = '('
                    else:
                        ptmp = p
                    L += ptmp
                ln1 = L + '\n'
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
            
        Lines = Lines1
        
    elif convMode == 3:
        # IS UNDER DEV!!!
        
        devProb =[\
            ['✔', 'Has error when lines are broken'],\
            ['✔', 'Deletes all whitespaces!'],\
            ['🔘', "Broken lines: Whenever there's text between '\\' and '\n', the algorithm does not work properly ---BUT--> Maybe it is always like that!"],\
            ['✔', "Confuses dicts (e.g. 'info_ll['status'] --> info_llstatus')"] ,\
            ['🔘', "Broken lines: Revert to initial state!"],\
            ['🔘', "Tampers with lines that don't even have indexed variables (such as if-else statements)!"],\
            ['✔', "Does not respect existing indentation"],\
            ['🔘', "Does not ignore lines after comment"]\
            ]

        logProg[secID]['DEV_PROBLEMS'] = devProb
        
        
        print('UNDER DEVELOPMENT:: convMode==3 FOR Sec. 7: convert "(" to "["')
 
        
        i_skip = [] # Indexes for lines to skip
        
        for iLn, ln in enum(Lines):
            
            if not iLn in i_skip: 

                ln1 = ln
                ln_next = ln1
                ln1_merge = ''
                iskp = 0 # 👈🏼 Lines to skip

                lnbr = re.findall(r"[\\][\s]*\n$", ln_next)
                while is_broken_line(ln_next): # there is at least one broken line!
                    iskp += 1
                    ln1_merge += ln_next[:ln_next.find(lnbr[0])]  #re.sub("[\\][\s]*\n$", "[\s]*\n$", ln_next)
                    ln_next = Lines[iLn + iskp]
                    i_skip.append(iLn + iskp)
                    lnbr = re.findall(r"[\\][\s]*\n$", ln_next)
                    
                ln1_merge += ln_next
                ln1 = ln1_merge
                
                iComm = ln1.find('#')
                if iComm!= -1:
                    wrd = ln1[:iComm]
                    lnComment = ln1[iComm:]
                else:
                    wrd = ln1
                    lnComment = ''
                
                # lnComment
                
                # Count parentheses ================================================
                pMode = 2
                parenthesis_counter = []
                if pMode == 1:
                    wrd = wrd.replace('(',' [ ').replace(')',' ] ').replace(':', ' : ')
                    patt1 = r"[a-z,0-9,\+,\-,\/,\*,\^,=,\[,\],\:]*"
                elif pMode == 2:
                    wrd = wrd.replace('(',' ( ').replace(')',' ) ').replace(':', ' : ')
                    # patt1 = r"[[\['\w+'\]+]*,a-z,A-Z,0-9,<,>,<=,>=,\+,\-,\/,\*,\^,=,==,\(,\),\:,_]*"
                    # patt1 = r"[a-z,A-Z,0-9,<,>,<=,>=,\+,\-,\/,\*,\^,=,==,\(,\),\:,_,\[\', \'\]]*"
                    patt1 = r"[a-z,A-Z,0-9,<,>,<=,>=,\+,\-,\/,\*,\^,=,==,\(,\),\:,_,[\['\w+'\]+]*]*"
                # ================================================================================================
                    
                patt2 = r"[(,)]*"
                popo = re.findall(patt1, wrd)
                popo = [x for x in popo if len(x)>0]
                # print(popo)
                L = ''
                p0 = ''
                
                ln1 = ln1_merge
                for iP, p in enum(popo):
                    
                    
                    if not ((p0 in LIST['functions']) or (p0 in LIST['operators'])):
                        if '(' in p: parenthesis_counter.append([1, 0])
                        pNew = p.replace('(', '[-1+').replace(':', ':-1+') #.replace(')', ']')
                        n_whtspc_before = 0
                        n_whtspc_after = 0
                    else:
                        if '(' in p: parenthesis_counter.append([1, 1])
                        pNew = p
                        n_whtspc_before = 0
                        n_whtspc_after = 0
                        
                    if ')' in p:   
                        parenthesis_counter = [[x[0]-1, x[1]] for x in parenthesis_counter]
                    
                    if len(parenthesis_counter)>0:
                        if parenthesis_counter[-1][0] == 0:
                            if parenthesis_counter[-1][1] == 0:
                                pNew = ']'
                                parenthesis_counter = parenthesis_counter[:-1]
                    
                    if pNew in LIST['operators_double_whitespace']: 
                        n_whtspc_before = 1
                        n_whtspc_after = 1
                    elif pNew in LIST['operators_at_right_whitespace']:
                        n_whtspc_before = 0
                        n_whtspc_after = 1
                    
                    n_tabs = 0
                    while ln1.startswith(" "*4*(n_tabs+1)):
                        n_tabs += 1
                    
                        
                    L += " "*4*(n_tabs) + n_whtspc_before*' ' + pNew + n_whtspc_after*' '
                    p0=p
                    
                print(L)    
                    
                # for iP, p in enumerate(popo):    
                #     pPrev = popo[iP-1]
                #     if '(' in p:
                #         if not pPrev in LIST['functions']:
                #             parenthesis_counter = [[x[0]+1, x[1]] for x in parenthesis_counter]
                #     elif ')' in p:
                #         parenthesis_counter = [[x[0]-1, x[1]] for x in parenthesis_counter]
                #         try:
                #             xlast = parenthesis_counter[-1]
                #         except:
                #             print('')
                #         if xlast[0]==0:
                #             # parenthesis closed
                #             if xlast[1]==0: 
                #                 p = p.replace(')', ']')
                #             parenthesis_counter = parenthesis_counter[:-1]

                ln1 = L + lnComment +  '\n'
                ln1Prev = ln1
                Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
            
        Lines = Lines1    
    elif convMode == 1:

        for ln in Lines:
            ln1 = ln
            n_blanks = 0
            if len(ln1) > 0: 
                while ln1[n_blanks] == ' ': n_blanks += 1
            idx0 = 0
            ln1_tmp0 = ''
            i_pr = 0
            ln1tmp = ln1
            i_ignore = []
            lst_idx = list()
            xx = findOccurrences(ln1tmp, '(')
            if len(xx.y) > 0:
                lst_idx = lst_idx + xx.y
            curly_brackets = findOccurrences(ln1tmp, '{') 
            if len(curly_brackets.y) > 0:
                lst_idx = lst_idx + curly_brackets.y
            Np = len(lst_idx)
            par_count = 0
            ln10_prev = ''

            # while '(' in ln1tmp:
            for zgi in range(Np):
                if zgi > 0:
                    # recalculate positions of '(' or '{'
                    lst_idx = []
                    xx = findOccurrences(ln1tmp, '(')
                    if len(xx.y) > 0:
                        lst_idx = lst_idx + xx.y
                    curly_brackets = findOccurrences(ln1tmp, '{') 
                    if len(curly_brackets.y) > 0:
                        lst_idx = lst_idx + curly_brackets.y
                    
                    if len(lst_idx) == 0:
                        break # PROBLEM 2: ⚠⚠⚠ "DIRTY-BAD" PROGRAMMING ALERT!!!
                    # print(lst_idx)
                    # print(zgi - par_count)

                    if zgi - par_count < len(lst_idx):
                        idx0 = lst_idx[zgi - par_count]
                    else:
                        continue
                else:
                    idx0 = lst_idx[zgi]    

                par_type = ln1tmp[idx0]
                ln_before_par = ln1tmp[:idx0] 
                ln_after_par = ln1tmp[idx0+1:] 
                ln1tmp = ln1tmp[idx0+1:]

                wrdy = parenthesis_cls()
                wrdy.get_word_before_par(ln_before_par, LIST['operators'], idx0)
                word_before_par = wrdy.word_before_par

                if (not ('#' in ln_before_par)) and len(word_before_par) > 0: 
                    # if the line is not a commented line
                    wrdy.get_par_content(ln1, idx0, i_pr, ln_after_par, \
                        word_before_par, LIST['functions'], par_type)
                    par_content = wrdy.par_content
                    ln_after_par_closed = wrdy.txt_after_par_closed
                    if len(par_content) > 0:
                        idx_comma = -1
                        idx_slice = -1
                        # shift index due to different numbering between matlab and python
                        had_comma = 0
                        if ',' in par_content: # 👈🏼 2 or more slots in parentheses
                            idx_comma = par_content.find(',')
                            before_comma0 = par_content[:idx_comma]
                            after_comma0 = par_content[idx_comma+1:]
                            wrdy.change_slice_content(before_comma0, had_comma, exception_indexes)
                            before_comma0 = wrdy.slice_content
                            if wrdy.had_slice == 0:
                                dum1 = ' - 1'
                                dumv1 = before_comma0.split() # 👈🏼 split based on blanks
                                for ch in dumv1:
                                    if (ch in exception_indexes):
                                        dum1 = ''      
                                        break    
                                if 'end' in dumv1:
                                    dum1 = ''    
                                    before_comma0 = '-1'
                            else:
                                dum1 = ''


                            before_comma = before_comma0 + dum1
                            wrdy.change_slice_content(after_comma0, had_comma, exception_indexes)
                            after_comma0 = wrdy.slice_content
                            slice_after_comma0 = wrdy.had_slice
                            if wrdy.had_slice == 0:
                                dum1 = ' - 1'
                                dumv1 = after_comma0.split() # split based on blanks
                                for ch in dumv1:
                                    if (ch in exception_indexes):
                                        dum1 = ''      
                                        break  
                                if 'end' in dumv1:
                                    dum1 = ''    
                                    after_comma0 = '-1'                  
                            else:
                                dum1 = ''
                            after_comma = after_comma0 + dum1
                            par_content = before_comma + '][' +  after_comma
                            had_comma = 1

                        wrdy.change_slice_content(par_content, had_comma, exception_indexes)
                        par_content = wrdy.slice_content

                        if (had_comma == 0 and wrdy.had_slice == 0):
                            par_content_nbl = par_content.replace(' ', '')
                            if (not (par_content_nbl in exception_indexes)) and (par_content_nbl != 'end'):
                                dum1 = ' - 1'
                            else:
                                dum1 = ''   
                            if par_content_nbl == 'end': par_content = '-1'                        
                            par_content = par_content + dum1
                            
                        n_blanks = 0
                        
                        if len(word_before_par) != 0:
                            lnbpar = ln_before_par[:-len(word_before_par)]
                        else:
                            lnbpar = ln_before_par
                        ln1 = ' '*n_blanks  + lnbpar +  word_before_par +\
                                '[' + par_content + ']' + ln_after_par_closed   
                        
                        ln10_prev = ''
                        par_count += 1
                    else:
                        ln10_prev = word_before_par + par_type 
                        i_pr = i_pr + len(ln10_prev)
                        i_ignore.append(idx0)
                    ln1tmp = ln1
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
        Lines = Lines1    
    # ================================================================================

    #  Sec. 8: Direct text substitutions (that do contain '.') =================================================

    txt_subst = txt_subst_dot

    # print(txt_subst[0][1])
    Lsubs = len(txt_subst)
    Lines1 = []
    # patt = r'norm('
    for ln in Lines:
        ln1 = ln
        for i in range(Lsubs): 
            ln1 = ln1.replace(txt_subst[i][0], txt_subst[i][1])
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1    
    # ================================================================================

    #  Sec. 9: change expressions of "[str1, str2, ...]" to [str1+str2+...] ===================

    Lines1 = []
    lst_vec_no_change = [] # 👈🏼 Needed so that MATLAB commands such as "A_str = ['str1', 'str2', ...]" are not to be confused with vectors
    z=0
    for ln in Lines:
        ln1 = ln
        ln1_nb = ln1.replace(' ',"")
        is_vec = True
        [dum, inhalt_urspr, is_matrix, inhalt] = get_vector_elements(ln1)
        if "['" in ln1_nb:
            if len(dum)>1:
                is_vec = False
        elif '[' in ln1_nb:
            if len(dum)>1:
                ln01 = inhalt_urspr.split(',')
                ln02 = []
                for lnn in ln01: ln02.append(lnn.replace(' ', ''))
                for lnn in ln02:
                    if "'" in lnn:
                        is_vec = False
                        break
                    else:
                        for lnpr in Lines1[:z]:
                            if lnn in lnpr:
                                # add very simplistic rule (incomplete though)
                                is_vec = not (("'" in lnpr) or ('str' in lnpr))
                                break

        if not is_vec:
            ln1 = ln1.replace(',','+')   
            ln1 = ln1.replace('[','')   
            ln1 = ln1.replace(']','')   
            lst_vec_no_change.append(ln1)     
        z+=1

        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1  
    # ================================================================================


    #  Sec. 10: Matlab vectors that don't have commas ==========================================
    # NOTE: Weakness: only for cases of non nested vectors 
    Lines1 = []
    re_list = ['\d+', '\s+']
    rngs_broken_lines = []
    ln1_prev = ''
    lst_taken_words = ['if', 'for']
    for i_ln, ln in enumerate(Lines):
        
        
        # Check if this line is in broken range (so that we ommit it, since we have merged the broken lines in a previous iteration)
        # \==================================================\==================================================\==================================================
        is_in_broken_line_range = False
        for rngbl in rngs_broken_lines:
            if i_ln in rngbl:
                is_in_broken_line_range = True
                break
        # \==================================================\==================================================\==================================================    
            
        if not is_in_broken_line_range:
            ln1 = ln
            
            might_be_vec = True
            for lt in lst_taken_words:
                if lt in ln: might_be_vec = False
            
            if might_be_vec:        
                # 1. Vektor erkennen:
                [lne, i_brl] = extract_from_line_breaks(Lines[i_ln-0:])
                is_in_broken_line_range = False
                for rngbl in rngs_broken_lines:
                    if i_ln in rngbl:
                        is_in_broken_line_range = True
                        break
                if (not is_in_broken_line_range):        
                    if (not ln1 in lst_vec_no_change):

                        # debugging
                        if '# REFERENCE TRAJECTORY FOR LOW LEVEL CONTROLLER -' in ln1_prev:
                            print('')
                        # 

                        # search for line breaks and get actual line
                        rngs_broken_lines_I = []
                        if i_brl > 0:
                            for iid in range(i_brl+1): rngs_broken_lines_I.append(i_ln + iid)
                            rngs_broken_lines.append(rngs_broken_lines_I)
                            ln1 = lne
                        [elemente, inhalt_urspr, is_matrix, inhalt] = get_vector_elements(ln1)
                        is_vec = (len(elemente) > 1) and (not is_matrix)
                        if is_vec:
                            inhalt_neu = elemente[0]
                            for e in elemente[1:]:
                                inhalt_neu += ', ' + e      
                            ln1 = ln1.replace(inhalt_urspr, inhalt_neu)    
                        elif is_matrix:
                            L = len(str_ends_with)
                            inhalt_neu = elemente[0]
                            dum1 =  ', '
                            for e in elemente[1:]:
                                ends_wth = False
                                for ii in range(L):
                                    ie = str_ends_with[ii][0]
                                    if len(e)>=len(ie):

                                        if str_ends_with[ii][1] == 'ends':
                                            cnd1 = e[-len(ie):] == ie
                                        elif str_ends_with[ii][1] == 'is':
                                            cnd1 = e == ie

                                        if cnd1:
                                            ends_wth = True
                                            break
                                    else:
                                        break

                                if not ends_wth:
                                    inhalt_neu += dum1 + e
                                    dum1 =  ', '
                                else:
                                    inhalt_neu += e
                                    if e[-1] == '[':
                                        dum1 = ''
                                    else:
                                        dum1 =  ', '
                            ln1 = ln1.replace(inhalt_urspr, inhalt_neu)   
                            ln1 = ln1.replace(inhalt_urspr, inhalt_neu) 
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
            ln1_prev = ln1
    Lines = Lines1  


        # 1a. mehr als 1 Element: die verschiedene Symbole messen
        # wrdy = parenthesis_cls()
        # wrdy.get_par_content(ln1, 0, LIST['operators'])
        # # get_par_content(self, ln1, idx0, i_pr, ln_after_par,\
        #     #  word_before_par, LIST['functions'], par_type)
        # par_content = wrdy.par_content
        # print(par_content)
        # parenthesis_cls get_word_before_par(self, s_in, LIST['operators'], idx0):

        # 2. Inhalt erwerben:


    # ====================================================================================

    #  Sec. 11: Substituting special functions =============================================
    is_under_dev = True
    if not is_under_dev:
        Lsubs = len(special_functions)
        words_pattern = '[a-z]+'
        for ln in Lines:
            ln1 = ln
            for i in range(Lsubs):
                txt0 = special_functions[i][0] 
                if txt0 in ln1:
                    # ln_args = split(special_functions[i][1], LIST['operators'])
                    ln_args = re.findall(words_pattern, special_functions[i][1], flags=re.IGNORECASE)
                                    # print(ln_args)
                    n_args = len(ln_args)

                    if special_functions[i][1].count(',') == n_args-1:
                        if special_functions[i][2].count('==') == n_args-1:
                            idx0 = ln1.find(txt0) 
                            idx = idx0 + len(txt0)
                            wrdy.get_word_before_par(ln1[:idx], [''], idx)
                            wrdy.get_par_content(ln1, idx, [], ln1[idx+1:],  ln1[:idx], [''], '(')
                            par_content = wrdy.par_content
                            ln_after_par_closed = wrdy.txt_after_par_closed
                            ln1 = ln1[:idx0] + par_content.replace(special_functions[i][1],\
                                 special_functions[i][2])
                    # if n_args == 2 and '=' in special_functions[i][20]:

    #  Sec. 12: np.zeros(n, 1) or np.zeros(1, n) to np.zeros(n)=================================
    Lines1 = []
    vec_f = [', 1','1, ', ',1', '1,', ',1', '1,']
    # PROBLEM 1. Weak programming above!
    for ln in Lines:
        ln1 = ln
        if 'np.zeros' in ln1:
            for vv in vec_f:
                if vv in ln1:
                    ln1=ln1.replace(vv, '')
                    break
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)

    Lines = Lines1

    # ================================================================================
    # ================================================================================

    #  Sec. 13: "function" to "def" ============================================================
    Lines1 = []
    str0d = 'function'
    str0r = 'def'
    for ln in Lines:
        if ln.startswith(str0d):
            ln = ln.replace(str0d, str0r)

            # get output variables ============================================================

            pos1 = ln.find(str0r)+len(str0r)
            pos2 = ln.find('=')
            out_expr = ln[pos1:pos2]
            out_expr = out_expr.replace(' ', '')
            out_expr = out_expr.replace('[', '')
            out_expr = out_expr.replace(']', '')
            out_vars = out_expr.split(',')
            # print("d")
            # ================================================================================

    Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    # ================================================================================


    # Sec. 14 PATCH. 1: Remove ";" from translated script
    # Motivation for the patch: the fact that we are not yet dealing with nested vectors 
    # ---> some ";" remain, which can be directly replaced
    Lines1 = []
    for ln in Lines:
        ln1 = ln.replace(';', ',')
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg, -1)
    Lines = Lines1
    # ================================================================================
    
    #  Sec. 15: convert slice to linspace ============================================================
    
    #UNDER_DEV
    
    
    
    # ===============================================================================================


    #  Sec. 16: Loading modules ===============================================================
    Lines1 = []
    for ln0 in modules2load: 
        Lines1.append(ln0 + '\n')
    for ln in Lines: 
        Lines1.append(ln)
    Lines = Lines1
    # ================================================================================




    # PRINT Python code ========================================================================
    # for ln in Lines: print(ln)
    flNm = filePath + '\\' + matFileNm + '.py'
    with open(flNm, 'w') as f:
        for ln in Lines: f.write(ln)
    # ================================================================================
