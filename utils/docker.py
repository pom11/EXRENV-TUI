from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import Reactive
from textual import events
from rich.table import Table
from rich.panel import Panel
import rich.box as box
import math
from docker import DockerClient
from python_on_whales import docker as pwhales

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return f"{s}{size_name[i]}"

# class DockerInfo(Widget):

# 	def __init__(self, client: DockerClient, refresh_rate: int) -> None:
# 		self.client = client
# 		self.refresh_rate = refresh_rate
# 		super().__init__()

# 	def getDocker(self):
# 		# client = docker.from_env()
# 		info = self.client.info()
# 		# client.close()
# 		table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
# 		table.add_column("Docker", style="dim", justify="left")
# 		table.add_column("", justify="left")
# 		if info == False:
# 			table.add_row("installed", str(info))
# 		else:
# 			data = {}
# 			data['NCPU'] = str(info['NCPU'])
# 			data['MemTotal'] = str(round(info['MemTotal']/ (1024.0 **3)))+" GB"
# 			data['Images'] = str(info['Images'])
# 			data['Containers'] = str(info['Containers'])
# 			data['Running'] = str(info['ContainersRunning'])
# 			data['Paused'] = str(info['ContainersPaused'])
# 			data['Stopped'] = str(info['ContainersStopped'])
# 			for k, v in data.items():
# 				table.add_row(k, v)
# 		return table

# 	def on_mount(self):
# 		self.set_interval(self.refresh_rate, self.refresh)

# 	def render(self):
# 		table = self.getDocker()
# 		return Static(renderable=table)


class ContainerKill(Widget):

	def __init__(self, client: DockerClient, refresh_rate: int) -> None:
		self.client = client
		self.refresh_rate = refresh_rate
		super().__init__()	

	mouse_over = Reactive(False)

	def container(self):
		try:
			# client = docker.from_env()
			container = self.client.containers.get(self.id)
			status = container.status()
			# client.close()
			return status
		except Exception as e:
			return "Error"

	def on_mount(self):
		self.set_interval(self.refresh_rate, self.refresh)

	def render(self):
		data = self.container()
		return Panel(data, style=("on red" if self.mouse_over else ""))



class DockerContainerStats(Widget):

	def __init__(self, client: DockerClient, refresh_rate: int) -> None:
		self.client = client
		self.refresh_rate = refresh_rate
		super().__init__()

	mouse_over = Reactive(False)

	def on_mount(self):
		self.set_interval(self.refresh_rate, self.refresh)

	def getContainers(self) -> Table:
		# client = docker.from_env()
		# containers = self.client.containers.list()
		containers = pwhales.stats()
		info = self.client.info()
		# client.close()
		table = Table(show_header=False, show_lines=False, box=box.HEAVY)
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",
		table.add_column("", no_wrap=False, justify="left") # style="dim",

		table.add_row('[bold magenta]NCPU', '[bold magenta]MemTotal', '[bold magenta]Images', '[bold magenta]Containers', '[bold magenta]Running', '[bold magenta]Paused', '[bold magenta]Stopped')
		if info == False:
			table.add_row("installed", str(info))
		else:
			table.add_row('[bold cyan]'+str(info['NCPU']), '[bold cyan]'+str(round(info['MemTotal']/ (1024.0 **3)))+" GB", '[bold cyan]'+str(info['Images']), '[bold cyan]'+str(info['Containers']), '[bold cyan]'+str(info['ContainersRunning']), '[bold cyan]'+str(info['ContainersPaused']), '[bold cyan]'+str(info['ContainersStopped']))

		table.add_row("[bold magenta]Container", "[bold magenta]Name", "[bold magenta]Status", "[bold magenta]CPU %", "[bold magenta]MEM USAGE / LIMIT", "[bold magenta]MEM %", "[bold magenta]NET I/O")
		for c in containers:
			if 'exrproxy-env' in c.container_name:
				# stats = c.stats(stream=False)
				# usagedelta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
				# systemdelta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
				# len_cpu = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
				# cpu = str(round((usagedelta / systemdelta) * len_cpu * 100, 2))+ "%"
				# ram_limit = convert_size(stats['memory_stats']['limit'])
				# ram_usage = convert_size(stats['memory_stats']['usage'])
				# ram = ram_usage+" / "+ram_limit
				# ram_precent = str(round(stats['memory_stats']['usage']/stats['memory_stats']['limit'],2)*100)+"%"
				# net_t = convert_size(stats['networks']['eth0']['tx_bytes'])
				# net_r = convert_size(stats['networks']['eth0']['rx_bytes'])
				# net = net_r+" / "+net_t
				# table.add_row('[bold cyan]'+c.short_id, '[bold cyan]'+c.name[13::], '[bold cyan]'+c.status, '[bold cyan]'+cpu, '[bold cyan]'+ram, '[bold cyan]'+ram_precent, '[bold cyan]'+net)
				table.add_row('[bold cyan]'+c.container, '[bold cyan]'+c.container_name, '', '[bold cyan]'+c.cpu_percentage, '', '[bold cyan]'+c.memory_percentage, '')
		return table

	def render(self):
		table = self.getContainers()
		return Static(renderable=table)



