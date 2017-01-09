from shutit_module import ShutItModule

class inspec(ShutItModule):


	def build(self, shutit):
		shutit.send('gem install rake')
		shutit.send('gem install inspec')
		return True

def module():
		return inspec(
			'shutit-library.inspec.inspec', 544526579.0001,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['shutit-library.kitchen.kitchen']
		)
