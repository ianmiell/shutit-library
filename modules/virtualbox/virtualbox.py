from shutit_module import ShutItModule

class virtualbox(ShutItModule):

	def build(self, shutit):
		cfg = shutit.cfg
		if not shutit.command_available('VBoxManage'):
			if shutit.get_current_shutit_pexpect_session_environment().install_type == 'apt': 
				shutit.send('echo "deb http://download.virtualbox.org/virtualbox/debian $(lsb_release -s -c) contrib" >> /etc/apt/sources.list ')
				shutit.send('wget -qO- https://www.virtualbox.org/download/oracle_vbox.asc | sudo apt-key add -')
				shutit.send('apt-get update')
				shutit.install('virtualbox-5.0')
			else:
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

