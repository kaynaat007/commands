#!/bin/bash
# updated 
install_dir=$HOME
machine_id=$1
machine_type=$2
version=$3
hour=$4
minute=$5

if [ "$#" -ne 5 ]; then
      echo "First is machine id"
      echo "Second is machine_type"
      echo "Third ia version of dyfo-lava"
      echo "fourth is hour at which lava will run (24 hour format)"
      echo "fifth is minute at which lava will run" 
      exit 1
fi

echo "dyfo-lava will be installed in $install_dir"
# contants
pip_conf="$install_dir/.pip/pip.conf"
yamjam_dir="$install_dir/.yamjam"
yamjam_config="$install_dir/.yamjam/config.yaml"
virtual_env="lava_env"
python_path="$install_dir/$virtual_env/bin/python"

echo "will be making virtual env $virtual_env in $install_dir"

# install dyfo-lava
if [ ! -d "$install_dir/$virtual_env" ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    cd $install_dir && virtualenv  --system-site-packages $virtual_env
fi
cd $install_dir && source $install_dir/$virtual_env/bin/activate
cd $install_dir && mkdir -p $install_dir/.pip
cd $install_dir && mkdir -p $yamjam_dir
cd $install_dir && touch $pip_conf
cd $install_dir && touch $yamjam_config

cat > $pip_conf <<- EOM
[global]
trusted-host=pypi.dyfolabs.com
index-url=http://pypi.dyfolabs.com:8080/simple/
EOM


if [[ $(grep -F "ftp_user" $yamjam_config) ]]; then
    echo "There is ftp user in yamjam.  No inserting ftp credentials."
else

cat >> $yamjam_config <<- EOM
ftp_user:
   user: shot
   pass: shot_ftp
EOM
echo "ftp credentials set in yamjam"

fi

cd $install_dir && pip install dyfo-lava==$version

$python_path $HOME/lava_cron.py $machine_id $machine_type $hour $minute 
echo "dyfo-lava is added to crontab at $hour hour and $minute minutes"
