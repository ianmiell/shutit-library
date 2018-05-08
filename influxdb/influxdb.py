
# Created from dockerfile: /space/git/dockerfiles_repos/Dockerfiles/influxdb/Dockerfile
from shutit import shutit_module

class influxdb(shutit_module.ShutItModule):

	def build(self, shutit):
		shutit.install('wget')
		shutit.send('mkdir -p /')
		shutit.send('wget -O /influxdb_latest_amd64.deb http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb')
		shutit.send('dpkg -i /influxdb_latest_amd64.deb')
		return True

def module():
		return influxdb(
				'shutit.tk.influxdb.influxdb', 0.1212353,
				depends=['shutit.tk.setup']
		)
