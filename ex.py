from itertools import combinations, product
from random import randint, random
import time

import matplotlib.pyplot as plt

import wgraph as wgf

# # Lista de adyacencia de grafo de prueba
#
# grafo = {'A': [('B', 1), ('C', 2), ('D', 3)],
#          'B': [('A', 1), ('C', 4)],
#          'C': [('A', 2), ('B', 4), ('D', 5)],
#          'D': [('A', 3), ('C', 5)]}
#
# # Convertir a grafo ponderado
# g = wgf.WeightedGraph(grafo)
#
# # Ejecutar el algoritmo de djikstra desde el vertice A
# print("# Algoritmo de Djikstra desde el vertice A")
# for node in g:
#     djikstraR = g.djikstra(node)
#     print("\n", djikstraR)
# #
# # print()
#
# # Dibujar el grafo
# # g.drawGraph()

# Funcion para crear listas de adyacencia aleatorias con cierto numero (n) de nodos con cierto umbral para los nodos a crear
def random_graph(n, p, directed=False):
    nodes = range(n)
    adj_mat = [[] for i in nodes]
    possible_edges = product(nodes, repeat=2) if directed else combinations(nodes, 2)
    for u, v in possible_edges:
        if len(adj_mat[u]) * len(adj_mat[v]) < 1 or random() < p:
            adj_mat[u].append( (v, randint(1,10)) )
            if not directed:
                adj_mat[v].append( (u, randint(1,10)) )
    return {vertex: adj_list for vertex, adj_list in enumerate(adj_mat)}

# Clase para construir nuestros experimentos
class Experiment:
    def __init__(self, prob, trials, directed=False):
        self.prob = prob
        self.trials = trials
        self.directed = directed

        self.currentStep = 1
        self.increment = 1

        self.timesPerStep = []
        self.avgTimesPerStep = []

        self.timesPerStepDirected = []
        self.avgTimesPerStepDirected = []
    
    def runStep(self):
        print("\n# STEP " + str(self.currentStep))
        times = []
        for x in range(self.trials):
            graphMat = random_graph(self.currentStep * self.increment, self.prob)
            graph = wgf.WeightedGraph(graphMat)
            start = time.time()

            for node in graph:
                print(graph.djikstra(node))

            end = time.time()
            currentTime = (end - start) * 1000
            times.append(currentTime)
            print("\n# TRIAL " + str(x) + " took " + str(currentTime) + " ms")
        avgTime = sum(times) / len(times)
        self.timesPerStep.append(times)
        self.avgTimesPerStep.append(avgTime)

        print("\n\n# STEP TIMES:", times, "AVG: " + str(avgTime) + " ms")

    def runStepDirected(self):
        print("\n# STEP " + str(self.currentStep))
        times = []
        for x in range(self.trials):
            graphMat = random_graph(self.currentStep * self.increment, self.prob, directed=True)
            graph = wgf.WeightedGraph(graphMat)
            start = time.time()

            for node in graph:
                print(graph.djikstra(node))

            end = time.time()
            currentTime = (end - start) * 1000
            times.append(currentTime)
            print("\n# TRIAL " + str(x) + " took " + str(currentTime) + " ms")
        avgTime = sum(times) / len(times)
        self.timesPerStepDirected.append(times)
        self.avgTimesPerStepDirected.append(avgTime)

        print("\n\n# STEP TIMES:", times, "AVG: " + str(avgTime) + " ms")

    def run(self, steps, increment=1):
        self.increment = increment
        self.steps = steps
        for x in range(steps):
            self.runStep()
            if(self.directed): self.runStepDirected()
            self.currentStep += 1

    def plot(self):
        rows = 1
        if(self.directed): rows = 2
        fig, ax = plt.subplots(rows, self.trials, sharey=True, sharex=True)

        for step in range(self.trials):
            if not self.directed:
                ax[step].bar([str(trial) for trial in range(self.increment, (self.steps + 1) * self.increment, self.increment)], self.timesPerStep[step])
            else:
                ax[0, step].bar([str(trial) for trial in range(self.increment, (self.steps + 1) * self.increment, self.increment)], self.timesPerStep[step])
                ax[0, step].set_title(str((step + 1) * self.increment) + " nodos")
                ax[1, step].bar([str(trial) for trial in range(self.increment, (self.steps + 1) * self.increment, self.increment)], self.timesPerStepDirected[step])
                ax[0, step].set_title(str((step + 1) * self.increment) + " nodos")

        fig.text(0.5, 0.04, 'Numero de Nodos', ha='center', va='center')
        fig.text(0.06, 0.5, 'Tiempo de Ejecucion (ms)', ha='center', va='center', rotation='vertical')
        fig.suptitle('Tiempos de Ejecucion de algoritmo de Djikstra')
        plt.show()

        plt.plot([str(trial) for trial in range(self.increment, (self.steps + 1) * self.increment, self.increment)], self.avgTimesPerStep, label="Ponderado Sin Dirigir")
        if (self.directed): plt.plot([str(trial) for trial in range(self.increment, (self.steps + 1) * self.increment, self.increment)], self.avgTimesPerStepDirected, label="Ponderado Dirigido")

        plt.xlabel("Numero de Nodos")
        plt.ylabel("Tiempo de Ejecucion Promedio (ms)")
        plt.legend()
        plt.show()


# # Construir un experimento con cinco pruebas, es decir de probar con grafos de 1, 2, 3, 4 y 5 nodos, con y sin direccionamiento
# ex = Experiment(0.5, 5, directed=True)
# # Correr 5 pruebas por cada tipo de grafo y numero de nodos
# ex.run(5)
# # Construir y mostrar las graficas con los resultados del experimento
# ex.plot()

# Ahora a correr el experimento de 20 en 20 hasta 100
ex2 = Experiment(0.5, 5, directed=True)
# Correr 5 pruebas por cada tipo de grafo y numero de nodos
ex2.run(5, increment=5)
# Construir y mostrar las graficas con los resultados del experimento
ex2.plot()
