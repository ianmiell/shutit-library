# Created from dockerfile: /space/git/dockerfiles_repos/Thermionix/Dockerfiles/phpmyadmin/Dockerfile
from shutit import shutit_module

class phpmyadmin(shutit_module.ShutItModule):

	def build(self, shutit):
		shutit.install('nginx phpmyadmin mcrypt libmcrypt-dev')
		return True

def module():
		return phpmyadmin(
				'shutit.tk.phpmyadmin.phpmyadmin', 0.1561234737,
				depends=['shutit.tk.setup']
		)
