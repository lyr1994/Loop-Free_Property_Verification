# Copyright (c) Microsoft Corporation 2015, 2016

# The Z3 Python API requires libz3.dll/.so/.dylib in the 
# PATH/LD_LIBRARY_PATH/DYLD_LIBRARY_PATH
# environment variable and the PYTHON_PATH environment variable
# needs to point to the `python' directory that contains `z3/z3.py'
# (which is at bin/python in our binary releases).

# If you obtained example.py as part of our binary release zip files,
# which you unzipped into a directory called `MYZ3', then follow these
# instructions to run the example:

# Running this example on Windows:
# set PATH=%PATH%;MYZ3\bin
# set PYTHONPATH=MYZ3\bin\python
# python example.py

# Running this example on Linux:
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:MYZ3/bin
# export PYTHONPATH=MYZ3/bin/python
# python example.py

# Running this example on OSX:
# export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:MYZ3/bin
# export PYTHONPATH=MYZ3/bin/python
# python example.py


from z3 import *

class CurrentSwitchTable:
    def _init_(self):
        self.currentTable={}
    
    def addSwitch(self,Switch):
        if Switch not in self.currentTable:
            newRoutetable={}
            self.currentTable[Switch]=newRoutetable

    def addRouteRule(self,Switch,IpPrefix,Interface):
        Routetable=self.currentTable[Switch]
        if IpPrefix in Routetable:
            Routetable


class LoopInfo:


def ifNewRuleCorrect(Switch,Interface,IpPrefix):
    #input is Switch and Interface, return a set that contains all loops in switch(as nodes) and the interface(the edge)
    allLops=LoopInfo.get(Switch,Interface);
    possibleIp=Int('possibleIp')
    for loop in allLops:
        s = Solver()
        # this returns all switch(as nodes) and all edges(as switchs interface) in one speicific loop
        allSwtichInfo=loop.getSwitchInfo
        for switchInfo in allSwtichInfo:
            # get the ip prefix set for a specific switch and a interface
            allIpPrefixSet=currentTable.getIpPrefix(switchInfo)
            for IpPrefix1 in allIpPrefixSet:
                lowerBound=Ip.getLower(IpPrefix1)
                uperBound=Ip.getUper(IpPrefix1)
                s.add(possibleIp >= lowerBound)
                s.add(possibleIp <= uperBound)
            if Switch=switchInfo.Switch && Interface = switchInfo.Interface:
                lowerBound=Ip.getLower(IpPrefix)
                uperBound=Ip.getUper(IpPrefix)
                s.add(possibleIp >= lowerBound)
                s.add(possibleIp <= uperBound)
        if s.check() == "sat"
            return false
    return true
