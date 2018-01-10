#
# this script should not be run directly,
# instead you need to source it from your .bashrc,
# by adding this line:
#   . ~/bin/myprog.sh
#

function cmd() {
     echo "changing to command home dir for user $USER"
     cd /home/nikhil/commands
}
# call it 
cmd



