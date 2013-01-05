import json

def read_json(fname):
    """
    Parse and return contents of file `fname`. 
    """
    with open(fname) as f:
        d = json.load(f)
    return d

def org_properties(fname):
    """
    Read contents of PROPERTIES drawers from org-mode file `fname` and
    return a dict.
    """

    d = {}
    in_props = False
    with open(fname) as fobj:
        for line in fobj:
            if ':PROPERTIES:' in line:
                in_props = True
            elif ':END:' in line:
                in_props = False
            elif in_props and line.startswith(':'):
                _, key, val = line.split(':', 3)
                d[key] = val.strip()
    
    return d


