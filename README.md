# mdpytree

## usage
```
from mdpytree import Node

md = open("MARKDOWN_FILE", "r").read()
toc = Node.fromMarkdown(md)
```