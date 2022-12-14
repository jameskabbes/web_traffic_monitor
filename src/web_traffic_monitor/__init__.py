import dir_ops as do
import os

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = do.Dir( do.get_cwd() )

# Custom RTI dependency
from .Base import Base

from .Columns import Columns 
# Column dependencies
from .Tables import Tables
from . import queries
from . import utils

from .Redirect import Redirect
from .Visit import Visit

from .Redirects import Redirects
from .Visits import Visits

from .Slug import Slug
from .Slugs import Slugs

from .Monitor import Monitor
from .FlaskMonitor import FlaskMonitor
