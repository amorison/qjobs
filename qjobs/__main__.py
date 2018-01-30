"""Make qjobs a callable module."""

from . import core, cmdargs


def main():
    """qjobs entry point"""
    subcmd = cmdargs.parse()
    core.main(subcmd)


if __name__ == '__main__':
    main()
