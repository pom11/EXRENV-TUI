from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style

from textual import events
from textual.app import App
from textual.widgets import Placeholder, ScrollView, Static
from textual.reactive import Reactive
from textual.widget import Widget
from utils.footer import CustomFooter
from utils.header import CustomHeader
from utils.system import CPUUsage, DISKUsage, RAMUsage, SystemInfo

pretty.install()


class Main(App):
    """An example of a very simple Textual App"""

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        # await self.bind("h", "view.toggle('sidebar')", "Help")
        await self.bind("q", "quit", "Quit")


    async def on_mount(self, event: events.Mount) -> None:
        grid = await self.view.dock_grid(edge='left')
        for i in range(40):
            # if i == 0:
                # grid.add_column(fraction=1, name=f"c{i+1}", max_size=20, size=0)
            # else:
            grid.add_column(fraction=1, name=f"c{i+1}")
        for i in range(40):
            grid.add_row(fraction=1, name=f"r{i+1}")


        grid.add_areas(
            area1="c1-start|c40-end,r1",
            area2="c1-start|c40-end,r40",
            area3="c11-start|c15-end,r3-start|r4-end",
            area4="c16-start|c20-end,r5-start|r6-end",
        )

        grid.place(
            area1 = CustomHeader(),
            area2 = CustomFooter(),
            area3 = CPUUsage(),
            area4 = DISKUsage()
            )

        grid.set_align("stretch", "center")

    # async def on_mount(self, event: events.Mount) -> None:
    #     """Create and dock the widgets."""

    #     # A scrollview to contain the markdown file
    #     body = ScrollView(gutter=1)

    #     # Header / footer / dock
    #     await self.view.dock(CustomHeader(), edge="top")
    #     await self.view.dock(CustomFooter(), edge="bottom")
    #     # await self.view.dock(Placeholder(), edge="left", size=30, name="sidebar")
    #     await self.view.dock(body, edge="left", size=30, name="sidebar")

    #     # Dock the body in the remaining space
    #     await self.view.dock(SystemInfo(), RAMUsage(), CPUUsage(), DISKUsage(), edge="left")
        


    #     async def get_markdown(filename: str) -> None:
    #         with open(filename, "rt") as fh:
    #             readme = Markdown(fh.read(), hyperlinks=True)
    #         await body.update(readme)

    #     await self.call_later(get_markdown, "/Users/desac/Documents/BLOCKNET/exrproxy-env/README.md")

if __name__ == '__main__':
    Main.run(title="EXRPROXY-ENV", log="dashboard.log")