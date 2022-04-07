
#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from src.session    import SessionEnvironment
from src.commands   import Shell


if __name__ == '__main__':

    session = SessionEnvironment()
    shell = Shell(session)
    shell.cmdloop()
