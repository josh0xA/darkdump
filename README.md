# Darkdump - Search The Deep Web Straight From Your Terminal
<p align="center">
  <img src="https://github.com/josh0xA/darkdump/blob/main/imgs/ddumplogo.png?raw=true"</img>
  <br><br>
  <b>Featured In</b>
  <br>
  <a href="https://blackarch.org/sniffer.html"><img src="https://i.imgur.com/IPiAUZi.png">
</p>

## About Darkdump (Recent Notice - 12/27/22)
Darkdump is a simple script written in Python3.11 in which it allows users to enter a search term (query) in the command line and darkdump will pull all the deep web sites relating to that query. Darkdump2.0 is here, enjoy!
## Installation
1) ``git clone https://github.com/josh0xA/darkdump``<br/>
2) ``cd darkdump``<br/>
3) ``python3 -m pip install -r requirements.txt``<br/>
4) ``python3 darkdump.py --help``<br/>
## Usage 
Example 1: ``python3 darkdump.py --query programming``<br/>
Example 2: ``python3 darkdump.py --query="chat rooms"``<br/>
Example 3: ``python3 darkdump.py --query hackers --amount 12``<br/>

 - Note: The 'amount' argument filters the number of results outputted<br/>
  
### Usage With Increased Anonymity 
Darkdump Proxy: ``python3 darkdump.py --query bitcoin -p``<br/>
  
## Menu
```

     ____          _     _
    |    \ ___ ___| |_ _| |_ _ _____ ___
    |  |  | .'|  _| '_| . | | |     | . |
    |____/|__,|_| |_,_|___|___|_|_|_|  _|
                                    |_|

        Developed By: Josh Schiavone
        https://github.com/josh0xA
            joshschiavone.com
              Version 2.0

usage: darkdump.py [-h] [-v] [-q QUERY] [-a AMOUNT] [-p]

options:
  -h, --help            show this help message and exit
  -v, --version         returns darkdump's version
  -q QUERY, --query QUERY
                        the keyword or string you want to search on the deepweb
  -a AMOUNT, --amount AMOUNT
                        the amount of results you want to retrieve (default: 10)
  -p, --proxy           use darkdump proxy to increase anonymity

```
## Visual
<p align="center">
  <img src="https://github.com/josh0xA/darkdump/blob/main/imgs/darkdump_example_output.png?raw=true">
</p>

## Ethical Notice
The developer of this program, Josh Schiavone, is not resposible for misuse of this data gathering tool. Do not use darkdump to navigate websites that take part in any activity that is identified as illegal under the laws and regulations of your government. May God bless you all. 

## License 
MIT License<br/>
Copyright (c) Josh Schiavone
