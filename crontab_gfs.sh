
path=/home/liuzhonghua/model/gfs_curl
pythonpath=/data1/liuzhonghua/software/miniconda3/bin/python3.6
exepath=/home/liuzhonghua/model/gfs_curl
logpath=/massdata1/liuzhonghua/data/gfs/log
 

##########################

. /etc/profile
. ~/.bash_profile
##########################

nohup $pythonpath ${exepath}/dl_gfs_newest_v2.py   >${logpath}/$(date +%Y-%m-%d-%Hh).dl_gfs_newest_v2.log	 2>&1 & 

 