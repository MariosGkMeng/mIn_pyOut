# mIn_pyOut
Matlab to Python code translator

# Available conversions so far

| Converted functionalities                                          | MATLAB        | Python         |
| ------------------------------------------------------------------ | ------------- | -------------- |
| Struct variable to dictionary                                      | d.field       | d.['field']    |
| for loops                                                          |               |                |
| if statements                                                      |               |                |
| switch-case statements                                             |               |                |
| indexing system                                                    | i = 1,2,...10 | i = 0,1,2,...9 |
| Vectors (does not work for nested vectors and needs some debuggin) |               |                |
| Matrices, but so far without line brakes                           |               |                |



# How to use

## User defined parameters

| Variable name | Description                                                                                                                           |
| ------------- | --------------------------------- |
| matFileNms    | list object wherein the names of the MATLAB files for translation are given (without the extension)                                   |
| filePath      | string variable wherein the path of the folder containing the file is given                                                           |
| list_py_funcs | List of MATLAB and Python function names. This is needed in order for the algorithm not to confuse variable names with function names | 
