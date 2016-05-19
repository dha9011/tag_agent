""" Setting for gunicorn.

    Refer to http://docs.gunicorn.org/en/latest/settings.html#settings for more.
"""

import os
import multiprocessing

# A string of the form: HOST, HOST:PORT, unix:PATH. An IP is a valid HOST.
bind = '0.0.0.0:5005'

# backlog = 2048

workers = 3
# workers = multiprocessing.cpu_count() * 2 + 1

# The type of workers to use.
#     sync
#     eventlet - Requires eventlet >= 0.9.7
#     gevent - Requires gevent >= 0.13
#     tornado - Requires tornado >= 0.2
worker_class = 'gevent'

# The number of worker threads for handling requests.
# Run each worker with the specified number of threads.
threads = workers

# The maximum number of simultaneous clients,
# ONLY affects Eventlet and Gevent worker type.
# worker_connections = 1000

# The maximum number of requests a worker will process before restarting.
# Any value > 0 will limit the number of requests a work will process before automatically restarting.
# This is a simple method to help limit the damage of memory leaks.
# If this is set to 0(the default) then it will be disabled.
max_requests = threads


# Workers silent for more than this many seconds are killed and restarted.
timeout = 30

# Timeout for graceful workers restart.
# graceful_timeout = 30

# The number of seconds to wait for requests on a Keep Alive connection.
# keepalive = 2

# Load application code before the worker processes are forked.
preload_app = True

# chdir = '/opt/autoplat/servive_ctrl'
chdir = os.path.dirname(os.path.abspath(__file__))

# Daemonize the Gunicorn process.
daemon = False

# Environment variableL: ['key=val', 'key1=val1']
raw_env = ['FOO=1', 'BAR=2']

# Access log and format.
accesslog = '/data/logs/tag.log'
errorlog = '/data/logs/tag.err'

# Log format.
access_log_format = '%(h)s %(l)s %(t)s %(r)s %(s)s %(b)s %(L)s(s) %(f)s "%(a)s"'

# Error log file.
# '-' means log to stderr.
# errorlog = '/tmp/sc_api.error'

# Process Name

# NOTE: `pip install setproctitle` is needed
proc_name = 'tag'
