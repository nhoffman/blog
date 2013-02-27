import sys
import glob
import json
import pprint
import collections
from os import path, environ

from pythings import read_json, org_properties, tagdict

def get_properties(target, source, env):
    """
    A Builder action to write a json file to `target` serializing a
    dict of values taken from all PROPERTIES drawers in org-mode file
    `source` plus keys 'basename','org','body','html'. Uses scons
    environment variables '$build' (for html bodies) and '$site' (for
    complete pages).
    """

    org, = map(str, source)
    basename = path.splitext(path.basename(org))[0]

    d = dict(
        org_properties(org),
        basename = basename,
        org = org,
        body = env.subst('$build/{}.html'.format(basename)),
        html = env.subst('$site/{}.html'.format(basename))
        )

    with open(str(target[0]), 'w') as out:
        json.dump(d, out, sort_keys=True, indent = 4)

# variables defining destination for output files; can be redefined
# from the command line, eg "scons site=path/to/output"
vars = Variables()
vars.Add('posts', 'org-mode source files', ARGUMENTS.get('posts', 'posts'))
vars.Add('build', 'compiled post bodies', ARGUMENTS.get('build', 'build'))
vars.Add('site', 'final html output', ARGUMENTS.get('site', 'site'))

env = Environment(ENV=environ, variables=vars)
# register the builder that we will use to write json files containing
# metadata for each post.
env['BUILDERS']['properties'] = Builder(action = get_properties)

# list of org-mode fies containing posts
posts = [p for p in glob.glob(env.subst('$posts/*.org')) if '/_' not in p]

# make a copy of stylesheet in directory containing compiled output.
css_worg = env.Command(
    target = '$site/worg.css',
    source = 'css/worg.css',
    action = 'cp $SOURCE $TARGET'
    )
Alias('css', css_worg)

# process all individual posts
properties = [] # json files containing post metadata
pages = [] # compiled html bodies
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
    # body is identified based on vaue of POSTS (in this case, a
    # single basename) but is not provided as a source, so we need to
    # explicitly declare the dependency.
    Depends(page, [body, 'bin/common.el'])
    pages.append(page)

# Build combined posts. We don't know what to include under each tag
# until all of the json files have been written to disk, so we confirm
# that this has been done before proceeding.
if not all(path.exists(p) for p in properties):
    print '\n* run scons again to build combined pages *\n'
else:
    # compile tag line to be included in all combined pages
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

    # metadata is a list of dicts in reverse chronological order; tags
    # is a dictionary providing pages for each tag.
    metadata, tags = tagdict(
        properties, key = lambda d: d['date'], reverse = True)

    # the front page (index.html) contains all of the posts.
    tags['index'] = metadata

    for tag, posts in tags.items():
        page, = env.Command(
            target = '$site/%s.html' % tag,
            source = ['bin/combine-posts.el', 'index.org'],
            action = ('POSTS="%s" '
                      'emacs --batch --no-init-file '
                      '--script ${SOURCES[0]} -org-src ${SOURCES[1]} '
                      '-html $TARGET '
                      '&> emacs.log'
                      ) % ' '.join(d['basename'] for d in posts)
            )
        # again, because we are only indirectly identifying the page
        # bodies to be included via the POSTS environment variable, we
        # need to explicitly identify them.
        Depends(page, ['bin/common.el', tags_body] + [d['body'] for d in posts])
        pages.append(page)

# publish the compiled pages
publish = env.Command(
    target = 'publish.log',
    source = pages,
    action = ('rsync -rv --exclude .git --delete $site/ ../blog-publish && '
              '(cd ../blog-publish && '
              'git commit -a -m "publishing" && '
              'git push origin gh-pages | tee $TARGET)')
    )
Alias('publish', publish)
Ignore('.', publish)
