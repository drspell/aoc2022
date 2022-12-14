import sys
import re
import logging as log
from stack import Stack 


if len(sys.argv) > 1:
    # filename = "test_lines_1_21.txt" if '-t' in sys.argv else "input.txt"
    filename = "test.txt" if '-t' in sys.argv else "input.txt"
    debugging = True if '-d' in sys.argv else False
else:
    filename = "input.txt"
    debugging = False

if debugging:
    log.basicConfig(level=log.DEBUG)
else:
    log.basicConfig(level=log.INFO)

class Node:
    DIR = "dir"
    FILE = "file"

    def __init__(self,type,name,parent,nodes=None,size=None):
        self.name = name
        self.type = type
        self._size = size
        self.parent = parent
        self.nodes = None if self.type == Node.FILE else []
        self.path = self._compute_path()

        # print(f"creating node '{self.name}' with path: '{self.path}'")
    
    def _compute_path(self):
        path = [self.name]
        node = self.parent
        # print("compute_path")

        i = 1
        while node is not None:
            # print(f"\t {i} above : {node.name}",end='...')
            path.append(node.name)
            # print(f"path = {path}")
            node = node.parent
            i += 1

        path.reverse()
        return path[0] + '/'.join(path[1:])


    def add_child(self, node):
        self.nodes.append(node)

    def size(self):
        if self.type == Node.FILE:
            return self._size
        else:
            total = 0
            for child in self.nodes:
                # print(f"\t child {child}")
                total += child.size()
            return total
                

    def __str__(self):
        return self.path
        # if self.type == Node.DIR:
            # parent_name = "none" if self.parent is None else self.parent.name
            # return f"<.='{self.name}' ..='{parent_name}'>"
        # else:
            # return f"({self.name},{self._size}) dir: '{self.parent.name}'"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash(self.name + self.type)

    @classmethod
    def dir(cls,name,parent):
        return Node(Node.DIR,name,parent,nodes = [])

    @classmethod
    def file(cls,parent,name,size):
        return Node(Node.FILE,name,parent,nodes=None,size=size)


# file system
def problem1():
    # root_node = Node.dir('/',None)
    # SYS = set([root_node]) #list of directory nodes
    SYS = set() #list of directory nodes
    ENV = {'cwd': None}

    # file_system = {root_node.path : root_node}
    file_system = {}

    CWD = None
    history = Stack()

    # Commands
    CD = 'cd'
    LS = 'ls'
    PS = '$ '

    with open(filename) as F:
        filepos = F.tell()
        ls_mode = False

        for line in F:
            # line = F.readline()
            line = line.rstrip()
            # log.debug(">> "+ line)
            # print(line)
            if line.startswith(PS): 
                cmd = re.findall('\$ (\w+)',line)[0]
                # print("cmd:",cmd)
                if cmd == CD:
                    # handleCMD_CD(line)
                    dirname = re.findall('\$ \w+\s(.*)$',line)[0]

                    relative_path = dirname == '..'

                    if relative_path:
                        CWD = CWD.parent
                    else:
                        # initial condition
                        if CWD is None:
                            # print(f"creating root directory")
                            node = Node.dir(dirname,None)
                            file_system[node.path] = node
                        else:
                            # print(f"** CD to existing directory -- {line}")
                            if CWD.path == '/':
                                path_key = CWD.path + dirname
                            else:
                                path_key = CWD.path + '/' + dirname
                            node = file_system[path_key]
                        CWD = node

                    ls_mode = False
                elif cmd == LS:
                    ls_mode = True
                    # line = F.readline()
                    # filepos = F.tell()

                # move onto next line
                continue

            if ls_mode:
                if line.startswith('dir'):
                    # create a directory with the correct parent
                    dirname = re.findall("dir (.*)",line)[0]
                    # print(f"creating sub directory {line}")
                    node = Node.dir(dirname,CWD)
                
                else:
                    # print(f"in ls_mode parsing line: {line}")
                    matches = re.findall("(\d+) (\w+\.?(?:\w+)?)",line)
                    # print("file name parse matches: ", matches)
                    size, name = matches[0] 
                    # print(f"creating file node: {node}, {line}")
                    node = Node.file(CWD,name,int(size))
                    # file_system[node.path] = node
                    # CWD.add_child(node)

                file_system[node.path] = node
                CWD.add_child(node)
    
    # print(f"file system: {file_system}")
    
    # problem 1
    # result = [ node.size() for path,node in file_system.items() if node.type == Node.DIR and node.size() <= 100000]
    # print(f" problem 1 answer: {sum(result)}")

    # problem 2
    # size of root_directory
    sys_size = file_system['/'].size()
    print(sys_size)
    sys_max = 70000000
    update_space_needed = 30000000
    unused_space = sys_max - sys_size
    
    space_needed = update_space_needed - unused_space 
    print(space_needed)

    dir_to_delete = [node for node in file_system.values() if node.type == Node.DIR and node.size() >= space_needed]
    dir_to_delete.sort(key= lambda n: n.size())
    print(f"problem 2 answer: {dir_to_delete[0].name},{dir_to_delete[0].size()}")


    
 

problem1()
