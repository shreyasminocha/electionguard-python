from typing import Any
import click


class E2eStepBase:
    """
    Responsible for providing common functionality to the individual steps within an end-to-end election command
    from the CLI.
    """

    header_color = "green"
    value_color = "yellow"

    def print_header(self, s: str) -> None:
        click.secho(f"{'-'*40}", fg=self.header_color)
        click.secho(s, fg=self.header_color)
        click.secho(f"{'-'*40}", fg=self.header_color)

    def print_value(self, name: str, value: Any) -> None:
        click.echo(click.style(name + ": ") + click.style(value, fg=self.value_color))
