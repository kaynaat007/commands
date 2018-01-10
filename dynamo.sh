
# this script should not be run directly,
# instead you need to source it from your .bashrc,
# by adding this line:
#   . ~/bin/myprog.sh
#

function dynamo() {
      echo "changing to dynamo home dir for user $USER"
      source /home/nikhil/Dyfo/dynamo/dynamo_env/bin/activate
      cd /home/nikhil/Dyfo/dynamo
}
# call it 
dynamo



