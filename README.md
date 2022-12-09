# Cheat Check v 0.2

## Description: 

A script to check Python scripts for duplicates. Given a directory, the script will traverse all Python scripts, and do a simple character-by-character comparison of them. The output is a percentage of similarity between all files, giving you a sense if students have cheated by collaborating on a particular assignment.

## FAQ

- Q: Why didn't you use the AST module?

A: The AST module was throwing exceptions whenever it found syntax errors in the student's code. 

- Q: This script is very slow.

A: Yeah, nothing about this script is optimised. If for example, you are comparing four submissions, you are essentially doing six comparisons. 

- Q: Isn't there a better way to do this?

A: Yeah, probably. At the moment, we strip code comments out of the scripts, and do a simple character-by-character comparison. Soon we will be stripping out all variable names and functions as well and only looking at Python keywords and whitespace.

