from resource_management import *
from resource_management.libraries.script.script import Script
import commands
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
tmp_dir = Script.get_tmp_dir()
kylin_properties=config['configurations']['kylin']['kylin_properties']
hdp_version =  default("/commandParams/version", None)
downloadlocation = config['configurations']['kylin']['download.location']

#install_dir = config['configurations']['kylin']['install.dir']
cmd = "/usr/bin/hdp-select versions"
usr_base = "/usr/hdp/"
base_dir = usr_base + commands.getoutput(cmd) + "/kylin"
install_dir = format(base_dir)

# Find current stack and version to push agent files to
stack_name = default("/hostLevelParams/stack_name", None)
stack_version = config['hostLevelParams']['stack_version']

# Kylin archive on agent nodes
kylin_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version + "/services/KYLIN/package/"


current_host_name = socket.gethostname()
server_mode = "query"
server_masters = config['clusterHostInfo']['kylin_all_hosts'][0]
server_clusters_arr = config['clusterHostInfo']['kylin_all_hosts'] + (config['clusterHostInfo'].has_key('kylin_query_hosts') and config['clusterHostInfo']['kylin_query_hosts'] or [] )
server_port = "7070"
server_clusters = ','.join(i + ":" + server_port for i in server_clusters_arr)
kylin_servers = ';'.join( "server " + i + ":" + server_port for i in server_clusters_arr) + ";"
hadoop_conf_dir = install_dir + "/latest/conf/hadoop_conf"
nginx_conf=config['configurations']['nginx']['nginx_conf']
nginx_port=config['configurations']['nginx']['nginx_port']