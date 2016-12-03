import random
import string
import os
import inspect

from shutit_module import ShutItModule

class swarm(ShutItModule):

	def build(self, shutit):
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		gui = shutit.cfg[self.module_id]['gui']
		memory = shutit.cfg[self.module_id]['memory']
		run_dir = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + '/vagrant_run'
		module_name = 'swarm_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.cfg[self.module_id]['vagrant_run_dir'] = run_dir + '/' + module_name
		shutit.send('command rm -rf ' + run_dir + '/' + module_name + ' && command mkdir -p ' + run_dir + '/' + module_name + ' && command cd ' + run_dir + '/' + module_name)
		if shutit.send_and_get_output('vagrant plugin list | grep landrush') == '':
			shutit.send('vagrant plugin install landrush')
		shutit.send('vagrant init ' + vagrant_image)
		shutit.send_file(run_dir + '/' + module_name + '/Vagrantfile','''Vagrant.configure("2") do |config|
  config.landrush.enabled = true
  config.landrush.upstream '8.8.8.8'
  config.vm.provider "virtualbox" do |vb|
    vb.gui = ''' + gui + '''
    vb.memory = "''' + memory + '''"
  end

  config.vm.define "swarm1" do |swarm1|
    swarm1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    swarm1.vm.hostname = "swarm1.vagrant.test"
  end
  config.vm.define "swarm2" do |swarm2|
    swarm2.vm.box = ''' + '"' + vagrant_image + '"' + '''
    swarm2.vm.hostname = "swarm2.vagrant.test"
  end
  config.vm.define "swarm3" do |swarm3|
    swarm3.vm.box = ''' + '"' + vagrant_image + '"' + '''
    swarm3.vm.hostname = "swarm3.vagrant.test"
  end
end''')
		pw = shutit.get_env_pass()
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'],{'assword for':pw},timeout=99999)
		except:
			shutit.multisend('vagrant up',{'assword for':pw},timeout=99999)
		swarm1_ip = shutit.send_and_get_output('''vagrant landrush ls | grep -w ^swarm1.vagrant.test | awk '{print $2}' ''')
		swarm2_ip = shutit.send_and_get_output('''vagrant landrush ls | grep -w ^swarm2.vagrant.test | awk '{print $2}' ''')
		swarm3_ip = shutit.send_and_get_output('''vagrant landrush ls | grep -w ^swarm3.vagrant.test | awk '{print $2}' ''')
		machines = [['swarm1','swarm1.vagrant.test',swarm1_ip],['swarm2','swarm2.vagrant.test',swarm2_ip],['swarm3','swarm3.vagrant.test',swarm3_ip]]
		for machine in machines:
			shutit.login(command='vagrant ssh ' + machine[0])
			shutit.login(command='sudo su -',password='vagrant')
			root_password = 'root'
			shutit.install('net-tools') # netstat needed
			shutit.install('bind-utils') # host needed
			# Workaround for docker networking issues + landrush.
			shutit.send('''echo "$(host -t A index.docker.io | grep has.address | head -1 | awk '{print $NF}') index.docker.io" >> /etc/hosts''')
			shutit.send('''echo "$(host -t A registry-1.docker.io | grep has.address | head -1 | awk '{print $NF}') registry-1.docker.io" >> /etc/hosts''')
			shutit.multisend('passwd',{'assword:':root_password})
			shutit.send('''sed -i 's/.*PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config''')
			shutit.send('''sed -i 's/.*PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config''')
			shutit.send('systemctl restart sshd')
			shutit.multisend('ssh-keygen',{'Enter':''})
			shutit.logout()
			shutit.logout()

		for machine in machines:
			shutit.login(command='vagrant ssh ' + machine[0])
			shutit.login(command='sudo su -',password='vagrant')
			for ssh_copy_to in machines:
				shutit.multisend('ssh-copy-id root@' + ssh_copy_to[0],{'assword:':root_password,'ontinue conn':'yes'})
				shutit.multisend('ssh-copy-id root@' + ssh_copy_to[1],{'assword:':root_password,'ontinue conn':'yes'})
			shutit.multisend('ssh-copy-id root@' + swarm1_ip,{'assword:':root_password,'ontinue conn':'yes'})
			shutit.multisend('ssh-copy-id root@' + swarm2_ip,{'assword:':root_password,'ontinue conn':'yes'})
			shutit.multisend('ssh-copy-id root@' + swarm3_ip,{'assword:':root_password,'ontinue conn':'yes'})
			shutit.logout()
			shutit.logout()
		
		shutit.login(command='vagrant ssh swarm1')
		shutit.login(command='sudo su -',password='vagrant')
		shutit.install('docker')
		# Workaround required for dns/landrush/docker issues: https://github.com/docker/docker/issues/18842
		shutit.insert_text('Environment=GODEBUG=netdns=cgo','/usr/lib/systemd/system/docker.service',pattern='Environment=.*')
		shutit.send('systemctl daemon-reload')
		shutit.send('systemctl restart docker')
		shutit.send('curl -L https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-`uname -s`-`uname -m` >/usr/local/bin/docker-machine && chmod +x /usr/local/bin/docker-machine')
		token = shutit.send_and_get_output('docker run swarm create 2>&1 | tail -1')
		shutit.send('docker-machine create -d generic --generic-ip-address ' + swarm1_ip + ' --engine-env GODEBUG=netdns=cgo --swarm --swarm-master --swarm-discovery token://' + token + ' swarm1')
		shutit.send('docker-machine create -d generic --generic-ip-address ' + swarm2_ip + ' --engine-env GODEBUG=netdns=cgo --swarm --swarm-discovery token://' + token + ' swarm2')
		shutit.send('docker-machine create -d generic --generic-ip-address ' + swarm3_ip + ' --engine-env GODEBUG=netdns=cgo --swarm --swarm-discovery token://' + token + ' swarm3')
		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		shutit.get_config(self.module_id,'vagrant_image',default='centos/7')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		shutit.get_config(self.module_id,'gui',default='false')
		shutit.get_config(self.module_id,'memory',default='1024')
		shutit.get_config(self.module_id,'vagrant_run_dir',default='/tmp')
		return True

def module():
	return swarm(
		'tk.shutit.swarm.swarm', 0.99000125135361,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualization.virtualization.virtualization','tk.shutit.vagrant.vagrant.vagrant']
	)
