import click

from pyconfman.plug_cli import add_config_cli


def test_command():
    @click.group
    def my_cli():
        """ciao"""
    assert my_cli.name == 'my-cli'
    my_cli = add_config_cli(my_cli)


if __name__ == '__main__':
    @click.group
    def my_cli():
        """ciao"""

    add_config_cli(my_cli)
    my_cli()
