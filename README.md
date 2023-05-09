# weshenderson.info
The personal webpage of Wes Henderson.

## Layout
This site is powered by [Alea](https://github.com/necrux/alea) and hosted with GitHub Pages. Alea is the templating engine that creates `index.html` and `resume.html` based off of their respective yaml config files. Otherwise it is very straight-forward HTML and CSS in a link tree style format.

## Hooks
This repo relies heavily on pre-commit hooks to auto-generate new resources whenever certain files are updated. This is especially important for my resume as I would otherwise have to maintain 3 versions: the HTML version, the PDF version, and the super secret version (see [below](#hooks-and-easter-eggs)). This allows me to effectively separate the content from the format and maintain 3 version via 1 yaml file.

**PDF Resume**

The PDF version of my resume is generated via Google Chrome dev tools:

```
/usr/bin/google-chrome \
            --headless \
            --disable-gpu \
            --no-pdf-header-footer \
            --no-margins \
            --run-all-compositor-stages-before-draw \
            --print-to-pdf=${PDF} \
```

Previously this work was done via Pandoc, however this results in a prettier end product without having to also create LateX templates as Chrome renders the underlying CSS.


### Hooks and Easter Eggs

The pre-commit hook generates a "Konami resume template" if `resume.yaml` is updated. The Konami template uses a different layout in order to give the resume a retro vibe. To view this version simply enter the Konami Code on [/resume](https://www.weshenderson.info/resume):

```
up, up, down, down, left, right, left, right, b, a
```
