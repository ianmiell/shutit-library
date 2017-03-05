from shutit_module import ShutItModule

class minikube(ShutItModule):


	def build(self, shutit):
		if not shutit.command_available('minikube'):
			shutit.send('curl https://storage.googleapis.com/minikube/releases/v0.16.0/minikube-linux-amd64 > minikube')
			shutit.send('chmod +x minikube')
			shutit.send('mv minikube /usr/local/bin/minikube')
		if not shutit.send_and_get_output('''minikube status | grep 'Does Not Exist' | wc -l | awk '{print $1}' ''') == '1':
			shutit.send('./minikube start')
		if not shutit.command_available('kubectl'):
			shutit.send('curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl')
			shutit.send('chmod +x kubectl')
			shutit.send('mv kubectl /usr/local/bin/kubectl')
		return True

def module():
		return minikube(
			'shutit-library.minikube.minikube', 0.12135426,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['shutit.tk.setup']
		)
