import sys
import numpy as np
import re

PREFIX = {
    'p': -12,
    'n': -9,
    'u': -6,
    'm': -3,
    '': 0,
    'k': 3,
    'M': 6,
    'G': 9,
}

def parse_value(s):
    match = re.fullmatch(r'([-+]?[0-9]*\.?[0-9]+)([pnumkMG]?)', s)
    if not match:
        raise ValueError(f"Invalid numeric value: {s}")
    num = float(match.group(1))
    pref = match.group(2)
    power = PREFIX.get(pref, 0)
    return num * 10**power

class Component:
    pass

class Resistor(Component):
    def __init__(self, name, n1, n2, value):
        self.name=name
        self.n1=n1
        self.n2=n2
        self.value=value

class VSource(Component):
    def __init__(self, name, n_plus, n_minus, value):
        self.name=name
        self.n_plus=n_plus
        self.n_minus=n_minus
        self.value=value

class Circuit:
    def __init__(self):
        self.resistors=[]
        self.vsources=[]
        self.nodes=set(['0'])

    def add_resistor(self, name, n1, n2, value):
        self.resistors.append(Resistor(name,n1,n2,value))
        self.nodes.update([n1,n2])

    def add_vsource(self, name, n_plus, n_minus, value):
        self.vsources.append(VSource(name,n_plus,n_minus,value))
        self.nodes.update([n_plus,n_minus])

    def solve(self):
        node_list=[n for n in self.nodes if n!='0']
        node_index={n:i for i,n in enumerate(node_list)}
        n=len(node_list)
        m=len(self.vsources)
        G=np.zeros((n,n))
        B=np.zeros((n,m))
        I=np.zeros(n)
        E=np.zeros(m)
        # assemble resistor contributions
        for r in self.resistors:
            g=1.0/parse_value(r.value)
            if r.n1!='0':
                i=node_index[r.n1]
                G[i,i]+=g
            if r.n2!='0':
                j=node_index[r.n2]
                G[j,j]+=g
            if r.n1!='0' and r.n2!='0':
                i=node_index[r.n1]
                j=node_index[r.n2]
                G[i,j]-=g
                G[j,i]-=g
        # voltage sources
        for idx,v in enumerate(self.vsources):
            E[idx]=parse_value(v.value)
            if v.n_plus!='0':
                i=node_index[v.n_plus]
                B[i,idx]=1
            if v.n_minus!='0':
                j=node_index[v.n_minus]
                B[j,idx]=-1
        C=B.T
        D=np.zeros((m,m))
        # build MNA matrix
        A=np.block([[G,B],[C,D]])
        z=np.concatenate([I,E])
        x=np.linalg.solve(A,z)
        voltages=x[:n]
        currents=x[n:]
        results={node_list[i]:voltages[i] for i in range(n)}
        for idx,v in enumerate(self.vsources):
            results[v.name+"_i"]=currents[idx]
        return results


def parse_netlist(lines):
    c=Circuit()
    for line in lines:
        line=line.strip()
        if not line or line.startswith('*'):
            continue
        tokens=re.split(r'\s+',line)
        if tokens[0].startswith('R') and len(tokens)>=4:
            name=tokens[0]
            n1,n2,value=tokens[1],tokens[2],tokens[3]
            c.add_resistor(name,n1,n2,value)
        elif tokens[0].startswith('V') and len(tokens)>=4:
            name=tokens[0]
            n_plus,n_minus,value=tokens[1],tokens[2],tokens[3]
            c.add_vsource(name,n_plus,n_minus,value)
        elif tokens[0]=='.op':
            pass
        else:
            raise ValueError(f"Unsupported or invalid line: {line}")
    return c


def main():
    if len(sys.argv)<2:
        print("Usage: python simulator.py <netlist file>")
        return
    with open(sys.argv[1],'r') as f:
        lines=f.readlines()
    c=parse_netlist(lines)
    results=c.solve()
    print("Node voltages and source currents:")
    for k,v in results.items():
        print(f"{k}: {v:.6g}")

if __name__=='__main__':
    main()
