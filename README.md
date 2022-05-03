# mIn_pyOut
Matlab to Python code translator

# Available conversions so far
## General

| Converted functionalities                                          | MATLAB        | Python         |
| ------------------------------------------------------------------ | ------------- | -------------- |
| Struct variable to dictionary                                      | d.field       | d.['field']    |
| for loops                                                          |               |                |
| if statements                                                      |               |                |
| switch-case statements                                             |               | Python does not use switch-case, so I replaced it with if-elif statements               |
| indexing system                                                    | i = 1,2,...10 | i = 0,1,2,...9 |
| Vectors (does not work for nested vectors and needs some debuggin) |               |                |
| Matrices, but so far without line brakes                           |               |                |


## Specific Functions

| Converted Functionalities | MATLAB                        | Python                                          |
| ------------------------- | ----------------------------- | ----------------------------------------------- |
| MATLAB "find" function    | idx_max_a = find(a == max(a)) | idx = [i for i, x in enumerate(a) if x\==max(a)] | 



# How to use

## User defined parameters

| Variable name (inside the main script) | Description                                                                                                                           |
| ------------- | --------------------------------- |
| matFileNms    | list object wherein the names of the MATLAB files for translation are given (without the extension)                                   |
| filePath      | string variable wherein the path of the folder containing the file is given                                                           |
| list_py_funcs | List of MATLAB and Python function names. This is needed in order for the algorithm not to confuse variable names with function names | 


## MATLAB and Python functions

The main python script of the repository contains the variable "list_py_funcs" (see section "User defined parameters"). Since MATLAB uses indexing via parentheses as well as passing function arguments in parentheses, whereas Python uses brackets for the former procedure, Python will treat a function as a variable by default. To avoid this, simply add the function name to the list variable "list_mat_py_funcs", so that it is treated as a function.

# Open issues
- [ ] Convert function handles (MATLAB) to lambda functions (Python)
- [ ] For vector conversion
	- [ ] Deal with nested vectors (so far no nested vectors are correctly converted. For example: M = [ [1; 1; 1], [1; 1; 1]  ])
- [ ] Open issues written in the beginning of the main script itself
