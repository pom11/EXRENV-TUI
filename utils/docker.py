from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import Reactive
from textual import events
from rich.table import Table
from rich.panel import Panel
import rich.box as box
import math
import docker 

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return f"{s}{size_name[i]}"

class DockerInfo(Widget):

	def getDocker(self):
		client = docker.from_env()
		info = client.info()
		client.close()
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

	def container(self):
		try:
			client = docker.from_env()
			container = client.containers.get(self.id)
			status = container.status()
			client.close()
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

	def on_mount(self):
		self.set_interval(3, self.refresh)

	def getContainers(self) -> Table:
		client = docker.from_env()
		containers = client.containers.list()
		client.close()
		table = Table(show_header=False, header_style='bold magenta', show_lines=False, box=box.HEAVY)
		table.add_column("Container", style="dim", justify="left")
		table.add_column("Name", style="dim", justify="left")
		table.add_column("Status", style="dim", justify="left")
		table.add_column("CPU %", style="dim", justify="left")
		table.add_column("MEM USAGE / LIMIT", style="dim", justify="left")
		table.add_column("MEM %", style="dim", justify="left")
		table.add_column("NET I/O", style="dim", justify="left")
		for c in containers:
			if 'exrproxy-env' in c.name:
				stats = c.stats(stream=False)
				usagedelta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
				systemdelta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
				len_cpu = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
				cpu = str(round((usagedelta / systemdelta) * len_cpu * 100, 2))+ "%"
				ram_limit = convert_size(stats['memory_stats']['limit'])
				ram_usage = convert_size(stats['memory_stats']['usage'])
				ram = ram_usage+" / "+ram_limit
				ram_precent = str(round(stats['memory_stats']['usage']/stats['memory_stats']['limit'],2)*100)+"%"
				net_t = convert_size(stats['networks']['eth0']['tx_bytes'])
				net_r = convert_size(stats['networks']['eth0']['rx_bytes'])
				net = net_r+" / "+net_t
				table.add_row(c.short_id, c.name[13::], c.status, cpu, ram, ram_precent, net)
		return table

	def render(self):
		table = self.getContainers()
		return Static(renderable=table)



