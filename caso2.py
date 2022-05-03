#!/usr/bin_/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import argparse

def parameters():
    parser = argparse.ArgumentParser(description="Ingrese los parametros de red deseados: -n 'Cantidad de sucursales' ")
    parser.add_argument("-n", "--number", type=int, required=True, help="Numero de sucursales en la red")
    # parser.add_argument("-f", "--outputfile", type=str, required=True, help="string")
    # parser.add_argument("-l", "--logfile", type=str, required=True, help="string")
    args = parser.parse_args()
    return args

def myNetwork(n):



    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')#Tengo que agregar 2 switch por sucursal, uno para conectar la LAN y otro para conectarse a la WAN
    s_lan = [[] for x in range(n)]
    s_wan = [[] for y in range(n)]
    name_sLAN = [[] for x in range(n)]
    name_sWAN= [[] for y in range(n)]
    for i in range(n):
        name_sLAN[i] = "s" + str(i) + "_lan"
        name_sWAN[i] = "s" + str(i) + "_wan"
        s_lan[i] = net.addSwitch(name_sLAN[i], cls=OVSKernelSwitch, failMode='standalone')
        s_wan[i] = net.addSwitch(name_sWAN[i], cls=OVSKernelSwitch, failMode='standalone')
    

    r_central = net.addHost('r_central', cls=Node, ip='')
    r_central.cmd('sysctl -w net.ipv4.ip_forward=1')
    r = [[] for y in range(n)]
    nameR = [[] for y in range(n)]
    for i in range(n):
        nameR[i] = "r" + str(i)
        r[i] = net.addHost(nameR[i], cls=Node, ip='')
        r[i].cmd('sysctl -w net.ipv4.ip_forward=1')
    

    info( '*** Add hosts\n')
    h = [[] for w in range(n)]
    nameH = [[] for w in range(n)]
    for i in range(n):
        nameH[i] = "h" + str(i)
        h[i] = net.addHost(nameH[i], cls=Host, ip=('10.0.' + str(i+1) + '.254/24'), defaultRoute=None)

    info( '*** Add links\n')
    ult_address_ut = 6
    prim_address_ut = 1
    desplazamiento = 0
    incremento = 8
    for i in range(n):
        nameLink = 'r_central-eth' + str(i)
        nameLink_ri_wan = 'r' + str(i) + '-eth0'
        nameLink_ri_lan = 'r' + str(i) + '-eth1'
        ip_dir_ult_wan = '192.168.100.' + str(ult_address_ut + desplazamiento) + '/29'
        ip_dir_prim_wan = '192.168.100.' + str(prim_address_ut + desplazamiento) + '/29'
        ip_dir_prim_lan = '10.0.' + str(i + 1) + '.1/24'
        desplazamiento = desplazamiento + incremento
        net.addLink(r_central, s_wan[i], intfName1=nameLink, params1={ 'ip' : ip_dir_ult_wan }) #agrego todos los links del router central con cada interfaz de la wan con su IP correspondiente
        net.addLink(r[i], s_wan[i], intfName1=nameLink_ri_wan, params1={ 'ip' : ip_dir_prim_wan })
        net.addLink(r[i], s_lan[i], intfName1=nameLink_ri_lan, params1={ 'ip' : ip_dir_prim_lan })
        

    for i in range(n):
        net.addLink(h[i], s_lan[i])

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    for i in range (n):
        net.get(name_sLAN[i]).start([])
        net.get(name_sWAN[i]).start([])

    info( '*** Post configure switches and hosts\n')
    prim_address_ut = 1
    desplazamiento = 0
    incremento = 8
    for i in range (n):
        net['r_central'].cmd('ip route add 10.0.' + str(i+1) + '.0/24 via 192.168.100.' + str(prim_address_ut + desplazamiento))
        desplazamiento = desplazamiento + incremento

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    args = parameters()
    myNetwork(args.number)