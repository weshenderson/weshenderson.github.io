# weshenderson.info
The personal webpage of Wes Henderson.

## Layout
The core of this site is powered by static resources, e.g. HTML, CSS, etc in a link tree format and is hosted with GitHub Pages. See the [Resume](#Resume) section for the fun stuff.

## Resume
The `/resume` path uses Jekyll as the templating engine. Additionally, pre-commit hooks export a [PDF copy](https://weshenderson.info/docs/resume.pdf) via [Pandoc](https://pandoc.org) as well as an alternate version dubbed `konami_resume`. This allows me to effectively separate the content from the format and maintain 3 version via 1 markdown file.

### Local Testing
For local development I am using a container [image](https://hub.docker.com/r/bretfisher/jekyll-serve) created by [Bret Fisher](https://github.com/BretFisher). From the root of the repo simply run:

```
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

The local site can be viewed at [http://localhost:4000/](http://localhost:4000/).

**Note:** Changes to `_config.yml` require a reload of the server.

### Hooks and Easter Eggs

The pre-commit hook generates a "konami resume template" if `resume.md` is updated. The Konami template uses a different layout in order to give the resume a retro vibe. To view this version simply enter the Konami Code on `/resume`:

```
up, up, down, down, left, right, left, right, b, a
```
