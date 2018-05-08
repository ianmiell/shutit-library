
# Created from dockerfile: /space/git/dockerfiles_repos/SvenDowideit/dockerfiles/camlistore//Dockerfile
from shutit import shutit_module

class camlistore(shutit_module.ShutItModule):

	def build(self, shutit):
		shutit.install('git golang',force=True)
		shutit.send('pushd /opt')
		shutit.send('git clone https://github.com/bradfitz/camlistore.git')
		shutit.send('chmod 777 camlistore')
		shutit.send('pushd camlistore')
		shutit.send('go run make.go')
		shutit.send('popd')
		return True

def module():
		return camlistore(
				'shutit.tk.camlistore.camlistore', 0.1567436346,
				depends=['shutit.tk.setup']
		)
