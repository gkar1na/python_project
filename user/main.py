import sys
import os
sys.path.append(os.getcwd().rsplit(os.sep, maxsplit=1)[0])


if __name__ == '__main__':
    import work
    work.create_window()
