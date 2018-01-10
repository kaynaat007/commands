#
# this script should not be run directly,
# instead you need to source it from your .bashrc,
# by adding this line:
#   . ~/bin/myprog.sh
#

function drona() {
    echo "changing to drona home dir for user $USER"
    source /home/nikhil/Dyfo/drona/Drona/drona_env/bin/activate
    cd /home/nikhil/Dyfo/drona/Drona
}
# call it 
drona



