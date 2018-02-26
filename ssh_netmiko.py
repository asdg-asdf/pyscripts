#!/bin/env python
# -*- coding: UTF-8 -*-
# script_name ssh_netmiko.py
# ssh_netmiko.py /CFG/${job_id}/config.cfg


import sys
import json
import os
import shlex
import re
import time
import socket
import copy
import netmiko



def disable_paging(remote_conn):
    remote_conn.send("terminal length 0 \n")
    time.sleep(1)
    output= remote_conn.recv(1000)
    return  output

def security_check(command_line):
    dict_cmd = ['rm', 'delete', 'echo', 'mv', 'cp', '', 'chown', 'chmod', 'sync', 'rsync', 'tar', 'tail', 'alias',
                '/usr/bin/rm', '/bin/rm', '/usr/bin/rm']
    for x_line in shlex.split(command_line):
        ##print "security_check::x_line=%s" %(x_line)
        if x_line in dict_cmd:
            return 'ranfail'
    return "security"

def ssh_connect(host_ip, host_port, host_username, host_passwd , device_type , uuid_command_list):
    ##IP::PORT::username::password::device_type::uuid11##command11::uuid22##command22::uuid33##command33
    device_dict = {
        'device_type': device_type ,
        'ip' : host_ip ,
        'port' : host_port ,
        'username' : host_username ,
        'password' : host_passwd,
        'verbose': False,
    }
    uuid_result_lists={}
    try:
        net_connect = netmiko.ConnectHandler(**device_dict)
        for uuid_command in uuid_command_list :
            uuid_result_lists[uuid_command.split('##')[0]] = net_connect.send_command(uuid_command.split('##')[1])
            time.sleep(1)
    except Exception, e:
        uuid_result_lists[uuid_command_list[0].split('##')[0]]= "ExceptionXOutput" + str(e)
    return  uuid_result_lists


def run_command_return_result(parameter_file_content_line):
    ##IP::PORT::username::password::device_type::uuid11##command11::uuid22##command22::uuid33##command33
    # 10.0.224.31::22::root::123456::d41d8cd98f00b204e9800998ecf8427e##ifconfig -a::u41d8cd98f00b206e9800998ecf8427F##hostname
    #('d41d8cd98f00b204e9800998ecf8427e1\n',{'username': 'root', 'ip': '192.168.2.1', 'password': '123456', 'command': 'ifconfig -a', 'port': '22'})
    command_result_list = []
    command_result = {}
    file_line=parameter_file_content_line.split('::')
    host_ip = file_line[0]
    host_port = file_line[1]
    host_username = file_line[2]
    host_passwd = file_line[3]
    device_type = file_line[4]
    uuid_command_list=file_line[5:]
    uuid_result = ssh_connect(host_ip, int(host_port), host_username, host_passwd, device_type,uuid_command_list)
    #uuid_result = {"uuid1":"result1","uuid2":"result2","uuid3":"result3"}
    for uuid in uuid_result :
        # result = {"uuid1":"result1"}
        command_result["MESSAGE"] = uuid_result[uuid]
        command_result["uuid"] = uuid
        if "ExceptionXOutput" in command_result["MESSAGE"] :
            command_result['STATUS'] = 'ranfail'
        else:
            command_result['STATUS'] = 'ran'
        command_result_list.append(copy.deepcopy(command_result))
    return command_result_list

def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def main():
    messgae_result = {}
    result = []
    ##print "main::sys.argv[1]=%s" %(sys.argv[1])
    #/CFG/job_id/config.cfg
    if  sys.argv[1] :
        pass
    else:
        messgae_result["sender"] = socket.gethostname()
        messgae_result["statusmsg"] = "args is null"
        messgae_result["statuscode"] = "42"
        result.append(messgae_result)
        encodedjson = json.dumps(result)
        print encodedjson
        sys.exit(0)
    parameter_file_path=sys.argv[1]
    ##print "main::job_id=%s" %(job_id)
    if (type(parameter_file_path) is str) and os.path.isfile(parameter_file_path):
        with open(parameter_file_path, 'r') as parameter_file_context:
            parameter_file_content_line = parameter_file_context.readline()
            while parameter_file_content_line:
                if checkip(parameter_file_content_line.split('::')[0]):
                    messgae_result["sender"] = parameter_file_content_line.split('::')[0]
                    messgae_result["statusmsg"] = run_command_return_result(parameter_file_content_line)
                    if messgae_result["statusmsg"] :
                        messgae_result["statuscode"] =0
                    else:
                        messgae_result["statuscode"] = 42
                result.append(copy.deepcopy(messgae_result))
                parameter_file_content_line = parameter_file_context.readline()
    else:
        messgae_result["sender"] = socket.gethostname()
        messgae_result["statusmsg"] = "arguments = [ " + sys.argv[1] + " ] " + "format error"
        messgae_result["statuscode"] = 42
        result.append(messgae_result)

    print json.dumps(result)

if __name__ == "__main__":
    main()
