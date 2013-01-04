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
vars.Add('site', 'html output', ARGUMENTS.get('site', 'site'))
vars.Add('build', 'compiled post bodies', ARGUMENTS.get('build', 'build'))

env = Environment(ENV=environ, variables=vars)
env['BUILDERS']['properties'] = Builder(action = get_properties)

posts = [p for p in glob.glob('posts/*.org') if '/_' not in p]

css_worg = env.Command(
    target = '$site/worg.css',
    source = 'css/worg.css',
    action = 'cp $SOURCE $TARGET'
    )

pages = []
# process all individual posts
properties = []
for post in posts:
    basename = path.splitext(path.basename(post))[0]
    props, = env.properties(
        target = '$build/{}.json'.format(basename),
        source = post)
    properties.append(str(props))

    body, = env.Command(
        target = '$build/{}.html'.format(basename),
        source = ['bin/export-body.el', post],
        action = ('emacs --batch --no-init-file '
                  '--script ${SOURCES[0]} -post ${SOURCES[1]} '
                  '-html-body $TARGET '
                  '&> emacs.log'
                  )
        )
    Depends(body, ['bin/common.el'])

    page, = env.Command(
        target = '$site/%s.html' % basename,
        source = ['bin/combine-posts.el', 'post.org'],
        action = (
            'POSTS="%s" '
            'emacs --batch --no-init-file '
            '--script ${SOURCES[0]} -org-src ${SOURCES[1]} '
            '-html $TARGET '
            '&> emacs.log'
            ) % basename
        )
    Depends(page, [body, 'bin/common.el'])
    pages.append(page)
    
# combined posts
if not all(path.exists(p) for p in properties):
    print 'run scons again to build combined pages'
else:
    metadata = [get_json(p) for p in properties]
    metadata.sort(key = lambda d: d['date'], reverse = True)

    # tag line to be included in all combined pages
    tags_body, = env.Command(
        target = '$build/tags.html',
        source = ['bin/export-body.el', 'tags.org'],
        action = ('emacs --batch --no-init-file '
                  '--script ${SOURCES[0]} -post ${SOURCES[1]} '
                  '-html-body $TARGET '
                  '&> emacs.log'
                  )
        )
    Depends(tags_body, ['bin/common.el'] + properties + pages)

    tags = collections.defaultdict(list)
    tags['index'] = metadata
    for d in metadata:
        for tag in d['tags'].split(','):
            tags[tag].append(d)

    for tag, posts in tags.items():
        page, = env.Command(
            target = '$site/%s.html' % tag,
            source = ['bin/combine-posts.el', 'index.org'],
            action = (
                'POSTS="%s" '
                'emacs --batch --no-init-file '
                '--script ${SOURCES[0]} -org-src ${SOURCES[1]} '
                '-html $TARGET '
                '&> emacs.log'
                ) % ' '.join(d['basename'] for d in posts)
            )
        Depends(page, ['bin/common.el','bin/combine-posts.el', tags_body] + \
                    [d['body'] for d in posts])
        pages.append(page)
        
# publish the compiled pages
publish = env.Command(
    target = 'publish.log',
    source = pages,
    action = ('rsync -rv --exclude .git --delete $site/ ../blog-publish && '
              'cd ../blog-publish && '
              'git commit -a -m "publishing" && '
              'git push origin gh-pages | tee $TARGET')
    )
Alias('publish', publish)
Ignore('.', publish)
