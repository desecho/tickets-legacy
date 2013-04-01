import os
here = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))

print(here('static'))
