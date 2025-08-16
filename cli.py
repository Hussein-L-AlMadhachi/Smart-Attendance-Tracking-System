import sys

import service.register
import service.monitor


mode = sys.argv[1]

if mode == "register":
    service.register.register_faces()

elif mode == "monitor":
    service.monitor.monitor_faces_headless()



