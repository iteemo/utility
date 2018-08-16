#!/bin/bash

base_path=$(cd $(dirname $0);pwd)
conf_file=$2
action=$1
args="$@"
visit_log="/Users/mengzhe/PycharmProjects/untitled1/project_ci_test/logs/visit.log"

Split_line(){
    echo '-----------------------------------------'
}

Debug_help(){
    help_info=$1
    [[ $args == "--help" ]] \
    &&{
        Split_line
        echo "$help_info"
        Split_line
        exit 1
    }
}

Start(){
    Split_line
    echo "Begin start service"
    Split_line
    [[ $num -gt 2 ]] \
    &&{
       echo "当前已在运行此程序: $conf_file "
    } \
    ||{
       uwsgi --ini ${conf_file}.ini
       echo "已经开始运行，请查看日志是否启动成功"
       Split_line
       sleep 2
       tail -50 $visit_log
 
    }
    Split_line
    echo "End start $conf_file service"
    Split_line
}

Stop(){
    Split_line
    echo "Begin stop service"
    Split_line
    [[ $num -gt 2 ]] \
       &&{
         uwsgi --stop ${conf_file}.pid 
         sleep 2
         tail -10 $visit_log
         } \
       ||{
          echo "$conf_file 此程序未运行！"
        }
    Split_line
    echo "End stop $conf_file service"
    Split_line
}

Show(){
    Split_line
    echo "Show $conf_file service"
    Split_line
    [[ $num -gt 2 ]] \
       &&{
         uwsgi --connect-and-read ${conf_file}.status
         } \
       ||{
          echo "$conf_file 此程序未运行！"
        }
    echo
    Split_line
    echo "End show $conf_file service"
    Split_line
}

Reload(){
    Split_line
    echo "Reload $conf_file service"
    Split_line
    [[ $num -gt 2 ]] \
       &&{
         uwsgi --reload ${conf_file}.pid
         tail -5 $visit_log
         sleep 100
         tail -50 $visit_log
         } \
       ||{
          echo "$conf_file 此程序未运行！"
        }
    Split_line
    echo "End reload $conf_file service"
    Split_line
}



Check_args(){
    [[ $conf_file = ""  ]] \
    &&{
       echo "Wrong config file"
       exit   
    }

    [[ $action =~ show|reload|start|stop|restart  ]] \
    ||{
       echo "Wrong args"
       exit 
    }
}

Main(){
    Debug_help "
    A script to manage uwsgi service

    Usage
    1) Start service
        bash $0 start uwsgi
    2) Stop service
        bash $0 stop uwsgi
    3) Restart service
        bash $0 restart uwsgi
    4) Restart service
        bash $0 show uwsgi
    5) Restart service
        bash $0 reload uwsgi
    6) Help
        bash $0 --help
    "
    Check_args

    echo "The server info："
    ps aux | grep $conf_file | grep -v grep
    num=$(ps aux | grep $conf_file | grep -v grep|awk '{if($13 ~ /uwsgi.*/)print $13}'|wc -l)
    echo "The PPID num :" $num

    case $action in
	 show)
               Show
               ;;
         reload)
               Reload
               ;; 
         start)  
               Start
               ;;
         stop)
               Stop
               ;;
         restart)
               Stop
               sleep 3
               Start
               ;;
    esac
}
Main
