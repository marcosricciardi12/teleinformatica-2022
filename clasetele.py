#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch, failMode='standalone')
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, failMode='standalone')
    r6 = net.addHost('r6', cls=Node, ip='0.0.0.0')
    r6.cmd('sysctl -w net.ipv4.ip_forward=1')
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, failMode='standalone')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    s18 = net.addSwitch('s18', cls=OVSKernelSwitch, failMode='standalone')
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, failMode='standalone')
    r7 = net.addHost('r7', cls=Node, ip='0.0.0.0')
    r7.cmd('sysctl -w net.ipv4.ip_forward=1')
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, failMode='standalone')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, failMode='standalone')
    s19 = net.addSwitch('s19', cls=OVSKernelSwitch, failMode='standalone')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, failMode='standalone')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, failMode='standalone')
    r5 = net.addHost('r5', cls=Node, ip='0.0.0.0')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch, failMode='standalone')
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s14)
    net.addLink(s14, r2)
    net.addLink(r2, s8)
    net.addLink(s8, r1)
    net.addLink(s9, r1)
    net.addLink(s10, r1)
    net.addLink(s11, r1)
    net.addLink(s12, r1)
    net.addLink(s13, r1)
    net.addLink(r3, s9)
    net.addLink(r4, s10)
    net.addLink(r5, s11)
    net.addLink(r6, s12)
    net.addLink(r7, s13)
    net.addLink(h6, s19)
    net.addLink(s19, r7)
    net.addLink(s18, r6)
    net.addLink(s17, r5)
    net.addLink(s16, r4)
    net.addLink(s15, r3)
    net.addLink(h2, s15)
    net.addLink(h3, s16)
    net.addLink(h4, s17)
    net.addLink(h5, s18)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s17').start([])
    net.get('s10').start([])
    net.get('s14').start([])
    net.get('s18').start([])
    net.get('s11').start([])
    net.get('s15').start([])
    net.get('s8').start([])
    net.get('s19').start([])
    net.get('s12').start([])
    net.get('s16').start([])
    net.get('s9').start([])
    net.get('s13').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

