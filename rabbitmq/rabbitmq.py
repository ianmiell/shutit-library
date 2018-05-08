
# Created from dockerfile: /space/git/dockerfiles_repos/dockerfiles/rabbitmq/Dockerfile
from shutit import shutit_module

class rabbitmq(shutit_module.ShutItModule):

	def build(self, shutit):
		shutit.install('wget logrotate rabbitmq-server')
		shutit.send('/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management')
		return True

def module():
		return rabbitmq(
				'shutit.tk.rabbitmq.rabbitmq', 0.1523523,
				depends=['shutit.tk.setup']
		)
