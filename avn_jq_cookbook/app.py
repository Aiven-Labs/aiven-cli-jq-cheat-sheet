import dataclasses
import importlib
import json
import pathlib

import typer
from textual.app import App
from textual.widgets import Footer, Header, MarkdownViewer, Tabs

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


ROOT_JSON_DIRECTORY = importlib.resources.files() / pathlib.Path("data")
JSON_PATHS = sorted(entry.stem.title() for entry in ROOT_JSON_DIRECTORY.iterdir())

WELCOME_TEXT = """ # Welcome to the Aiven CLI + JQ CookBook"""


def load_entries(command_option) -> str:
    json_path = ROOT_JSON_DIRECTORY / pathlib.Path(command_option.lower()).with_suffix(
        ".json"
    )
    entries = [str(Entry(**entry)) for entry in json.loads(json_path.read_text())]
    return "\n\n".join(entries)


class CookBook(App):
    active_command_option = "user"
    TITLE = "Aiven CLI + JQ Cheat Sheet"

    BINDINGS = [
        ("q", "quit", "Close the Program"),
    ]

    def compose(self):
        """Given a filename"""
        yield Header()
        yield Tabs(*[path for path in JSON_PATHS], id="selection-tab")
        yield MarkdownViewer(id="markdown-viewer")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        viewer = self.query_one("#markdown-viewer")
        viewer.document.update(load_entries(str(event.tab.label)))

    def action_quit(self):
        self.exit()


def app():
    cookbook = CookBook()
    cookbook.run()


if __name__ == "__main__":
    app()
