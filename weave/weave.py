"""ShutIt module. See http://shutit.tk
"""

from shutit import shutit_module


class weave(shutit_module.ShutItModule):

	def build(self, shutit):
		#shutit.install('conntracker')
		shutit.install('wget')
		shutit.install('ethtool')
		shutit.send('wget -O /usr/local/bin/weave https://raw.githubusercontent.com/zettio/weave/master/weave')
		shutit.send('chmod a+x /usr/local/bin/weave')
		return True

	def start(self, shutit):
		# TODO: this is synchronous
		#shutit.send('weave launch')
		return True

	def stop(self, shutit):
		#shutit.send('weave stop')
		return True

def module():
	return weave(
		'shutit.tk.weave.weave', 0.397382568,
		description='',
		maintainer='',
		depends=['shutit.tk.setup','shutit.tk.docker.docker']
	)

