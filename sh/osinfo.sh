#!/bin/bash
#Server OS info

OS_version=''


echo -e "\n\033[31;49;1m [ Flying chicken 1.0 ] \033[39;49;0m\n" 
echo -e "\033[37;49;1m Produced by Turkey Team! \033[39;49;0m" 
echo -e "\033[37;49;1m A security scanner for Linux!!! \033[39;49;0m\n"

echo -e "##################################################################################\n"

#server infomation
echo -e "\033[34;49;1m[+] Server Info \033[39;49;0m"
echo -e "------------------------------------"

hostname=`hostname`
echo -e "  - HostName:        $hostname" 
#osinfo=`cat /etc/redhat-release`

#echo -e "OS info:        $osinfo"


kernelinfo=`uname -r`
echo -e "  - LinuxKernel:     $kernelinfo" 

kernelmac=`uname -m`
echo -e "  - HW Machine:      $kernelmac" 

CPU=`cat /proc/cpuinfo | grep "model name" | head -n 1 | awk -F ":" "{print $2}"`
echo -e "  - CPU info:        $CPU" 

if [ "${OS_version}" == 'CentOS6' ];then
        network=`ifconfig -a  | awk 'BEGIN {FS="\n"; RS=""} {print $1,$2}' | grep -v 'lo' |  awk '{print "\t\t"$1,$7}'`
else
        network=`ifconfig -a  | awk 'BEGIN {FS="\n"; RS=""} {print $1,$2}' | grep -v 'lo' |  awk '{print "\t\t"$1,$6}'`
fi

echo -e "  - NetWork info:    $network" 

externalip=$(timeout 3 curl -s ipecho.net/plain;echo)
[ $? -ne 0 -o 'X' == "$externalip"X ] && externalip='No outside network or ACL drop'
echo -e "  - External IP:     $externalip" 


Username=`whoami`
echo -e "  - UserName:        $Username" 

echo -e "  - UserHomeDir:     $HOME\n" 
echo -e "\n---------------------------------------------------------------------------------------------\n"

#mem detect
echo -e "\033[34;49;1m[+] Memory Info \033[39;49;0m"
echo -e "------------------------------------"

MemTotal=$(grep MemTotal /proc/meminfo| awk '{print $2}')  #KB
MemFree=$(grep MemFree /proc/meminfo| awk '{print $2}')    #KB
let MemUsed=MemTotal-MemFree
MemPercent=$(awk "BEGIN {if($MemTotal==0){printf 100}else{printf \"%.2f\",$MemUsed*100/$MemTotal}}")
report_MemTotal="$((MemTotal/1024))""MB"        #内存总容量(MB)
report_MemFree="$((MemFree/1024))""MB"          #内存剩余(MB)
report_MemUsedPercent="$(awk "BEGIN {if($MemTotal==0){printf 100}else{printf \"%.2f\",$MemUsed*100/$MemTotal}}")""%"   #内存使用率%
echo -e "  - Memory Total:    ${report_MemTotal}" 
echo -e "  - Memory Total:    ${report_MemFree}" 
echo -e "  - Memory Total:    ${report_MemUsedPercent}" 

echo -e "\n---------------------------------------------------------------------------------------------\n"

#disk detect
echo -e "\033[34;49;1m[+] Disk Info \033[39;49;0m"
echo -e "------------------------------------"

    df -hiP | sed 's/Mounted on/Mounted/'> /tmp/inode
    df -hTP | sed 's/Mounted on/Mounted/'> /tmp/disk 
    #join /tmp/disk /tmp/inode | awk '{print $1,$2,"|",$3,$4,$5,$6,"|",$8,$9,$10,$11,"|",$12}'| column -t
    #报表信息
    diskdata=$(df -TP | sed '1d' | awk '$2!="tmpfs"{print}') #KB
    disktotal=$(echo "$diskdata" | awk '{total+=$3}END{print total}') #KB
    diskused=$(echo "$diskdata" | awk '{total+=$4}END{print total}')  #KB
    diskfree=$((disktotal-diskused)) #KB
    diskusedpercent=$(echo $disktotal $diskused | awk '{if($1==0){printf 100}else{printf "%.2f",$2*100/$1}}') 
    inodedata=$(df -iTP | sed '1d' | awk '$2!="tmpfs"{print}')
    inodetotal=$(echo "$inodedata" | awk '{total+=$3}END{print total}')
    inodeused=$(echo "$inodedata" | awk '{total+=$4}END{print total}')
    inodefree=$((inodetotal-inodeused))
    inodeusedpercent=$(echo $inodetotal $inodeused | awk '{if($1==0){printf 100}else{printf "%.2f",$2*100/$1}}')
    report_DiskTotal=$((disktotal/1024/1024))"GB"   #硬盘总容量(GB)
    report_DiskFree=$((diskfree/1024/1024))"GB"     #硬盘剩余(GB)
    report_DiskUsedPercent="$diskusedpercent""%"    #硬盘使用率%
    report_InodeTotal=$((inodetotal/1000))"K"       #Inode总量
    report_InodeFree=$((inodefree/1000))"K"         #Inode剩余
    report_InodeUsedPercent="$inodeusedpercent""%"  #Inode使用率%
echo -e "  - Disk Total:            ${report_DiskTotal}" 
echo -e "  - Disk Free:             ${report_DiskFree}" 
echo -e "  - Disk Used Percent:     ${report_DiskUsedPercent}" 
echo -e "  - Inode Total:           ${report_InodeTotal}" 
echo -e "  - Inode Free:            ${report_InodeFree}" 
echo -e "  - Inode Used Percent:    ${report_InodeUsedPercent}" 

echo -e "\n---------------------------------------------------------------------------------------------\n"

