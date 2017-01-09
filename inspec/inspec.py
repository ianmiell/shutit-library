from shutit_module import ShutItModule

class inspec(ShutItModule):


	def build(self, shutit):
		shutit.send('gem install rake')
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
