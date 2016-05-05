from shutit_module import ShutItModule

class virtualbox(ShutItModule):

	def build(self, shutit):
		cfg = shutit.cfg
		if not shutit.command_available('VBoxManage'):
			shutit.install('virtualbox')
		return True

def module():
	return virtualbox(
		'shutit-library.virtualbox.virtualbox.virtualbox', 0.8024250902,
		description='Virtualbox',
		maintainer='ian.miell@gmail.com',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

