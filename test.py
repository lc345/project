# 1,2,3
# 4,5,6
# 7,8,9
from collections import defaultdict
import multiprocessing
import random
from typing import List

exit_case = dict()  # 求组合总和的本地缓存

waiting_handle_path_map = {
    "0":{
        "1": [[1,2],[1,2,3],[1,4],[1,5],[1,2,6],[1,4,7],[1,4,8],[1,5,9]],
        "2": [[2,3],[2,4],[2,5],[2,6],[2,5,7],[2,5,8],[2,5,9]],
        "3": [[3,2,4],[3,5],[3,6],[3,5,7],[3,6,8],[3,6,9]],
        "4": [[4,5],[4,5,6],[4,7],[4,8],[4,5,9]],
        "6": [[6,5],[6,5,7],[6,8],[6,9]],
        "7": [[7,5],[7,8],[7,8,9]],
        "8": [[8,5],[8,9]],
        "9": [[9,5]],
    },
}


class ConvertPathsToGraph():
    def __init__(self, paths_map) -> None:
        self.paths_map = paths_map  # type: dict[dict]

    def __generate_graph_by_path(
        self, 
        path_list  # typr: List[List]
    ):
        graph = defaultdict(list)
        for paths in path_list:
            for i in range(len(paths)):
                if i == len(paths)-1:
                    if paths[i] in graph.keys():continue
                    # 图的叶子节点的情况
                    graph[paths[i]] = []
                    continue
                else:
                    graph[paths[i]].append(paths[i+1])
                    
        result = {}
        for key, value in graph.items():
            # 去重（可能有重复值）& 转成字符串
            result[str(key)] = list(map(str, list(set(value))))

        return result

    def do(self):
        result = {}
        for first_key, paths in self.paths_map.items():
            temp_result = {}
            for second_key, path_list in paths.items():
                graph = self.__generate_graph_by_path(path_list)
                temp_result[second_key] = graph

            result[first_key] = temp_result

        return result


# 所有图，带编号，处理数据时候只需要知道是哪个编号，其实只需要生成一次存起来就好
all_graph = ConvertPathsToGraph(waiting_handle_path_map).do()  # type: dict[dict[dict]]


class GetAllGraphWeight():
    def __init__(self, graph, graph_weight, right_path_value, target, num_range) -> None:
        self.graph = graph # 图
        self.graph_weight = graph_weight # 图对应的权值（不是严格意义上的权值）
        self.right_path_value = right_path_value # 唯一正确的路径是什么
        self.target = target # 不能等于的数是多少
        self.num_range = num_range # 每个数的取值范围是多少
        self.temp_graph_weight = [] # 临时存放的权值
        self.used_graph = [] # 不满足条件的图，当本地缓存用

    def __get_valid_value(self, node, total=0):
        # 已经有确定的权值

        if self.graph_weight[int(node)]:
            return self.graph_weight[int(node)]
        
        # 任意返回一个和不是目标数的, 需要在排除一个数之后的范围里面选择一个
        if total < self.target:
            exclude_number = self.target-total
            total_range = list(range(self.num_range+1))
            total_range.remove(0)
            if exclude_number in total_range:
                total_range.remove(exclude_number)
            return random.choice(total_range)
        # 任意返回一个即可
        else:
            return random.randint(1, self.num_range+1)
        
    def __dfs(self, graph, begin_node, total):
        for i in graph[begin_node]:
            value = self.__get_valid_value(i, total)
            total+=value
            self.temp_graph_weight[int(i)] = value
            self.__dfs(graph, i, total)
            total-=value

    def __get_one_random_case(self, begin_node):
        max_graph = self.graph['1'] # TODO: 更合理的方式
        self.temp_graph_weight = self.graph_weight
        begin_sum = self.__get_valid_value(begin_node, 0)
        self.__dfs(max_graph, begin_node, begin_sum)
        return self.temp_graph_weight

    def do(self):
        # 1. 先找到最大那个图(通常是第一个)满足条件的一个case
        random_one_case = self.__get_one_random_case("1")
        print(random_one_case)

        # 2. 遍历其他图是否全都满足条件

        # 3. 满足返回结果，不满足加入本地缓存，下次不用

        pass


class CombinationSum():
    def __init__(self) -> None:
        self.path = []
        self.sub_path = []

    def __dfs(self, number, target, num_range, total):
        if total > target:
            return
        
        if len(self.sub_path) > number:
            return
        
        if len(self.sub_path) == number and total == target:
            self.path.append(self.sub_path[:])
            return

        for i in range(1, num_range+1):
            self.sub_path.append(i)
            total+=i
            self.__dfs(number, target, num_range, total)
            total-=i
            self.sub_path.pop()

        return self.path

    def do(self, number, target, num_range):
        result = self.__dfs(number, target, num_range, 0)
        return result


class GetResult():
    def __init__(self, number, num_range, number_of_result, map_id, right_path, total_number) -> None:
        self.number = number # 几个数
        self.num_range= num_range # 每个数的范围
        self.number_of_result = number_of_result # 要几个结果
        self.target = None # 这几个数和是几
        self.map_number = map_id # 地图编号
        self.right_path = right_path # 正确的路径，eg. "c,b,a"
        self.total_number = total_number # 一共多少个数
        self.lock = multiprocessing.Lock()

    def __get_right_path_all_results(self):
        combination_results = []

        # 先从本地缓存拿
        key = (self.number, self.target, self.num_range)
        if key in exit_case.keys():
            print("get from local cache, key: %s" % (key,))
            combination_results = exit_case[key]
            return combination_results

        # 没有再重新计算
        combination_results = CombinationSum().do(self.number, self.target, self.num_range)

        # 多进程并发安全
        if combination_results:
            self.lock.acquire()
            exit_case[key] = combination_results
            self.lock.release()

        return combination_results

    def __get_one_path_result(self, combination_result):
        # 1. 根据地图的编号获取地图的形式
        graph = all_graph[self.map_number]  # type: dict

        # 2. 将正确路径赋值给该地图（给正确路径加权, 但是其实并不是真正意义上的权值）
        right_path_to_int = []
        graph_weight = [0]*(self.total_number+1)
        right_path_list = self.right_path.split(",")
        for i in range(len(right_path_list)):
            right_path_value = ord(right_path_list[i])-ord('a')+1 # 索引是0的不存储值
            right_path_to_int.append(right_path_value)
            graph_weight[right_path_value] = combination_result[i]

        # 3. 获取图的其他权值
        result = GetAllGraphWeight(graph, graph_weight, right_path_value, self.target, self.num_range).do()

        return result

    def do(self, target):
        self.target = target  # 有点奇怪，但是方便做多进程参数传参

        # 1. 求出正确路径的所有情况
        combination_results = self.__get_right_path_all_results()  # type: List[List]

        # 2. 遍历正确路径，获取每一个路径的正确结果
        result = []
        for combination_result in combination_results[0:1]:
            result.extend(self.__get_one_path_result(combination_result))

        # 3. 返回正确结果，随机取规定数量结果
        return random.sample(result, self.number_of_result)


result = GetResult(3, 9, 20, '0', "c,b,a", 9).do(15)