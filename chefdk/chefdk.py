from shutit_module import ShutItModule

class chefdk(ShutItModule):

	def build(self, shutit):
		# TODO: version number, rpm download
		processor = shutit.send_and_get_output('uname -p')
		if not shutit.command_available('wget'):
			shutit.install('wget')
		if not shutit.command_available('chef-solo'):
		if shutit.get_current_shutit_pexpect_session_environment().install_type == 'apt':
			pw = shutit.get_env_pass('Input your sudo password to install chefdk')
			shutit.send('wget -qO- https://packages.chef.io/stable/ubuntu/12.04/chefdk_1.0.3-1_amd64.deb > /tmp/chefdk.deb')
			shutit.multisend('sudo dpkg -i /tmp/chefdk.deb',{'assword':pw})
		elif shutit.get_current_shutit_pexpect_session_environment().install_type == 'yum':
			pw = shutit.get_env_pass('Input your sudo password to install chefdk')
			shutit.send('wget -qO- https://packages.chef.io/stable/ubuntu/12.04/chefdk_1.0.3-1_amd64.deb > /tmp/chefdk.rpm')
			shutit.multisend('sudo rpm -i /tmp/chefdk.rpm',{'assword':pw})
		else:
			shutit.install('chefdk')
		return True

def module():
		return chefdk(
			'shutit-test.chefdk.chefdk', 0.1649027060,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['shutit.tk.setup']
		)


