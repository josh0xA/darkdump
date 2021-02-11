# Darkdump - Search The Deep Web Straight From Your Terminal
## About Darkdump
Darkdump is a simple script written in Python3.9 in which it allows users to enter a search term (query) in the command line and darkdump will pull all the deep web sites relating to that query. Darkdump wraps up the darksearch.io API. 
## Installation
1) ``git clone https://github.com/josh0xA/darkdump``<br/>
2) ``cd darkdump``<br/>
3) ``python3 -m pip install -r requirements.txt``<br/>
4) ``python3 darkdump.py --help``<br/>
## Usage 
Example 1: ``python3 darkdump.py --query programming``<br/>
Example 2: ``python3 darkdump.py --query="chat rooms"``<br/>
Example 3: ``python3 darkdump.py --query hackers --page 2``<br/>
 - the 'page' argument filters through the second page of the results that the darksearch engine returns<br/>


