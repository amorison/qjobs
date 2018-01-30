"""Make qjobs a callable module."""

from . import commands


def main():
    """qjobs entry point"""
    subcmd = commands.parse()
    commands.main(subcmd)


if __name__ == '__main__':
    main()
