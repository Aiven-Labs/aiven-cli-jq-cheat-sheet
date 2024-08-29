import dataclasses
import json
import pathlib

from textual.app import App
from textual.screen import Screen
from textual.widgets import MarkdownViewer, Footer, OptionList, Markdown 

import typer


typer = typer.Typer()


@dataclasses.dataclass
class Entry:
    command: str
    title: str
    description: str
    output: str

    def __str__(self):
        return f"""
## {self.title}

`{self.command}`

{self.description}

### Example Output:

```sh
> {self.command}
{self.output}
```
"""

    def __repr__(self):
        return self.__str__()


JSON_PATH = pathlib.Path("data/user.json")
JSON_ENTRIES = [Entry(**entry) for entry in json.loads(JSON_PATH.read_text())]

WELCOME_TEXT = """ # Welcome to the Aiven CLI + JQ CookBook"""


    class Recipe(Static):



class OptionScreen(Screen):
    """Displays the selection list for a Section"""

    action_enter(self):
        self.app.push_screen()

    def compose(self):
        yield OptionList(*[entry.title for entry in JSON_ENTRIES])


class CookBook(App):

    BINDINGS = [
        ("q", "quit", "Immediately Close the Program"),
        ("a", "all_cookbooks"),
        ("f", "focus"),
        ("c", "copy"),
        ("s", "select"),
    ]

    def action_select(self):
        self.push_screen(OptionScreen())

    def compose(self):
        """Given a filename"""
        yield MarkdownViewer(
            WELCOME_TEXT, show_table_of_contents=False, id="main_window"
        )
        yield Footer()

    def action_quit(self):
        self.exit()


if __name__ == "__main__":
    CookBook().run()
