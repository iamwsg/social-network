__author__ = 'lujiji'
import json
import  random

nodes = {}
weight = {}

def run(source, target):
    with open('wall.json') as json_data:
	d = json.load(json_data)
    jsonObj=d['edges']
    #content = open("./wall_l.json").read()
    #jsonObj = json.loads(content)
    #source = jsonObj[random.randrange(0,len(jsonObj))]["from"]
    #target = jsonObj[random.randrange(0,len(jsonObj))]["from"]
    #source = 41483
    #target = 60168
    path = interface(jsonObj, None, source, target)
    print(source,target)
    print(path)
    return path

def interface(edgeList, weightList, s, g, weighted = False):
    for n in range(0,len(edgeList)):
        item = edgeList[n]
        source = item["from"]
        target = item["to"]
        if nodes.has_key(source) is False:
            nodes[source] = [target]
        elif target not in nodes[source]:
            nodes[source].append(target)

        if nodes.has_key(target) is False:
            nodes[target] = [source]
        elif source not in nodes[target]:
            nodes[target].append(source)

    path = {}
    if weight is True:
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
    key = source+','+target
    if key not in weightDic.keys():
        key = target+','+source
    return weightDic[key]
