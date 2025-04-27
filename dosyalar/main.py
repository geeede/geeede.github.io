""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

js_code = r"""
    <script>
      (async () => {
        const response = await fetch('https://api.github.com/repos/:user/:repo/contents/');
        const data = await response.json();
        let htmlString = '<ul>';
        for (let file of data) {
          htmlString += `<li><a href="${file.path}">${file.name}</a></li>`;
        }
        htmlString += '</ul>';
        document.getElementsByTagName('body')[0].innerHTML = htmlString;
      })()
    </script>"""

INDEX_TEMPLATE = r"""
<html>
<body>
${javascript_code}
<h2>${header}</h2>
<p>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</p>
</body>
</html>
"""

EXCLUDED = ['index.html']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED]
    header = (args.header if args.header else os.path.basename(args.directory))
    
    generated_html = Template(INDEX_TEMPLATE).render(names=fnames, header=header,javascript_code=js_code)
    open("index.html","w+").write(generated_html)

if __name__ == '__main__':
    main()