from shutit_module import ShutItModule

class inspec(ShutItModule):


	def build(self, shutit):
		if not shutit.command_available('rake'):
			if shutit.send_and_expect('whoami') != 'root':
				shutit.fail('must be root')
			if not shutit.command_exists('gem'):
				shutit.fail('gem must be available')
			shutit.send('gem install rake')
		if not shutit.command_available('inspec'):
			if shutit.send_and_expect('whoami') != 'root':
				shutit.fail('must be root')
			if not shutit.command_exists('gem'):
				shutit.fail('gem must be available')
			shutit.send('gem install inspec')
		return True

def module():
		return inspec(
			'shutit-library.inspec.inspec', 0.9555141983517,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['shutit-library.test_kitchen.test_kitchen']
		)
