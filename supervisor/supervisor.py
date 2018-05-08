
# Created from dockerfile: /tmp/supervisor/Dockerfile
from shutit import shutit_module

class supervisor(shutit_module.ShutItModule):

	def build(self, shutit):
		shutit.send('echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list')
		shutit.send('apt-get update')
		shutit.install('supervisor')
		shutit.send('mkdir -p /var/log/supervisor')
		shutit.send_host_file('/etc/supervisor/conf.d/supervisord.conf', 'context/supervisord.conf')
		return True

def module():
		return supervisor(
				'shutit.tk.supervisor.supervisor', 0.0001,
				depends=['shutit.tk.setup']
		)
