#!C:\Users\nueof\PycharmProjects\django-project\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'IntelliCoder==0.5.2','console_scripts','ic'
__requires__ = 'IntelliCoder==0.5.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('IntelliCoder==0.5.2', 'console_scripts', 'ic')()
    )
