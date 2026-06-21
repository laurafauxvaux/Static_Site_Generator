# Static Site Generator

A static site generator written in Python as part of the Boot.dev backend curriculum.

## What It Does:
- Converts Markdown files to HTML
- Supports headings, lists, blockquotes and code blocks
- Supports inline formatting (bold, italic, code, links and images)
- Recursively generates pages from a content directory
- Copies static files (CSS and images) automatically
- Supports GitHub Pages deployment

## How It's Made:
Technologies used: Python, HTML
Python libraries :
- pathlib
- os
- shutil

## How To Run:
##### Locally
Generate the site with the default base path and launch a local web server:

```bash
./main.sh
```

##### To Deploy to GitHub Pages
Generate the site with the `/Static_Site_Generator/` base path:

```bash
./build.sh
```

Commit and push the generated files:

```bash
git add .
git commit -m "Update site"
git push
```


## What I learned
- Recursive directory traversal
- Markdown to HTML conversion
- Regex
- Unittest
- Path manipulation with pathlib
- GitHub Pages deployment
- Overall, how to research and understand the Python documentation
