"""ShutIt module. See http://shutit.tk
"""

from shutit import shutit_module

class headless(shutit_module.ShutItModule):

	def build(self,shutit):
		shutit.install('xvfb')
		shutit.install('rubygems')
		shutit.send('gem install headless')
		return True

def module():
	return headless(
		'shutit.tk.headless.headless', 0.1231251,
		description='https://github.com/mparaz/headless',
		depends=['shutit.tk.setup']
	)

