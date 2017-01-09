from shutit_module import ShutItModule

class test_kitchen(ShutItModule):


	def build(self, shutit):
		# TODO: https://github.com/test-kitchen/test-kitchen/wiki/Getting-Started
		return True

def module():
		return test_kitchen(
			'git.test_kitchen.test_kitchen', 0.9549975645,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['tk.shutit.vagrant.vagrant.vagrant','shutit-library.chefdk.chefdk']
		)
