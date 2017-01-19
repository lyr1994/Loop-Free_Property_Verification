#########
from z3 import *
import random


class loopDetection:
    def __init__(self):
		#[[s1,i1],[s2,i2],[s3,i3]]
        self.loopTable={}
        self.currentTable={}

		#network maintains all network link between switches
		#if s1 and s2 are linked by i1 and i2, then key=s1, value=[s2,i1,i2]] is an element in the network
		#here, we have s1<s2, where s1 and s2 are all string(strings can compare between each other with ascii)
        self.network={}
        self.graph={}

    def addSwitch(self, Switch):
        if self.currentTable.has_key(Switch):
            print "Switch ", Switch, " already exists!"
            return
        else:
            self.currentTable[Switch] = {}
            for i in range(4):
                self.currentTable[Switch][i]=[]
        #print self.currentTable

    def addRule(self, Switch, Interface, Ipprefix):
        if self.currentTable.has_key(Switch)==False:
            print "Switch does not exist!"
            return
        elif self.currentTable[Switch].has_key(Interface) == False:
            print "Switch does not have interface ", Interface
            return
        else:
            self.currentTable[Switch][Interface].append(Ipprefix)
        #print self.currentTable

    def addlink(self, S1, I1, S2, I2):
        if S1==S2:
            print "Link cannot be added between same switch"
            return
		#elif S1<S2:
		#	if self.network.has_key(S1):
		#		self.network[S1].append([S2,I1,I2])
		#	else:
		#		self.network[S1]=[]
		#		self.network[S1].append([S2,I1,I2])
        else:
            if self.network.has_key(S2):
                self.network[S2].append([S1,I2,I1])
                self.graph[S2].append(S1)
            else:
                self.network[S2]=[]
                self.network[S2].append([S1,I2,I1])
                self.graph[S2]=[]
                self.graph[S2].append(S1)
            if self.network.has_key(S1):
                self.network[S1].append([S2,I1,I2])
                self.graph[S1].append(S2)
            else:
                self.network[S1]=[]
                self.network[S1].append([S2,I1,I2])
                self.graph[S1]=[]
                self.graph[S1].append(S2)
        #print self.network

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        #if self.network.has_key(start) == False:
        #    return []
        paths = []
        for node in self.network[start]:
            if node[0] not in path:
                newpaths = self.find_all_paths(node[0], end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_all_loops(self, node):
        loops = []
        for item in self.network:
            if node not in self.graph[item]:
                continue
            paths = self.find_all_paths(node, item)
            if paths == None:
                continue
            for path in paths:
                temp = path + [node]
                loops.append(temp)
        return loops
            
    def check_link(self, start, end):
        
        for item in self.network[start]:
            if item[0] == end:
                #link1.append((start,item[1]))
                #link2.append((end, item[2]))
                link1 = (start, item[1])
                link2 = (end, item[2])
                break

        #print link
        return link1, link2

    def localloop(self):
		#add loop information here
		#for example, [s1,i2]-[s2,i3], [s2,i1]-[s3,i0], [s3,i1]-[s1,i1], then
		#loopTable[[s1,i2]]=[[[s1,i2],[s2,i3],[s2,i1],[s3,i0],[s3,i1],[s1,i1]]]
		#here [[s1,i2],[s2,i3],[s2,i1],[s3,i0],[s3,i1],[s1,i1]] is an element in the
		#loopTable[[s1,i2]]

        for node in self.network:
            loops = self.find_all_loops(node)
            #print "node is ", node, " and loop is ",loops
            for loop in loops:
                link = []
                for i in range (0,len(loop)-1):
                    temp1, temp2 = self.check_link(loop[i],loop[i+1])
                    link.append(temp1)
                    link.append(temp2)
                    if i == 0:
                        key = temp1
                #print link, key
                if self.loopTable.has_key(key):
                    self.loopTable[key].append(link)
                else:
                    self.loopTable[key] = []
                    self.loopTable[key].append(link)
        #print self.loopTable
        #self.loopTable[("s1",1)]=[[("s1",1),("s2",3),("s2",1),("s3",0),("s3",1),("s1",1)]]
        #self.loopTable[("s2",1)]=[[("s2",1),("s3",0),("s3",1),("s1",1),("s1",2),("s2",3)]]
        #self.loopTable[("s3",1)]=[[("s3",1),("s1",1),("s1",2),("s2",3),("s2",1),("s3",0)]]



    def ifNewRuleCorrect(self,Switch,Interface,IpPrefix):
    	#input is Switch and Interface, return a set that contains all loops in switch(as nodes) and the interface(the edge)
        allLops=self.loopTable[(Switch, Interface)]
        possibleIp=Int('possibleIp')
        for loop in allLops:
            s = Solver()
            TotalConstrain=[]
        	# this returns all switch(as nodes) and all edges(as switchs interface) in one speicific loop
            allSwtichInfo=loop
            count =0;
            for switchInfo in allSwtichInfo:
                if count%2 == 0:
            	# get the ip prefix set for a specific switch and a interface
                    allIpPrefixSet=self.currentTable[switchInfo[0]][switchInfo[1]]
                    allConstrain=[]
                    for IpPrefix1 in allIpPrefixSet:
                        lowerBound=IpPrefix1[0]
                        uperBound=IpPrefix1[1]
                        constrain=And(possibleIp >= lowerBound, possibleIp<= uperBound)
                        allConstrain.append(constrain)
                    if (Switch==switchInfo[0]) and (Interface == switchInfo[1]):
                        lowerBound=IpPrefix[0]
                        uperBound=IpPrefix[1]
                        constrain=And(possibleIp >= lowerBound, possibleIp<= uperBound)
                        allConstrain.append(constrain)
                    allConstrain.append(False)
                    constrains=Or(allConstrain)
                    TotalConstrain.append(constrains)
                count=count+1
            allLoopConstrain=And(TotalConstrain)
            s.add(allLoopConstrain)
            if s.check() == sat :
                print "it is not ok"
                return False
        print "it is ok"
        return True


def two_random(min_ipprefix, max_ipprefix):
    rand1 = random.randint(min_ipprefix,max_ipprefix)
    rand2 = rand1
    while(rand2 == rand1):
        rand2 = random.randint(min_ipprefix, max_ipprefix)
    if rand1 < rand2:
        return rand1, rand2
    else:
        return rand2, rand1

possible_switch_interface = []


if __name__=="__main__":
    loop=loopDetection()
    


    loop.addSwitch("s1")
    loop.addSwitch("s2")
    loop.addSwitch("s3")
    loop.addRule("s1",1,(1,16))
    loop.addRule("s1",2,(17,32))
    loop.addlink("s1",1,"s2",2)
    loop.addlink("s2",3,"s3",1)
    loop.addlink("s3",3,"s1",0)
    loop.localloop()
    #print "initialization end"
    #print possible_switch_interface

    #test
    #for i in range(500):
    #    rand = random.choice(possible_switch_interface)
    #    rand1, rand2 = two_random(min_ipprefix, max_ipprefix)
    #    loop.ifNewRuleCorrect(rand[0],rand[1],(rand1,rand2))
    loop.ifNewRuleCorrect("s1",1,(17,20))






