import glob
from os import path, environ

outdir = ARGUMENTS.get('site', 'site')

vars = Variables()
vars.Add('outdir', 'html output', outdir)
env = Environment(ENV=environ, variables=vars)

posts = glob.glob('posts/*.org')

for post in posts:
    page = env.Command(
        target = path.join(outdir, path.basename(post)).replace('.org','.html'),
        source = post,
        action = ('emacs --batch --no-init-file '
                  '--script bin/export-page.el '
                  '-template post-template.org '
                  '-include $SOURCE '
                  '-html $TARGET ')
        )
    Depends(page, ['bin/export-page.el','post-template.org'])
