# weshenderson.github.io
The personal webpage of Wes Henderson.

## Layout
This site is primarily powered by static resources, e.g. HTML, CSS, etc. However I am also experimenting with Jekyll as the templating engine; this can be seen via `/resume`.

## Local Testing
For local development I am using a container [image](https://hub.docker.com/r/bretfisher/jekyll-serve) created by [Bret Fisher](https://github.com/BretFisher). From the root of the repo simply run `docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve` and navigate to [http://localhost:4000/](http://localhost:4000/).
