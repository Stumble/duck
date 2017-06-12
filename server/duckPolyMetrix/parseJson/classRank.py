import pagerank

# input = {"a" : {"b" : 1, "c" : 2}, "b" : {}, "c" : {}}
# rst = pagerank.powerIteration(input, rsp=0.15, epsilon=0.00001, maxIterations=1000)

# print rst

class CalcPageRank(object):
    """
    Get pagerank
    """
    def __init__(self):
        self.graph = {}

    def add_node(self, node_name):
        if node_name not in self.graph:
            self.graph[node_name] = {}

    def add_directed_edge(self, start, end, weight):
        self.add_node(start)
        self.add_node(end)
        self.graph[start][end] = weight

    def get_value(self):
        rst = pagerank.powerIteration(self.graph, rsp=0.15, epsilon=0.00001, maxIterations=1000)
        return dict(rst)

if __name__ == '__main__':
    calc = CalcPageRank()
    calc.add_node("ndn::Zone")
    calc.add_node("ndn::Rrset")
    calc.add_directed_edge("ndn::Zone", "ndn::Rrset", 10)
    print calc.get_value()

