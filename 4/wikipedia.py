import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file, 'r', encoding='utf-8') as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file, 'r', encoding='utf-8') as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = [key for key, value in self.titles.items() if value == start][0]
        goal_id = [key for key, value in self.titles.items() if value == goal][0]
        queue = collections.deque([(start_id, [start_id])])  # make queue
        # found_paths = [] # 見つかった最短経路のパスを格納
        found_paths = False
        # current_depth = 1

        while queue: # キューが空になるまで
            next_queue = collections.deque() # 次の深さのノードを処理するためのキューを用意
            while queue: # 今の深さのキューが空になるまで
                pop_node = queue.popleft()  # 末尾を１つdeque
                pop_id = int(pop_node[0])
                path = pop_node[1]
                enqueue = self.links[pop_id] # dequeしたノードの次ノード配列を取得

                for x in enqueue:
                    if x == goal_id: # ノードがgoalなら、パスの末尾に加えそのパスを見つかったパス配列に格納
                        # found_paths.append(path + [x])
                        found_paths = True
                        for id in path+[x]:
                            print(self.titles[id] + " ", end="")
                        print()
                    else: # goalでなかったら、pathを更新して次の深さを処理するキューに格納
                        next_queue.append((x, path + [x]))

            if found_paths: # ある深さxについてすべての経路を探索し終えたときにgoalへのpathが見つかっていれば
            # すべての最短経路を表示
                # for path in found_paths:
                #     for id in path:
                #         print(self.titles[id] + " ", end="")
                #     print()
                break   
        
            queue = next_queue # 処理を続行する場合、1つ深いノードのキューを処理対象とする
            # current_depth += 1 

        if not found_paths:
            print("Not found the route")
        return
    
    # def find_shortest_path(self, start, goal):
    #     start_id = [key for key, value in self.titles.items() if value == start][0]
    #     goal_id = [key for key, value in self.titles.items() if value == goal][0]
    #     queue = collections.deque([(start_id,[start_id])]) # make queue
    #     judge = False
    #     min = 100000000
    #     while True:
    #         pop_node = queue.popleft() # 末尾を１つdeque
    #         pop_id = int(pop_node[0])
    #         path = pop_node[1]
    #         # print(pop_id)
    #         enqueue = self.links[pop_id]
    #         for x in enqueue:
    #             if x != goal_id:
    #                 queue.append((x, path + [x]))
    #             else:
    #                 # judge = True
    #                 path.append(x)
    #                 min = len(path)
    #                 for id in path:
    #                     print(self.titles[id] + " ", end="")
    #                 print()
    #                 # break
    #         if judge:
    #             break
    #         if len(queue) == 0:
    #             print("Not found the route")
    #             break
    #     return


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        self.ranks = {key: 1.0 for key in self.links}
        # new_ranks = {key: 0 for key in self.links}
        num_pages = len(self.links)
        # k=0
        while True:
            # print(k)
            # k+=1
            sum_rank = 0
            new_ranks = {key: 0 for key in self.links}
            for page, links in self.links.items(): # 各ページにおいて
                # print(k, page)

                if len(links) == 0: # リンク先がなかったら等配分
                    for key, value in new_ranks.items():
                        new_ranks[key] = 1 / len(new_ranks)
                        sum_rank += 1 / len(new_ranks)
                else:
                    for key,value in new_ranks.items(): # 全ページにおいて
                        if key in links: # ページがリンクされていたら
                            new_ranks[key] += self.ranks[page] * 0.85 / len(links) #元のページランクの0.85を等配分
                            sum_rank += self.ranks[page] * 0.85 / len(links) 
                        else: # リンクされていなかったら、元のページランクの0.15を等配分
                            new_ranks[key] += self.ranks[page] * 0.15 / (len(new_ranks)-len(links))
                            sum_rank += self.ranks[page] * 0.15 / (len(new_ranks)-len(links))
                    # print(sum, self.ranks, new_ranks)
                    
            if self.ranks == new_ranks:
                new_ranks = sorted(new_ranks.items(), key = lambda x : x[1])
                for i in range(min(10, len(self.ranks))):
                    print(new_ranks[i])
                break
            else:
                self.ranks = new_ranks.copy()
            if round(sum_rank) != len(self.ranks):
                print(round(sum_rank))
                break
        return

    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # wikipedia.find_shortest_path("ねこ", "さめ")
    # wikipedia.find_shortest_path("A", "F")
    # wikipedia.find_most_popular_pages()