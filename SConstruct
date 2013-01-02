import glob
from os import path, environ
import json

def properties(target, source, env):
    d = {}
    in_props = False
    with open(str(source[0])) as fobj:
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
env['BUILDERS']['properties'] = Builder(action = properties)

posts = [p for p in glob.glob('posts/*.org') if '/_' not in p]

css_worg = env.Command(
    target = '$site/worg.css',
    source = 'css/worg.css',
    action = 'cp $SOURCE $TARGET'
    )

for post in posts:
    basename = path.splitext(path.basename(post))[0]
    metadata = env.properties(
        target = '$build/{}.json'.format(basename),
        source = post
        )
    
    page = env.Command(
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
    Depends(page, ['bin/build-page.el','post-template.org'])
    
index = env.Command(
    target = '$site/index.html',
    source = 'index.org',
    action = (
        'POSTS="{}" '
        'emacs --batch --no-init-file '
        '--script bin/combine-posts.el '
        '-org-src $SOURCE '
        '-html $TARGET ').format(' '.join(posts))
    )
