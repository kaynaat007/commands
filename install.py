from __future__ import print_function
import subprocess
import os
import sys

this_path = os.path.abspath(__file__)
current_dir = os.path.dirname(this_path)
valid_files = ['open_salt.sh', 'open_graylog.sh']



def console(*args,  **kwargs):
    """
    handles key value in message
    :param args:
    :return:
    """
    # if either display or display_messages is True, print on screen. display_messages is global
    # variable.

    print(*args, file=sys.stdout, ** kwargs)
    return


def run_command(cmd, ignore_error=False, maintain_pipe=True):
    """
    :param command:
    :return:
    """
    if cmd in ['start', 'restart', 'stop']:
        command_services(cmd, ignore_error)
        return

    console('executing command {0}'.format(cmd))
    if maintain_pipe:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print (output.strip())
        rc = process.poll()
        if ignore_error:
            console('Ignore error is set to True. Not reporting status of the command')
            return
        assert rc == 0, 'The command {0} failed. Aborting'.format(cmd)
    else:
        process = subprocess.Popen(cmd, shell=True)
        exit(0)

def install():
   for content in os.listdir(current_dir): 
        if content not in valid_files:
		continue
        path = os.path.join(current_dir, content);
        content = content.split('.')[0]
        cmd = ' '.join([ 'sudo', 'ln', '-s', path,  os.path.join('/usr/bin', content)])
        run_command(cmd, ignore_error=True)

install() 


        
 	

         

