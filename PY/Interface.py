__author__ = 'lujiji'
import json
import  random

nodes = {}
weight = {}
dfile='wall4_w.json'

##def run():
##    content = open("./wall.json").read()
##    jsonObj = json.loads(content)["edges"]
##    source = jsonObj[random.randrange(0,len(jsonObj))]["from"]
##    target = jsonObj[random.randrange(0,len(jsonObj))]["from"]
##    path = interface(jsonObj, source, target, True)
##    print path

def test():
    with open(dfile) as json_data:
        d = json.load(json_data)
        return d

def run(source, target, isWeighted=False):
    with open(dfile) as json_data:
	d = json.load(json_data)
    jsonObj=d['edges']

    path = interface(jsonObj, source, target, isWeighted)
    print(source,target)
    print(path)
    return path

def getLargestCC():
    content = open(dfile).read()
    jsonObj = json.loads(content)
    edgeList = jsonObj["edges"]
    print(len(edgeList))
    adjList, weightList = transform(edgeList)
    cc_list = []
    dist = {}
    while len(adjList) > 0:
        source = adjList.items()[0][0]
        dist[source] = 0
        queue = [source]
        subData = {}
        while len(queue) > 0:
            u = queue.pop(0)
            dist_u = dist[u]
            neighbor = adjList[u]
            del adjList[u]
            subData[u] = neighbor
            for v in neighbor:
                if v not in dist:
                    dist[v] = dist_u + 1
                    queue.append(v)
        cc_list.append(subData)
    largestCC = cc_list[0]
    for i in range(1, len(cc_list)):
        if len(cc_list[i]) > len(largestCC):
            largestCC = cc_list[i]
    edgeList = restore(largestCC, weightList)
    print(len(edgeList))

    record = {}
    nodesList = []
    for edge in edgeList:
        source = edge["from"]
        if record.has_key(source) is False:
            record[source] = 1
            nodesList.append({"id":source,"label":source})

    jsonObj["edges"] = edgeList
    jsonObj["nodes"] = nodesList
    return jsonObj


def transform(edgeList):
    weightList = {}
    adjList = {}
    for n in range(0,len(edgeList)):
        item = edgeList[n]
        source = item["from"]
        target = item["to"]
        key = "%d,%d" % (source,target)
        weightList[key] = item['weight']
        if adjList.has_key(source) is False:
            adjList[source] = [target]
        elif target not in adjList[source]:
            adjList[source].append(target)

        if adjList.has_key(target) is False:
            adjList[target] = [source]
        elif source not in adjList[target]:
            adjList[target].append(source)
    return adjList, weightList

def restore(adjList, weightList):
    edgeList = []
    for item in adjList.items():
        source = item[0]
        for target in item[1]:
            edge = {"from":source,"to":target,"weight":getWeight(weightList,source,target)}
            edgeList.append(edge)
    return edgeList


def interface(edgeList, s, g, weighted = False):
    nodes, weightList = transform(edgeList)
    path = {}

    if nodes.has_key(s) is False or nodes.has_key(g) is False:
        return path
    
    if weighted is True:
        path = dikstra(nodes,weightList, s, g)
    else:
        path = bfs(nodes, s, g)

    result = []
    for item in path.items():
        result.append({"from":item[0],"to":item[1]})
    return result



def bfs(data, source, target):
    dist = {}
    dist[source] = 0
    queue = [source]
    pre = {}
    path = {}
    distribution = {}
    while len(queue) > 0:
        u = queue.pop(0)
        dist_u = dist[u]
        if u == target:
            while u != source:
                v = pre[u]
                path[u] = v
                u = v
            break
        for v in data[u]:
            if v not in dist:
                dist[v] = dist_u + 1
                queue.append(v)
                pre[v] = u

    return path

def dikstra(data, weightDic, source, target):
    dist = {}
    pre = {}
    path = {}
    for i in range(0, len(data)):
        dist[data.items()[i][0]] = float('inf')
    dist[source] = 0
    queue = BinaryHeap()
    queue.insert(source, 0)
    while len(queue.heap) > 1:
        u = queue.pop()
        if u == target:
            while u != source:
                v = pre[u]
                path[u] = v
                u = v
            break
        for v in data[u]:
            if dist[v] > dist[u] + getWeight(weightDic,u,v):
                dist[v] = dist[u] + getWeight(weightDic,u,v)
                queue.insert(v, dist[v])
                pre[v] = u
    return path


class BinaryHeap:
    def __init__(self):
        self.heap = ['0']
        self.weight = {}

    def insert(self, obj, weight):
        self.weight[obj] = weight
        if obj not in self.heap:
            self.heap.append(obj)
            index = len(self.heap) - 1
            self.up(index)
        else:
            self.reorder(obj)

    def count(self):
        return len(self.heap) - 1

    def reorder(self, obj):
        self.up(self.heap.index(obj))


    def up(self, i):
        cldIndex = i
        while cldIndex//2 > 0:
            parIndex = cldIndex//2
            if self.weight[self.heap[cldIndex]] < self.weight[self.heap[parIndex]]:
                tmp = self.heap[cldIndex]
                self.heap[cldIndex] = self.heap[parIndex]
                self.heap[parIndex] = tmp
                cldIndex = parIndex
            else:
                break

    def pop(self):
        if len(self.heap) > 1:
            result = self.heap[1]
            self.heap[1] = self.heap[-1]
            self.heap.pop()
            self.down(1)
            return result

    def down(self,i):
        parIndex = i
        while parIndex*2 <= len(self.heap) - 1:
            minChild =self.minChild(parIndex)
            if self.weight[self.heap[parIndex]] > self.weight[self.heap[minChild]]:
                tmp = self.heap[parIndex]
                self.heap[parIndex] = self.heap[minChild]
                self.heap[minChild] = tmp
                parIndex = minChild

            else:
                break


    def minChild(self,parIndex):
        if parIndex*2+1 > len(self.heap) - 1:
            return parIndex*2
        else:
            if self.weight[self.heap[parIndex*2]]>self.weight[self.heap[parIndex*2+1]]:
                return parIndex*2+1
            else:
                return parIndex*2



def getWeight(weightDic, source, target):
    key = "%d,%d" % (source,target)
    if key not in weightDic.keys():
        key = "%d,%d" % (target,source)
    return weightDic[key]
