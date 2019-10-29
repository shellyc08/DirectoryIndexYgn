import sys
import site
import os

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__), 'env/local/lib64/python2.7/site-packages'))

# Path of execution
sys.path.append('/var/www/vhosts/yangonindex')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))
 
# import server  as application
from server import app as application

