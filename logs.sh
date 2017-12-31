function piws() {
   echo "changing to logs  dir for user $USER"
   source /home/`whoami`/AviatorRepo/aviator_env/bin/activate
   cd /home/`whoami`/AviatorRepo/dyfo/logs/
}
# call it 
piws



