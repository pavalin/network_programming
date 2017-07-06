import paramiko
import time

def disable_paging(remote_conn):
	'''Disable paging on a Juniper router'''
	
	remote_conn.send("set cli screen-length 0\n")
	time.sleep(1)
	
	#Clear the buffer on the screen
	output = remote_conn.recv(1000)
	
	return output
	
	
if __name__ == '__main__':

	#VARIABLES
	ip = '192.168.1.217'
	username = 'root'
	password = '1qaz2wsx'
	
	#Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()
	
	#Automatically add untrusted hosts (make sure ok for security policy)
	remote_conn_pre.set_missing_host_key_policy(
		paramiko.AutoAddPolicy())
		
	# initiate SSH connection
	remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
	print "SSH connection established to %s" % ip
	
	#Use invoke shell to establish an interactive session
	remote_conn = remote_conn_pre.invoke_shell()
	print "Interactive SSH session established"
	
	#Strip the initial router prompt
	output = remote_conn.recv(1000)
	
	#See what we have
	print output
	
	#Establish a CLI session
	remote_conn.send("cli\n")
	
	#Turn off paging
	disable_paging(remote_conn)
	
	#Send the router a command
	remote_conn.send("\n")
	remote_conn.send("show interface terse\n")
	
	#Wait for the command to complete
	time.sleep(2)
	
	output = remote_conn.recv(5000)
	print output
	
	
