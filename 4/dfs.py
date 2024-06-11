#! /usr/bin/python3
import collections


# An example graph structure
links = {"A": ["B","E","G"],
         "B": ["C"],
         "C": ["D"],
         "D": ["E"],
         "E": ["B","F"],
         "F": [],
         "G": ["F"]}


# A helper function to find a path.
def find_path(goal, previous):
    path = []
    node = goal
    path.append(node)
    while previous[node]:
        node = previous[node]
        path.append(node)
    path.reverse()
    return path


# dfs_with_recursion finds A -> B -> C -> D -> E -> F first.
def dfs_with_recursion(start, goal):
    print("dfs_with_recursion:")
    visited = {}
    previous = {}

    visited[start] = True
    previous[start] = None
    recursion(start, goal, visited, previous)

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
    else:
        print("Not found")

def recursion(node, goal, visited, previous):
    if node == goal:
        return True
    for child in links[node]:
        if not child in visited:
            visited[child] = True
            previous[child] = node
            if recursion(child, goal, visited, previous):
                return True
    return False


# dfs_with_stack finds A -> G -> F first.
def dfs_with_stack(start, goal):
    print("dfs_with_stack:")
    stack = collections.deque()
    visited = {}
    previous = {}

    stack.append(start)
    visited[start] = True
    previous[start] = None
    while len(stack):
        node = stack.pop()
        if node == goal:
            break
        for child in links[node]:
            if not child in visited:
                stack.append(child)
                visited[child] = True
                previous[child] = node

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
    else:
        print("Not found")


# Challenge quiz: Implement DFS using a stack that visits nodes and edges
# in the same order as dfs_with_recursion. In other words, implement DFS that
# finds A -> B -> C -> D -> E -> F first using a stack.
def dfs_with_stack_in_the_recursion_order(start, goal):
    print("dfs_with_stack_in_the_recursion_order:")
    stack = collections.deque()
    visited = {}
    previous = {}
    
    for i in links:# visitedを Falseで初期化
        visited[i] = False

    stack.append(start)
    visited[start] = True
    previous[start] = None

    node = start # ノードの初期値をstartにセット
    # count = 0
    while stack: # stackが空になるまで
        if node == goal: # ノードがgoalの場合終了
            break
        judge = False

        children = links[node]
        
        for child in children:
            # count += 1
            if visited[child] == False: # 未探索の子ノードがいればそこに移動、探索済フラグを立てる
                judge = True
                stack.append(child)
                visited[child] = True
                previous[child] = node
                node = child
                break
        if not judge: # (未探索の)子がいなかったらスタックからpopし新たなnodeに設定, whileで戻って再びその子ノードを探索
            # stack.pop() # ←必要
            node = stack.pop()

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
        # print(count)
    else:
        print("Not found")


dfs_with_recursion("A", "F")
dfs_with_stack("A", "F")
dfs_with_stack_in_the_recursion_order("A", "F")