#!/usr/bin/env python
import os
import sys

# Auto-load virtual env
#if os.path.exists("venv"):
#    activate_this = "venv/bin/activate_this.py"
#    execfile(activate_this, dict(__file__=activate_this))

# Auto-load environment variables
if os.path.exists(".env"):
    with open(".env", "r") as f:
        print "Loading .env"
        for line in f.readlines():
            try:
                k,v = [x.strip() for x in line.split("=", 2)]
                if k != "":
                    print "--> Setting %s" % k
                    os.environ[k] = v
            except ValueError:
                pass

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinheiro.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
