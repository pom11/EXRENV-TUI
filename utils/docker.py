from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import Reactive
from textual import events
from rich.table import Table
from rich.panel import Panel
import rich.box as box

class DockerInfo(Widget):

	def __init__(self, client):
		super().__init__(client = client)
		self.client = client

	def getDocker(self):
		info = self.client.info()
		table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
		table.add_column("Docker", style="dim", justify="left")
		table.add_column("", justify="left")
		if info == False:
			table.add_row("installed", str(info))
		else:
			data = {}
			data['NCPU'] = str(info['NCPU'])
			data['MemTotal'] = str(round(info['MemTotal']/ (1024.0 **3)))+" GB"
			data['Images'] = str(info['Images'])
			data['Containers'] = str(info['Containers'])
			data['Running'] = str(info['ContainersRunning'])
			data['Paused'] = str(info['ContainersPaused'])
			data['Stopped'] = str(info['ContainersStopped'])
			for k, v in data.items():
				table.add_row(k, v)
		return table

	def on_mount(self):
		self.set_interval(1, self.refresh)

	def render(self):
		table = self.getDocker()
		return Static(renderable=table)


class ContainerKill(Widget):

	mouse_over = Reactive(False)

	def __init__(self, client, id):
		super().__init__(client=client, id=id)
		self.client = client
		self.id = id

	def container(self):
		try:
			container = self.client.containers.get(self.id)
			status = container.status()
			return status
		except Exception as e:
			return "Error"

	def on_mount(self):
		self.set_interval(1, self.refresh)

	def render(self):
		data = self.container()
		return Panel(data, style=("on red" if self.mouse_over else ""))



class DockerContainerStats(Widget):

	mouse_over = Reactive(False)

	def __init__(self, client):
		super().__init__(client=client)
		self.client = client

	def on_mount(self):
		self.set_interval(1, self.refresh)

	def getContainers(self) -> Table:
		containers = self.client.containers.list()
		table = Table(show_header=False, header_style='bold magenta', show_lines=False, box=box.HEAVY)
		table.add_column("Container", style="dim", justify="left")
		table.add_column("Name", style="dim", justify="left")
		table.add_column("Status", style="dim", justify="left")
		for c in containers:
			table.add_row(c.short_id, c.name[13::], ContainerKill(self.client, c.id))
		return table

	def render(self):
		table = self.getContainers()
		return Static(renderable=table)



