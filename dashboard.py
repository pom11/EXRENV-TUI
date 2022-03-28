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
from utils.docker import DockerInfo, DockerContainerStats

import docker
import sys

try:
    docker_client = docker.from_env()
except Exception as e:
    print("Docker daemon error. Please install docker to continue")
    sys.exit(0)
    

class Main(App):

    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")


    async def on_mount(self, event: events.Mount) -> None:
        grid = await self.view.dock_grid(edge='left')
        
        for i in range(40):
            grid.add_column(name=f"c{i+1}")
        for i in range(40):
            grid.add_row(name=f"r{i+1}")
        
        grid.add_areas(
            area1="c1-start|c40-end,r1",
            area2="c1-start|c40-end,r40",
            area3="c1-start|c15-end,r2-start|r10-end",
            area4="c16-start|c19-end,r2-start|r7-end",
            area5="c16-start|c19-end,r8-start|r12-end",
            area6="c20-start|c23-end,r2-start|r7-end",
            area7="c23-start|c26-end,r8-start|r14-end",
            area8="c1-start|c22-end,r11-start|r35-end",
        )
        for i in range(8):
            grid.set_align("stretch", f"area{i+1}")

        grid.place(
            area1 = CustomHeader(),
            area2 = CustomFooter(),
            area3 = SystemInfo(),
            area4 = RAMUsage(),
            area5 = CPUUsage(),
            area6 = DISKUsage(),
            area7 = DockerInfo(client=docker_client, refresh_rate=10),
            area8 = DockerContainerStats(client=docker_client, refresh_rate=10),
            )


if __name__ == '__main__':
    Main.run(title="EXRPROXY-ENV", log="dashboard.log")