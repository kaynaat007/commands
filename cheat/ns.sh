#!/bin/bash
# updated 
install_dir=$HOME
version=$1
echo "nucleus will be installed in $install_dir"
# contants
pip_conf="$install_dir/.pip/pip.conf"
yamjam_dir="$install_dir/.yamjam"
yamjam_config="$install_dir/.yamjam/config.yaml"
virtual_env="nucleus_env"
manage_py_path="$install_dir/$virtual_env/lib/python2.7/site-packages/DyfoNucleus/nucleus/manage.py"
python_path="$install_dir/$virtual_env/bin/python"
nucleus_command_file_name="$install_dir/nucleus.sh"
nucleus_command_path="/usr/local/bin/nucleus"
ALIASES_FILE_PATH=$HOME/.aliases

echo "will be making virtual env $virtual_env in $install_dir"

# install nucleus
# sudo apt-get install vim
# sudo apt-get install virtualenv
cd $install_dir && virtualenv  --system-site-packages $virtual_env
cd $install_dir && source $install_dir/$virtual_env/bin/activate
cd $install_dir && mkdir -p $install_dir/.pip
cd $install_dir && mkdir -p $yamjam_dir
cd $install_dir && touch $pip_conf
cd $install_dir && touch $yamjam_config
cd $install_dir && touch $nucleus_command_file_name

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

cd $install_dir && pip install dyfo-nucleus==$version
cd $install_dir && $python_path $manage_py_path migrate

cat > $nucleus_command_file_name <<- EOM
#!/bin/bash
$python_path $manage_py_path \$*
EOM

echo "making $nucleus_command_file_name executable"
sudo chmod +x $nucleus_command_file_name
echo "creating symlink to $nucleus_command_path"
sudo ln -sf $nucleus_command_file_name $nucleus_command_path
echo "done running migrations. nucleus install is complete"
echo "nucleus command is now available"


# usage ./add_alias.sh gtd=git diff
# function save-alias() {`

#    touch $ALIASES_FILE_PATH || exit

#    ALIAS_NAME=`echo "$1" | grep -o ".*="`

    # Deleting dublicate aliases
#    sed -i "/alias $ALIAS_NAME/d" $ALIASES_FILE_PATH

    # Quoting command: my-alias=command -> my-alias="command"
#    QUOTED=`echo "$1"\" | sed "s/$ALIAS_NAME/$ALIAS_NAME\"/g"`

#    echo "alias $QUOTED" >> $ALIASES_FILE_PATH

#    # Loading aliases

#    source $ALIASES_FILE_PATH
#    echo "sourcing $ALIASES_FILE_PATH"
#}

#save-alias "nucleus=$python_path $manage_py_path"


