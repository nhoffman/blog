import json
import collections

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

def tagdict(jfiles, key = None, reverse = False):
    """
    Given a list of file names in `jfiles`, return (metadata, tags) in
    which `metadata` is a list of dicts corresponding to metadata for
    each post represented among `jfiles`; and `tags`, a dict in the
    format {tag: [list-of-dicts]}. The order of each list is defined
    by `key`, an optional function with a dict of metadata as its only
    argument, and `reverse`.
    """

    metadata = [read_json(f) for f in jfiles]

    if key:
        metadata.sort(key = key, reverse = reverse)

    tags = collections.defaultdict(list)
    for d in metadata:
        for tag in d['tags'].split(','):
            tags[tag].append(d)
    
    return metadata, tags
            

