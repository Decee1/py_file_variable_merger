# py_file_variable_merger
Tool for merging 2 Python files + tool for loading them


I needed a tool for merging the variables of 2 Python files together so i creates this ugly tool that just loops though the fileB and merges it with fileA

The need for this was i had 2 Python file, a user config and a main config for a tool where i wanted to have raw Python support so you could just do
```import config ```
and then you have your config data. 
The problem then comes when you have a user config. Which is why this tool exist.
