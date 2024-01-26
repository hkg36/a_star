import sys
import math

#地图(从文件中获取的二维数组)
maze=[]
#起点
start=None
#终点
end=None
#开放列表（也就是有待探查的地点）
open_list={}
#关闭列表  (已经探查过的地点和不可行走的地点)
close_list={}
#地图边界(二维数组的大小，用于判断一个节点的相邻节点是否超出范围)
map_border=()
#方向
orientation=[]

class Node(object):
    @staticmethod
    def buildNode(father,x,y):
        if x<0 or x>=map_border[0] or y<0 or y>=map_border[1]:
            return None
        if (x,y) in close_list:
            return None
        newnode=Node()
        newnode.father=father
        newnode.x=x
        newnode.y=y

        if father !=None:
            newnode.G=newnode.G_to_Self(father)
            newnode.H=distance(newnode,end)
            newnode.F=newnode.G+newnode.H
        else:
            newnode.G=0
            newnode.H=0
            newnode.F=0
        return newnode
    def G_to_Self(self,from_node):
        if from_node.father==None:
            return from_node.G+1
        else:
            prenode=from_node.father
            #尽量不转向
            if (prenode.x==from_node.x and from_node.x==self.x) or (prenode.y==from_node.y and from_node.y==self.y):
                return from_node.G+1
            else:
                return from_node.G+1.2

    def reset_father(self,father,new_G):
        if father!=None:
            self.G=new_G
            self.F=self.G+self.H

        self.father=father

#计算距离
def distance(cur,end):
    return math.sqrt(math.pow(cur.x-end.x,2)+math.pow(cur.y-end.y,2))
        

#在open_list中找到最小F值的节点
def min_F_node():
    global open_list
    if len(open_list)==0:
        raise Exception('路径不存在')

    _min=9999999999999999
    _k=(start.x,start.y)

    #以列表的形式遍历open_list字典
    for k,v in open_list.items():
        if _min>v.F:
            _min=v.F
            _k=k

    return open_list[_k]

#把相邻的节点加入到open_list之中，如果发现终点说明找到终点
def addAdjacentIntoOpen(node):
    global open_list,close_list
    
    #首先将该节点从开放列表移动到关闭列表之中
    open_list.pop((node.x,node.y))
    close_list[(node.x,node.y)]=node
    adjacent=[]

    for i,j in ((0,1),(0,-1),(1,0),(-1,0)):
        nnode=Node.buildNode(node,node.x+i,node.y+j)
        if nnode:adjacent.append(nnode)

    #检查每一个相邻的点
    for a in adjacent:
        #如果是终点，结束
        if (a.x,a.y)==(end.x,end.y):
            new_G=end.G_to_Self(node)
            end.reset_father(node,new_G)
            return True
        #如果不在open_list中，则添加进去
        if (a.x,a.y) not in open_list:
            open_list[(a.x,a.y)]=a
        #如果存在在open_list中，通过G值判断这个点是否更近 
        else:
            exist_node=open_list[(a.x,a.y)]
            new_G=exist_node.G_to_Self(node)
            if new_G<exist_node.G:
                exist_node.reset_father(node,new_G)

    return False

#查找路线
def find_the_path(start,end):
    global open_list
    open_list[(start.x,start.y)]=start

    the_node=start
    try:
        while not addAdjacentIntoOpen(the_node):
            the_node=min_F_node()

    except Exception as err:
        #路径找不到
        print(err)
        return False
    return True

#读取文件，将文件中的信息加载到地图(maze)信息中
def readfile(url):
    global maze,map_border
    with open(url) as f:
        allline=[list(map(int,l.split())) for l in f.readlines()]
        maze=allline
        map_border=(len(maze[0]),len(maze))


#通过递归的方式根据每个点的父节点将路径连起来
pathpos=set()
def mark_path(node):
    global orientation,pathpos
    while True:
        pathpos.add((node.x,node.y))
        if node.father==None:     
            return
        
        #print('({x},{y})'.format(x=node.x,y=node.y))
        #将方向信息存储到方向列表中
        if node.father.x-node.x>0:
            orientation.append('L')
        elif node.father.x-node.x<0:
            orientation.append('R')
        elif node.father.y-node.y>0:
            orientation.append('U')
        elif node.father.y-node.y<0:
            orientation.append('D')
        node=node.father
    
#解析地图,把不可走的点直接放到close_list中
def preset_map():
    global start,end,map_bloder,maze
    for i in range(len(maze)):
        l=maze[i]
        for j in range(len(l)):
            o=l[j]
            if o==1:
                block_node=Node.buildNode(None,j,i)
                close_list[(block_node.x,block_node.y)]=block_node
            if o==2:
                start=Node.buildNode(None,j,i)
            if o==3:
                end=Node.buildNode(None,j,i)

def printMap():
    for i in range(len(maze)):
        l=maze[i]
        for j in range(len(l)):
            o=l[j]
            if (j,i) in pathpos:
                print(f"\u25CB",end="")
            elif o==1:
                print(f"\u2588",end="")
            elif o==0:
                print(f" ",end="")
        print("\n",end="")
if __name__=='__main__':
    #判断在控制台输入的参数时候达到要求
        #从控制台读取参数
    readfile("map.txt")

    preset_map()

    #判断起点终点是否符合要求
    if (start.x,start.y) in close_list or (end.x,end.y) in close_list:
        raise Exception('输入的坐标不可走')

    if find_the_path(start,end):
        mark_path(end)
    printMap()

    #列表方向调整为起点开始
    orientation.reverse()
    str_ori=''
    for o in orientation:
        str_ori=str_ori+o+' '
    print(str_ori)