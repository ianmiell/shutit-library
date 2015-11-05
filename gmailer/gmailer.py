"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule

class gmailer(ShutItModule):

	def build(self,shutit):
		shutit.install('mailutils')
		shutit.install('ssmtp')
		shutit.send("""cat > /etc/ssmtp/ssmtp.conf << END
AuthUser=""" + shutit.cfg[self.module_id]['email'] + """
AuthPass=""" + shutit.cfg[self.module_id]['password'] + """
mailhub=smtp.gmail.com:587
UseSTARTTLS=YES
AuthMethod=LOGIN
END""") 
		return True

	def get_config(self,shutit):
		shutit.get_config(self.module_id,'email',default='test@gmail.com')
		shutit.get_config(self.module_id,'password',default='')
		return True

def module():
	return gmailer(
		'shutit.tk.gmailer.gmailer', 0.0006,
		description='Allows you to send gmails with mail',
		depends=['shutit.tk.setup']
	)

