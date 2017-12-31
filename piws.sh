
#
# this script should not be run directly,
# instead you need to source it from your .bashrc,
# by adding this line:
#   . ~/bin/myprog.sh
#

function piws() {
   echo "changing to piws home dir for user $USER"
   source /home/`whoami`/AviatorRepo/aviator_env/bin/activate
   cd /home/`whoami`/AviatorRepo/dyfo/projects/piWS/piWS
}
# call it 
piws



