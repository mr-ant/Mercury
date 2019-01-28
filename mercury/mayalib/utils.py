
def isMaya():
    try:
        from maya import cmds
        return True
    except ImportError:
        return False
