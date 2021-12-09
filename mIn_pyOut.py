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
# 1. Solve problem 5
# 2. SEARCH "PROBLEM 1"
#
#
# List of bugs-problems
# 1. ✔ Add exception for index that is looped starting from 0 and do not add "-1"
#   b. TODO Avoid confusion (sometimes that index is not looped, but user-set)
# 2. Conditional operations with <>=. DO they need change in indexing?
# 3. Changing vectors ("[a b c] to [a,b,c]" does not work for all cases!)
# 4. deal with nested vectors   
# 5. Broken lines that are fixed again have problems
# =================================================================================
# =================================================================================

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


    # List of math operations to NOT be confuses with vector elements
    lst_operators = ['+', '-', '*', '/', '^']


    # Weakness - Start: nested vectors ================================================
    # ==================================================================================
    #   Does not work on assignments such as
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

    for z, ch in enumerate(c_in):
        if ch.endswith("\n"):
            ch = ch[:-2].replace(' ', '')
            if not ch.endswith('\\'):
                break
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
def store_line(Ln1, ln1, err_msg_4user):
    # store modified line 
    if err_msg_4user:
        ln1 = ln1.replace('\n', '')
        ln1 += ' # ' + err_msg_4user + '\n'

    Ln1.append(ln1)
    get_vector_elements.error_msg = ''
    return Ln1


    



# Read the .m file ===============================================================
filePath = 'C:\\Users\\mario\\Dropbox\\migration'
# Add the matlab files (without the extension) below. You can add more than one
# In case you want to convert only one file, please keep the matFileNms as a list object
matFileNms = ['SOLVE_PROBLEM']   

# ================================================================================

# Direct text substitutions (that do NOT contain '.') =================================================
# init_text final_text position_mode

# List of MATLAB functions, so that the function names are not treated as variable names
list_py_funcs = [\
    'zeros', 'ones', 'get_scaled_time', 'range',\
    'reshape', 'polyval', 'len', 'length', 'eval',\
    'exec', 'error', 'print', 'disp', 'warning', 'any', 'all',\
    'obstacle_generator', 'IPOPT_SOLVE', 'exist', \
    'ipopt_initial_condition', 'switch_controller_mode',\
    'targetStatesInputs', 'full', 'isfield', 'abs',\
    'find', 'size', 'sin', 'cos', 'num2str', 'str',\
    'make_signals_continuous', 'strcmp', 'min',\
    'max', 'norm', 'eval_g', 'reshape', 'tan', 'plant_model',\
    'update_problem_CASADI']
# ==================================================================================================

# List of operators
lst_operators = [' ', '+', '-', '*', '/', ':', ';',\
                 '.', ',', '(', ')', '[', ']', "'"]

 #['function ',   '#function ',        'any',         'below'] ,\
# , 'below' ['~=',          '!=',                'any'],\


# Explicit text substitutions ===========================================================
# =======================================================================================
# NOTE: comment symbols should always be the first to be replaced!
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
# =======================================================================================
# =======================================================================================

txt_subst0 = [\
    ['%',           '#',                 'any'] ,\
    [' ;',          '',                  'end'] ,\
    [';',           '',                  'end'] ,\
    ['...',         '\\ \n',             'any' ],\
    ['end',         '# end',             'start' ] ,\
    ['clc',         '# clc',             'start' ],\
    ['clear',       '# clear',           'start' ],\
    ['else if',     'elif',              'any'] ,\
    ['else',        'else:',             'any'] ,\
    ['length',      'len',               'function'],\
    ['eval',        'exec',              'function'],\
    ['~=',          '!=',                'any'],\
    ['~',           'not ',              'any'],\
    ['clear',       '# clear',           'any'],\
    ['len',         'len',               'function'],\
    ['switch ',     'var_sw_cs = ',      'any'],\
    ['case ',       'elif var_sw_cs ==', 'any',       'case'],\
    ['&&',          'and',               'any'],\
    ['||',          'or',                'any'],\
    ['disp',        'print',             'function'],\
    ['num2str',     'str',               'function'],\
    ['true',        'True',              'any'],\
    ['false',       'False',             'any']] 

# Substitutions that need "np."
txt_subst_dot = [\
    ['zeros',   'np.zeros'] ,\
    ['ones',    'np.ones'] ,\
    ['polyval', 'np.polyval'],\
    ['reshape', 'np.reshape'],\
    ['&',        'and'] ,\
    ['cos(', 'np.cos('],\
    ['sin(', 'np.sin('],\
    ['size','np.shape'],\
    ['norm','np.norm'],\
    ['tan(','np.tan(']    ]

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

special_functions =[\
    ['strcmp', '(a,b)', 'a==b']
    ]

i_ln = 0
comm_below = False
n_switch_case = 0
n_switch_case0 = 0
rng_shift_indent0 = range(-1)

exception_indexes = ['end']
for matFileNm in matFileNms:
    # Loop through all files to convert
    
    rngs_shift_indent = []
    txt_subst = txt_subst0
    Lsubs = len(txt_subst0)
    flNm = filePath + '\\' + matFileNm + '.m'
    file1 = open(flNm, 'r', encoding="UTF-8") #
    
    # 👇🏼  Get lines of the current MATLAB file
    Lines = file1.readlines()
    
    # 👇🏼 Denote the list of code lines that have undergone a modification with "Line1": 
    Lines1 = [] 
    
    print('Converting ' + flNm + '\n'*2)
    decorator_calls = 0
    # print(get_vector_elements.calls) 
    # print(get_vector_elements.error_msg)
    
    # 👇🏼 Character substitutions ================================================================
    for ln in Lines:

        i_ln += 1
        ln1 = ln
        if comm_below:
            ln1 = '#' + ln1# + '\n'
            comm_below = False
        else:
            for i in range(Lsubs):
                # print(str(type(dum1)))
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
                        if Lt > 3:
                            if txti[3] == 'below': 
                                comm_below = True

                        if txt0 == 'switch ': 

                            # n_switch_case0: Count of already converted switch-case statements
                            # n_switch_case: Count of switch-case statements detected so far

                            n_switch_case0 = n_switch_case
                            n_switch_case += 1    


                            # 👇🏼 find the "end" of current "switch-case" statement =========================
                            iLnSwCase = 0
                            for ii0 in range(10000):
                                lnd = Lines[ii0+i_ln]
                                lnd_no_bl = lnd.replace(' ', '')
                                if lnd_no_bl.startswith('end'):
                                    break
                            # 👆🏼 ===========================================================================    

                            iLnSwCase = ii0+1
                            # all lines that should have their identation changed
                            rng_shift_indent0 = range(i_ln+1, i_ln+iLnSwCase+0)
                            rngs_shift_indent.append(rng_shift_indent0)


                        if txt0 == 'case ': 
                            if n_switch_case0 != n_switch_case:
                                n_switch_case0 = n_switch_case
                                ln1 = ln1.replace('elif', 'if')      

                elif text_mode == 'start':
                    # get blanks before any first char
                    if txt0 in ln1:
                        idxx1 = ln1.find(txt0)
                        i_b = -1
                        for i_b in range(idxx1):
                            if ln[(i_b)] != ' ': break
                        if i_b == idxx1-1:    
                            ln1 = ' '*i_b + txt1 #+ ln1[idxx1-1:]
                        ln1 = ln1 + '\n'
                        #print(ln1[idxx1-1:])
                elif text_mode == 'function':
                    #             # not completely correct: 
                    txt01 = txt0 + '('
                    txt11 = txt1 + '('
                    ln1 = ln1.replace(txt01, txt11)
                
                elif text_mode == 'end':
                    
                    if txt0 in ln1:
                        ln1 = ln1.replace('\n', '')
                        i_C = ln1.find('#')
                        if i_C == -1: i_C = len(ln1)
                        ln1nC = ln1[:i_C]
                        if len(ln1nC) > 0:
                            for n_bl_end in range(1,len(ln1nC)+1):
                                dum1 = ln1nC[-n_bl_end]
                                if dum1!=' ': 
                                    break

                        if n_bl_end != 0: 
                            Ll = len(ln1nC)-n_bl_end+1  
                            ln1nC = ln1nC[0:Ll]   
                        
                        
                        pp=ln1nC[-len(txt0):]
                        ln1_nobl = ln1nC#.replace(' ', '')
                        if len(ln1_nobl)>0:
                            if ln1_nobl.endswith(txt0):
                                ln1 = ln1nC[:-len(txt0)]+ln1[i_C:] + '\n'

        for rng_shft_i in rngs_shift_indent:
            if i_ln in rng_shft_i: 
                n_dum = 4
                if ln1.startswith(n_dum*' '): # do not "shift-tab" if there is text
                    ln1 = ln1[n_dum:]
                

        # err_msg_4user = get_vector_elements.msg # can I add it in the function "store_line" for simplicity?
        # store_line(ln1, err_msg_4user)
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1    
    # ================================================================================

    # The "find" function ================================================================================
    is_under_dev = False
    if not is_under_dev:
        cmd = 'find'
        lhs_repl = 'dum_cnd'
        Lines1 = []
        
        for ln in Lines:
            ln1 = ln
            add_line = False
            if cmd+'(' in ln1:
                idx0 = ln1.find(cmd)
                ln1 = ln1.replace(cmd, '')    
                ln_after_cmd = ln1[idx0-len(cmd)+1:]
                idxc = ln_after_cmd.find('#')
                ln_after_cmd = ln_after_cmd[:idxc]
                idxeq = ln1.find('=')
                rhs = ln1[idxeq+1:].replace(' ','')
                lhs = ln1[:idxeq].replace(' ','')
                ln1 = lhs_repl + ' = ' + rhs
                ln2 = lhs + ' = [i for i, x in enumerate(' + lhs_repl + ') if x]' + '\n'
                add_line = True
                exception_indexes = exception_indexes + [lhs]
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
            if add_line: Lines1.append(ln2)

        Lines = Lines1   
    # ================================================================================

    # 'elif <expr>' ---> 'elif <expr>' + ':' ===========================================
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        if 'elif' in ln1:
            idxc = ln1.find('#')
            idxe = ln1.find('\n')
            if idxc != -1: 
                ln1 = ln1[:idxc] + ':' + ln1[idxc:]

            ln1 = ln1.replace('\n', ':\n')
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1  
    # ================================================================================


    # Handle struct variables ========================================================

    # manage exceptions: 
    # 1. is before comment
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        if ('.' in ln1):
            flds = []
            xx = findOccurrences(ln1, '.')
            idx_dot = xx.y        
            n_flds = 0
            for inn in range(len(idx_dot)):
                if inn > 0:
                    xx = findOccurrences(ln1, '.')
                    idx_dot = xx.y        
                if len(idx_dot) == 0: break
                i = idx_dot[inn-n_flds]  

                if inn+1 < len(idx_dot):  
                    i1 = idx_dot[inn+1]+1
                else:
                    i1 = len(ln1)
                # check if is in comment
                ln_before = ln1[:i]
                xx = findOccurrences(ln_before, '#')       
                idx = xx.y
                if np.mod(len(idx), 2) == 0:
                    # is not in comment
                    ln1_after = ln1[i + 1:i1]
                    p1 = len(ln1_after) - 1
                    fldi = ln1_after[0:p1]
                    for ltr in lst_operators:
                        xx = findOccurrences(ln1_after, ltr)       
                        idx = xx.y
                        if  (len(idx) > 0):
                            if idx[0] < p1:
                                p1 = idx[0]
                            # print(ln1_after[0:p1])
                            fldi = ln1_after[0:p1]
                            if len(fldi) > 0:
                                if fldi[-1] in lst_operators:
                                    fldi = fldi[:-1]
                                elif fldi[0] in lst_operators:
                                    fldi = fldi[1:]
                                # break
                    flds.append(fldi)
                n_flds = len(flds)
                for fld in flds:
                    dum0 = '.' + fld
                    dum1 = "['" + fld + "']"
                    is_num = fld.isnumeric()
                    if not is_num: ln1 = ln1.replace(dum0, dum1)
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)

    Lines = Lines1
    # ================================================================================

    # Convert "for" loop =======================================================================

    Lines1 = []
    for ln in Lines:
        ln1 = ln
        loopSyntax = 'for '
        idx = ln1.find(loopSyntax)
        # xx = findOccurrences(ln1, loopSyntax)
        # ln1_no_bl = ln1.replace(' ', '')
        is_for_loop = (idx != -1) 
        # ln1_no_bl[:len(loopSyntax)] == loopSyntax
        if is_for_loop:
            ln1 = ln1.replace('=', 'in')
            if ':' in ln1:
                ln1 = ln1.replace(':', ', ')
                inRngCmd = 'in range('
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
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1
    exception_indexes = unique(exception_indexes)

    # ================================================================================


    # if-statements: add ":" =========================================================
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
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1    
    # ================================================================================

    # convert "(" to "["  ============================================================
    Lines1 = []
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
        xx1 = findOccurrences(ln1tmp, '{') 
        if len(xx1.y) > 0:
            lst_idx = lst_idx + xx1.y
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
                xx1 = findOccurrences(ln1tmp, '{') 
                if len(xx1.y) > 0:
                    lst_idx = lst_idx + xx1.y
                
                if len(lst_idx) == 0:
                    break # PROBLEM 2: "DIRTY-BAD" PROGRAMMING ALERT!!!
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
            wrdy.get_word_before_par(ln_before_par, lst_operators, idx0)
            word_before_par = wrdy.word_before_par

            if (not ('#' in ln_before_par)) and len(word_before_par) > 0: 
                # if the line is not a commented line

                wrdy.get_par_content(ln1, idx0, i_pr, ln_after_par, \
                    word_before_par, list_py_funcs, par_type)
                par_content = wrdy.par_content
                ln_after_par_closed = wrdy.txt_after_par_closed
                if len(par_content) > 0:
                    idx_comma = -1
                    idx_slice = -1
                    # shift index due to different numbering between matlab and python
                    had_comma = 0
                    if ',' in par_content: # 2 or more slots in parentheses
                        idx_comma = par_content.find(',')
                        before_comma0 = par_content[:idx_comma]
                        after_comma0 = par_content[idx_comma+1:]
                        wrdy.change_slice_content(before_comma0, had_comma, exception_indexes)
                        before_comma0 = wrdy.slice_content
                        if wrdy.had_slice == 0:
                            dum1 = ' - 1'
                            dumv1 = before_comma0.split() # split based on blanks
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
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1    
    # ================================================================================

    # Direct text substitutions (that do contain '.') =================================================

    txt_subst = txt_subst_dot

    # print(txt_subst[0][1])
    Lsubs = len(txt_subst)
    Lines1 = []
    for ln in Lines:
        ln1 = ln
        for i in range(Lsubs): ln1 = ln1.replace(txt_subst[i][0], txt_subst[i][1])
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1    
    # ================================================================================

    # change expressions of "[str1, str2, ...]" to [str1+str2+...] ===================

    Lines1 = []
    lst_vec_no_change = []
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

        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    Lines = Lines1  
    # ================================================================================


    # Matlab vectors that don't have commas ==========================================
    # NOTE: Weakness: only for cases of non nested vectors 
    Lines1 = []
    re_list = ['\d+', '\s+']
    rngs_broken_lines = []
    ln1_prev = ''
    for i_ln, ln in enumerate(Lines):
        ln1 = ln
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
                if i_brl > 0:
                    rngs_broken_lines.append(range(i_ln+1,i_ln+i_brl+1))
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
            Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
            ln1_prev = ln1
    Lines = Lines1  


        # 1a. mehr als 1 Element: die verschiedene Symbole messen
        # wrdy = parenthesis_cls()
        # wrdy.get_par_content(ln1, 0, lst_operators)
        # # get_par_content(self, ln1, idx0, i_pr, ln_after_par,\
        #     #  word_before_par, list_py_funcs, par_type)
        # par_content = wrdy.par_content
        # print(par_content)
        # parenthesis_cls get_word_before_par(self, s_in, lst_operators, idx0):

        # 2. Inhalt erwerben:


    # ====================================================================================

    # Substituting special functions =============================================
    is_under_dev = True
    if not is_under_dev:
        Lsubs = len(special_functions)
        words_pattern = '[a-z]+'
        for ln in Lines:
            ln1 = ln
            for i in range(Lsubs):
                txt0 = special_functions[i][0] 
                if txt0 in ln1:
                    # ln_args = split(special_functions[i][1], lst_operators)
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

    # np.zeros(n, 1) or np.zeros(1, n) to np.zeros(n)=================================
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
        Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)

    Lines = Lines1

    # ================================================================================
    # ================================================================================

    # "function" to "def" ============================================================
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
            print("d")
            # ================================================================================

    Lines1 = store_line(Lines1, ln1, get_vector_elements.error_msg)
    # ================================================================================


    # Loading modules ===============================================================
    Lines1 = []
    for ln0 in modules2load: 
        Lines1.append(ln0 + '\n')
    for ln in Lines: 
        Lines1.append(ln)
    Lines = Lines1
    # ================================================================================


    # PRINT ========================================================================
    # for ln in Lines: print(ln)
    flNm = filePath + '\\' + matFileNm + '.py'
    with open(flNm, 'w') as f:
        for ln in Lines: f.write(ln)
    # ================================================================================
