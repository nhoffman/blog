import sys
import glob
import json
import pprint
import collections
from os import path, environ

def get_json(fname):
    with open(fname) as f:
        d = json.load(f)
    return d

def get_properties(target, source, env):
    org, = map(str, source)
    basename = path.splitext(path.basename(org))[0]

    d = dict(
        basename = basename,
        org = org,
        body = env.subst('$build/{}.html'.format(basename)),
        html = env.subst('$site/{}.html'.format(basename))
        )

    in_props = False
    with open(org) as fobj:
        for line in fobj:
            if ':PROPERTIES:' in line:
                in_props = True
            elif ':END:' in line:
                in_props = False
            elif in_props and line.startswith(':'):
                _, key, val = line.split(':', 3)
                d[key] = val.strip()

    with open(str(target[0]), 'w') as out:
        json.dump(d, out, sort_keys=True, indent = 4)

vars = Variables()
vars.Add('site', 'html output',
         ARGUMENTS.get('site', 'site'))
vars.Add('build', 'compiled post bodies',
         ARGUMENTS.get('build', 'build'))

env = Environment(ENV=environ, variables=vars)
env['BUILDERS']['properties'] = Builder(action = get_properties)

posts = [p for p in glob.glob('posts/*.org') if '/_' not in p]

css_worg = env.Command(
    target = '$site/worg.css',
    source = 'css/worg.css',
    action = 'cp $SOURCE $TARGET'
    )

properties = []
for post in posts:
    basename = path.splitext(path.basename(post))[0]
    props, = env.properties(
        target = '$build/{}.json'.format(basename),
        source = post)
    properties.append(str(props))

    body, page = env.Command(
        target = ['$build/{}.html'.format(basename),
                  '$site/{}.html'.format(basename)],
        source = post,
        action = ('emacs --batch --no-init-file '
                  '--script bin/build-page.el '
                  '-post $SOURCE '
                  '-template post-template.org '
                  '-html-body ${TARGETS[0]} '
                  '-html ${TARGETS[1]} ')
        )
    Depends(page, ['bin/common.el','bin/build-page.el','post-template.org'])

if not all(path.exists(p) for p in properties):
    print 'run scons again to build combined pages'
else:
    metadata = [get_json(p) for p in properties]
    metadata.sort(key = lambda d: d['date'], reverse = True)

    tags = collections.defaultdict(list)
    tags['index'] = metadata
    for d in metadata:
        for tag in d['tags'].split(','):
            tags[tag].append(d)

    for tag, posts in tags.items():
        page, = env.Command(
            target = '$site/%s.html' % tag,
            source = 'index.org',
            action = (
                'POSTS="{}" '
                'emacs --batch --no-init-file '
                '--script bin/combine-posts.el '
                '-org-src $SOURCE '
                '-html $TARGET ').format(' '.join(d['basename'] for d in posts))
            )
        Depends(page, ['bin/common.el','bin/combine-posts.el'])
