import glob
from os import path, environ

vars = Variables()
vars.Add('site', 'html output',
         ARGUMENTS.get('site', 'site'))
vars.Add('build', 'compiled post bodies',
         ARGUMENTS.get('build', 'build'))

env = Environment(ENV=environ, variables=vars)

posts = glob.glob('posts/*.org')

css_worg = env.Command(
    target = '$site/worg.css',
    source = 'css/worg.css',
    action = 'cp $SOURCE $TARGET'
    )

for post in posts:
    basename = path.splitext(path.basename(post))[0]
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
