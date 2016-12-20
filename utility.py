import logging
import json

def print_log(string):
    logging.info(string)
    print(string)
    
def get_name(name):
    '''
    Returns actual name if name can be parsed
    Else returns string 'name'
    '''
    try:
        return str(name)
    except:
        return 'name'
        
def easy_json(d):
    if not isinstance(d, dict):
        d = dict(d)
    return json.dumps(d, indent=4)