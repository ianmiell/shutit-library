"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class vagrant(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#if not shutit.command_available('vagrant'):
		#	if shutit.get_input('vagrant apparently not installed. Would you like me to install it for you?',boolean=True):
		#	    pw = shutit.get_input('Please input your sudo password in case it is needed.',ispass=True)
		#	    command = shutit.get_input('Please input your install command, eg "apt-get install -y", or "yum install -y"')
		#	    shutit.multisend('sudo ' + command + ' vagrant',{'assword':pw})
		cfg=shutit.cfg
		vagrant_version = '1.8.1'
		processor = shutit.send_and_get_output('uname -p')
		if not shutit.command_available('wget'):
			shutit.install('wget')
		if not shutit.command_available('vagrant'):
			if cfg['environment'][cfg['build']['current_environment_id']]['install_type'] == 'apt':
				pw = shutit.get_env_pass('Input your sudo password to install vagrant')
				shutit.send('wget -qO- https://dl.bintray.com/mitchellh/vagrant/vagrant_' + vagrant_version + '_' + processor + 'x86_64.deb > /tmp/vagrant.deb',note='Downloading vagrant and installing')
				shutit.multisend('sudo dpkg -i /tmp/vagrant.deb',{'assword':pw})
				shutit.send('rm -f /tmp/vagrant.deb')
			elif cfg['environment'][cfg['build']['current_environment_id']]['install_type'] == 'yum':
				pw = shutit.get_env_pass('Input your sudo password to install vagrant')
				shutit.send('wget -qO- https://dl.bintray.com/mitchellh/vagrant/vagrant_' + vagrant_version + '_' + processor + '.rpm > /tmp/vagrant.rpm',note='Downloading vagrant and installing')
				shutit.multisend('sudo rpm -i /tmp/vagrant.rpm',{'assword':pw})
				shutit.send('rm -f /tmp/vagrant.rpm')
			else:
				shutit.install('vagrant')
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


	#Class-level functions
	def restore(shutit):
		if shutit.send_and_match_output('vagrant status',['.*running.*','.*saved.*','.*poweroff.*','.*not created.*','.*aborted.*']):
			if not shutit.send_and_match_output('vagrant status',['.*running.*','.*not created.*']) and shutit.get_input('A vagrant setup already exists here. Do you want me to start up the existing instance (y) or destroy it (n)?',boolean=True):
				shutit.send('vagrant up')
				return True
			elif not shutit.send_and_match_output('vagrant status',['.*not created.*']):
				shutit.send('vagrant up')
				return True
			elif not shutit.send_and_match_output('vagrant status',['.*running.*']):
				shutit.send('vagrant destroy -f')
				shutit.send('vagrant up')
				return True
			else:
				return False
		else:
			return False


def module():
	return vagrant(
		'tk.shutit.vagrant.vagrant.vagrant', 0.941247152,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

