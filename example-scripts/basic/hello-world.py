title = "Hello world"
description = """
Prints "Hello world" to the console
"""

arguments = [
    {
        "name": "input_phrase", 
        "type": "str", 
        "default": "hello world", 
        "description": "Phrase to print to the console"
    },
]

def main(args):
    print(args.input_phrase)