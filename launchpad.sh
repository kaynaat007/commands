#
# this script should not be run directly,
# instead you need to source it from your .bashrc,
# by adding this line:
#   . ~/bin/myprog.sh
#

function launchpad() {
    echo "changing to launchpad home dir for user $USER"
    source /home/nikhil/AviatorRepo/aviator_env/bin/activate
    cd /home/nikhil/Dyfo/astrolaunchpadrepo/AstroLaunchpad
}
# call it 
launchpad



