import numpy as np

class node():
    def __init__(self,value = None):
        self.value = value
        self.next = None

class queue():
    def __init__(self):
        self.head = None
        self.last = None
        self.len = 0
    
    def add(self,elemento):
        self.len += 1
        no = node(elemento)
        if self.last is None:
            self.last = no 
        else:
            self.last.next = no
            self.last = no
        if self.head is None:
            self.head = no
    
    def remove(self):
        if self.head is None:
            raise IndexError
        else:
            valor = self.head.value
            self.head = self.head.next
        if self.head is None:
            self.last is None 
        self.len -= 1
        return valor 

class linked_list():
    def __init__(self):
        self.head = None
    def add_value(self, value):
        if self.head:
            ponteiro = self.head
            while ponteiro.next:
                ponteiro = ponteiro.next
            ponteiro.next = node(value)
        else:
            self.head = node(value)
    
    def __repr__(self):
        p = ""
        ponteiro = self.head
        while(ponteiro):
            p= p + str(ponteiro.value) + " "
            ponteiro = ponteiro.next
        return p

class MinHeap():
    def __init__(self):
        self.heap = []
        self.tamanho = 0
    
    def getPai(self,index):
        return (index-1)//2
    
    def getFilhoDireito(self, index):
        return 2*index + 2
    
    def getFilhoEsquerdo(self, index):
        return 2*index + 1
   
    def temPai(self, index):
        return self.getPai(index) >= 0
    
    def temFilhoDireito(self, index):
        return self.getFilhoDireito(index) <= self.tamanho - 1
    
    def temFilhoEsquerdo(self, index):
        return self.getFilhoEsquerdo(index) <= self.tamanho - 1
    

    def insercao(self, data):
        self.heap.append(data)
        self.tamanho += 1
        self.HeapUp(self.tamanho - 1)
    
    def HeapUp(self, index):
        while self.temPai(index) and self.heap[self.getPai(index)][0] > self.heap[index][0]:
            self.heap[self.getPai(index)], self.heap[index] = self.heap[index], self.heap[self.getPai(index)]
            index = self.getPai(index)
    
    def RemoveMinimo(self):
        if self.tamanho == 0:
            raise("Está Vazio")
        dado = self.heap[0]
        self.heap[0] = self.heap[self.tamanho - 1]
        self.heap.pop()
        self.tamanho -= 1
        self.HeapDown()
        return dado
    
    def HeapDown(self, index = 0):
        while self.temFilhoEsquerdo(index):
            menorfilho = self.getFilhoEsquerdo(index)
            if self.temFilhoDireito(index) and self.heap[self.getFilhoDireito(index)][0] < self.heap[self.getFilhoEsquerdo(index)][0]:
                menorfilho = self.getFilhoDireito(index)
            if self.heap[index][0] < self.heap[menorfilho][0]:
                break
            else:
                self.heap[index], self.heap[menorfilho] = self.heap[menorfilho], self.heap[index]
            index = menorfilho
    
    def atualiza(self, indice, valor):
        self.heap[indice] = valor
        if self.heap[indice][0] < self.heap[self.getPai]:
            self.HeapUp(indice)
        elif self.temFilhoEsquerdo(indice) and self.heap[self.getFilhoEsquerdo(indice)][0] < self.heap[self.heap[indice]][0]:
            self.HeapDown(indice)
                      
def BFS_list(lista, vertices,elemento, ponderado):
    pai, nivel, marca = [-1 for i in range(vertices)], [-1 for i in range(vertices)],  [0 for i in range(vertices)]
    f = queue()
    pai[elemento-1], nivel[elemento-1] = None, 0
    marca[elemento -1] = 1
    f.add(elemento)
    while f.len != 0:
        v = f.remove()
        ponteiro = lista[v-1].head
        if not ponderado:
            while ponteiro:
                if marca[ponteiro.value - 1] == 0:
                    marca[ponteiro.value - 1] = 1
                    pai[ponteiro.value - 1] = v
                    nivel[ponteiro.value - 1] = nivel[v-1] + 1
                    f.add(ponteiro.value)
                ponteiro = ponteiro.next
        else:
            while ponteiro:
                if marca[ponteiro.value[1] - 1] == 0:
                    marca[ponteiro.value[1] - 1] = 1
                    pai[ponteiro.value[1] - 1] = v
                    nivel[ponteiro.value[1] - 1] = nivel[v-1] + 1
                    f.add(ponteiro.value[1])
                ponteiro = ponteiro.next
    return marca, pai, nivel

def Dijkstra_lista(vertices,lista, inicial):
    heap = MinHeap()
    visitados = [0]*vertices
    dist = [float("inf")]*vertices
    anterior =[-1]*vertices
    dist[inicial-1] = 0
    heap.insercao((0, inicial))
    while heap.tamanho != 0:
        menor = heap.RemoveMinimo()
        visitados[menor[1] - 1] = 1
        ponteiro = lista[menor[1] - 1].head
        while ponteiro:
            if visitados[ponteiro.value[1] - 1] == 0:
                if dist[ponteiro.value[1] - 1] > dist[menor[1] - 1] + ponteiro.value[0]:
                    soma = dist[menor[1] - 1] + ponteiro.value[0]
                    dist[ponteiro.value[1] - 1] = soma
                    anterior[ponteiro.value[1] - 1] = menor[1]
                    heap.insercao((soma, ponteiro.value[1]))
            ponteiro = ponteiro.next
    return dist, anterior

def Bellman_ford_lista(vertice, grafo, inicial):
    dist = [float("inf")]*vertice
    ultimo = [-1]*vertice
    dist[inicial-1] = 0

    for a in range(vertice-1):
        alterou = False
        
        for i in range(vertice):
            ponteiro = grafo[i].head
            while ponteiro:
                vizinho = ponteiro.value[1]-1
                if dist[i] != float("inf") and dist[vizinho] > dist[i] + ponteiro.value[0]:
                    dist[vizinho] = dist[i] + ponteiro.value[0]
                    ultimo[vizinho] = i+1
                    alterou = True
                ponteiro = ponteiro.next
        if not alterou:
            break
    
    if alterou:
        for i in range(vertice):
            ponteiro = grafo[i].head
            while ponteiro:
                if dist[i] != float("inf") and dist[ponteiro.value[1]-1] > dist[i] + ponteiro.value[0]:
                    return 0
                ponteiro = ponteiro.next
    
    return dist, ultimo

def caminho(pais, final):
    caminho = []
    caminho.append(final)
    pai = pais[final-1]
    while pai != -1:
        caminho.append(pai)
        pai = pais[pai-1]
    return caminho[::-1]

def prim_lista(vertices,lista,inicial):
    heap = MinHeap()
    visitados = [0]*vertices
    peso = [float("inf")]*vertices
    anterior =[-1]*vertices
    peso[inicial-1] = 0
    heap.insercao((0, inicial))
    while heap.tamanho != 0:
        menor = heap.RemoveMinimo()
        visitados[menor[1] - 1] = 1
        ponteiro = lista[menor[1] - 1].head
        while ponteiro:
            if visitados[ponteiro.value[1] - 1] == 0:
                if peso[ponteiro.value[1] - 1] > ponteiro.value[0]:
                    peso[ponteiro.value[1] - 1] = ponteiro.value[0]
                    anterior[ponteiro.value[1] - 1] = menor[1]
                    heap.insercao((ponteiro.value[0], ponteiro.value[1]))
            ponteiro = ponteiro.next
    
    with open("MST.txt","w") as arquivo:
        arquivo.write("")
    with open("MST.txt","a") as arquivo:
        arquivo.write(f"{vertices}\n")
        for i in range(vertices):
            if anterior[i] != -1:
                arquivo.write(f"{i+1} {anterior[i]} {peso[i]}\n")
    arquivo.close()
    return sum(peso)

def distancia(grafo,vertices,origem,fim, ponderado, negativo):
    if not ponderado:
        d = BFS_list(grafo, vertices, origem, ponderado)[2][fim-1]
    if ponderado:
        if negativo:
            d = Bellman_ford_lista(vertices,grafo,origem)
            if d == 0:
                return "ciclo negativo"
            else:
                return d[0][fim-1]
        else:
            d = Dijkstra_lista(vertices,grafo,origem)[0][fim-1]
    return d

s = 1
d = int(input("O grafo é direcionado? Aperte 1 para sim e 0 para não "))
t = 0
arestas = 0
vetor = []
negativo = False
ponderado = False

with open("grafo.txt","r") as arquivo:
    aresta = arquivo.readlines()

if s == 1:
    for par in aresta:
        if t == 0:
            vertices = int(par)
            grau = np.zeros((vertices), dtype=np.uint16)
            for k in range(int(par)):
                vetor.append(linked_list())
            t+=1
        else:
            if len(par.split()) == 2:
                a,b = par.split()
                c,f = int(a), int(b)
                vetor[c-1].add_value(f)
                if d == 0:
                    vetor[f-1].add_value(c)
                    grau[f-1] += 1
                grau[c-1] += 1
                arestas += 1
            else:
                a,b,p = par.split()
                c,f,w = int(a), int(b),float(p)
                ponderado = True
                if not negativo and w < 0:
                    negativo = True
                vetor[c-1].add_value((w,f))
                if d == 0:
                    vetor[f-1].add_value((w,c))
                    grau[f-1] += 1
                grau[c-1] += 1
                arestas += 1
arquivo.close()