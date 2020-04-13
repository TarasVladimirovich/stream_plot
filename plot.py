from sys import argv

from builder import Builder

if __name__ == '__main__':
    builder = Builder(argv[1:])
    builder.create_file()
    print('Done')
