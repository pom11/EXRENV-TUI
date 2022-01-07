from textual.widget import Widget
from textual.widgets import Static
from textual import events
from rich.table import Table
import rich.box as box
import platform, socket, re, uuid, psutil, requests

def externalIP():
    try:
        req = requests.get('http://checkip.amazonaws.com')
        req = req.text
        return req[:-2]
    except Exception as e:
        try:
            req = requests.get('http://ifconfig.co')
            req = req.text.split('code')[3].split('>')[1].split('<')[0]
            return req
        except Exception as e:
            return ''

extIP = externalIP()

class SystemInfo(Widget):

    def getSystemInfo(self):
        table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
        table.add_column("System", style="dim", justify='left')
        table.add_column("", justify='left')
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = extIP
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        for k, v in info.items():
            table.add_row(k,v)
        return table

    def render(self):
        table = self.getSystemInfo()
        return Static(renderable=table)


class RAMUsage(Widget):

    def getCurrentUsage(self):
        table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
        table.add_column("RAM", style="dim", justify='left')
        table.add_column("", justify='left')
        info = {}
        info['total'] = '{:.2f}'.format(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['free'] = '{:.2f}'.format(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)+ " %"
        info[''] = '{:.2f}'.format(round(psutil.virtual_memory().available / (1024.0 **3)))+" GB"
        info['used'] = '{:.2f}'.format(psutil.virtual_memory().used * 100 / psutil.virtual_memory().total)+ " %"
        info[' '] = '{:.2f}'.format(psutil.virtual_memory().used / (1024.0 **3))+" GB"
        for k, v in info.items():
            table.add_row(k,v)
        return table

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        table = self.getCurrentUsage()
        return Static(renderable=table)


class CPUUsage(Widget):

    def getCurrentUsage(self):
    
        table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
        table.add_column("CPU  ", style="dim", justify='left')
        table.add_column("", justify='left')
        info = {}
        info['used'] = '{:.2f}'.format(round(psutil.cpu_percent()))+" %"
        for k, v in info.items():
            table.add_row(k,v)
        return table

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        table = self.getCurrentUsage()
        return Static(renderable=table)


class DISKUsage(Widget):

    def getCurrentUsage(self):
        table = Table(show_header=True, header_style='bold magenta', show_lines=False, box=box.HEAVY)
        table.add_column("DISK", style="dim", justify='left')
        table.add_column("", justify='left')
        hdd = psutil.disk_usage('/')
        info = {}
        info['total'] = '{:.2f}'.format(hdd.total / (2**30))+" GB"
        info['free'] = '{:.2f}'.format(hdd.free * 100 / hdd.total)+ " %"
        info[''] = '{:.2f}'.format(hdd.free / (2**30))+" GB"
        info['used'] = '{:.2f}'.format(hdd.used * 100 / hdd.total)+ " %"
        info[' '] = '{:.2f}'.format(hdd.used / (2**30))+" GB"
        for k, v in info.items():
            table.add_row(k,v)
        return table

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        table = self.getCurrentUsage()
        return Static(renderable=table)
