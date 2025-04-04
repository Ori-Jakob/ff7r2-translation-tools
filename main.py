import sys
from gui import render
from tool import tool
#from fix import fix

def main():
    #options = ["Fix CSV File", "CSV Tools", "Exit"]
    options = ["CSV Tools", "Exit"]

    while(True):
        match(render.start(options, "Pick an option")):
            #case 0:
                # original was intended to fix the translation error from the LLM not conforming to proper CSV format
                # I am stubbing this as it was only needed to fix the file once, but there are other text related issues with it
                # fix()
            case 0:
                tool()
            case 1:
                sys.exit(1)

if __name__ == "__main__":
    main()


    
    