import code.main as run_code
import sys

'''
This is the main function that runs the code.
'''
if __name__== '__main__':
    arguments = sys.argv[1:]

    if len(arguments)>=1:
        #If port code is passed as an argument
        run_code.get_cargo_vessels(arguments[0])
    else:
        #If port code is not passed as an argument 
        run_code.get_cargo_vessels()