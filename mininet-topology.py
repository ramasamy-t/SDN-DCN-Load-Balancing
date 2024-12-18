from mininet.topo import Topo

class CustomTopology(Topo):
    def build(self):
        # Create switches (with OpenFlow enabled)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch('s10')
        
        # Create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        
        # Add links between core and aggregation switches
        self.addLink(s1, s3)
        self.addLink(s1, s5)
        self.addLink(s2, s4)
        self.addLink(s2, s6)
        
        # Add links between aggregation and edge switches
        self.addLink(s3, s7)
        self.addLink(s3, s8)
        self.addLink(s4, s7)
        self.addLink(s4, s8)
        self.addLink(s5, s9)
        self.addLink(s5, s10)
        self.addLink(s6, s9)
        self.addLink(s6, s10)
        
        # Add links between edge switches and hosts
        self.addLink(s7, h1)
        self.addLink(s7, h2)
        self.addLink(s8, h3)
        self.addLink(s8, h4)
        self.addLink(s9, h5)
        self.addLink(s9, h6)
        self.addLink(s10, h7)
        self.addLink(s10, h8)

# Instantiate and start the topology
topos = {'customtopo': (lambda: CustomTopology())}
