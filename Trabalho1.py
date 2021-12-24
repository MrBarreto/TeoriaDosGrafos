import numpy as np
from time import time
from math import log2

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

def DFS_list(lista, vertices, elemento):
    pilha = [elemento]
    pai = [-1 for i in range(vertices)]
    nivel = [-1 for i in range(vertices)]
    marca = [0 for i in range(vertices)]
    pai[elemento-1],nivel[elemento-1] = None, 0
    while pilha:
        v = pilha.pop()
        if marca[v-1] == 0:
            marca[v-1] = 1
            ponteiro = lista[v-1].head
            while ponteiro:
                pilha.append(ponteiro.value)
                if nivel[ponteiro.value - 1] == -1:
                    nivel[ponteiro.value - 1] = nivel[v-1] + 1
                    pai[ponteiro.value - 1] = v
                ponteiro = ponteiro.next
    return pai,nivel

def DFS_matriz(matriz, vertices, elemento):
    pilha = [elemento]
    pai = [-1 for i in range(vertices)]
    nivel = [-1 for i in range(vertices)]
    marca = [0 for i in range(vertices)]
    pai[elemento-1],nivel[elemento-1] = None, 0
    while pilha:
        v = pilha.pop()
        if marca[v-1] == 0:
            marca[v-1] = 1
            for i in range(vertices):
                if matriz[v-1][i] == 1:
                    pilha.append(i+1)
                    if nivel[i] == -1:
                        nivel[i] = nivel[v-1] + 1
                        pai[i] = v
    return pai,nivel
                           
def BFS_list(lista, vertices,elemento):
    pai, nivel, marca = [-1 for i in range(vertices)], [-1 for i in range(vertices)],  [0 for i in range(vertices)]
    f = queue()
    pai[elemento-1], nivel[elemento-1] = None, 0
    marca[elemento -1] = 1
    f.add(elemento)
    while f.len != 0:
        v = f.remove()
        ponteiro = lista[v-1].head
        while ponteiro:
            if marca[ponteiro.value - 1] == 0:
                marca[ponteiro.value - 1] = 1
                pai[ponteiro.value - 1] = v
                nivel[ponteiro.value - 1] = nivel[v-1] + 1
                f.add(ponteiro.value)
            ponteiro = ponteiro.next
    return marca, pai, nivel

def BFS_matriz(matriz, vertices,elemento):
    pai, nivel, marca = [-1 for i in range(vertices)], [-1 for i in range(vertices)],  [0 for i in range(vertices)]
    f = queue()
    pai[elemento-1], nivel[elemento-1] = None, 0
    marca[elemento -1] = 1
    f.add(elemento)
    while f.len != 0:
        v = f.remove()
        for i in range(vertices):
            if matriz[v-1][i] == 1:
                if marca[i] == 0:
                    marca[i] = 1
                    f.add(i+1)
                    pai[i] = v
                    nivel[i] = nivel[v-1] + 1
    return marca, pai, nivel

def Conexas(s, grafo, vertices):
    inicial = []
    desmarcados = []
    componentes = []
    
    if s == 0:
        c = BFS_matriz(grafo, vertices, 1)[0]
    else:
        c = BFS_list(grafo, vertices, 1)[0]
    for i in range(vertices):
        if c[i] == 0:
            desmarcados.append(i+1)
        else:
            inicial.append(i+1)
    componentes.append(inicial)
    if desmarcados == []:
        return "Grafo conexo"
    
    while len(desmarcados) != 0:
        inicial = []
        if s == 0:
            c = BFS_matriz(grafo, vertices, desmarcados[0])[0]
        else:
            c = BFS_list(grafo, vertices, desmarcados[0])[0]
        retirar = []
        count = 0
        for i in desmarcados:
            if c[i-1] == 1:
                inicial.append(i)
                retirar.append(count)
            count += 1
        for i in retirar:
            desmarcados.pop(i)
        componentes.append(inicial)
    
    componentes.sort(key=len, reverse= True)
    return componentes

def diametro(s, grafo, vertices):
    maior = -1
    for i in range(vertices):
        if s == 0:
            d = BFS_matriz(grafo, vertices, i)[2]
        else:
            d = BFS_list(grafo, vertices, i)[2]
        for i in range(vertices):
            if d[i] > maior:
                maior = d[i]
    return maior
  
def distancia(i,grafo,vertices,origem,fim):
    if i == 0:
        d = BFS_matriz(grafo,vertices,origem)[2][fim-1]
    else:
        d = BFS_list(grafo, vertices, origem)[2][fim-1]
    return d

def dia_aprox(s, grafo, vertices):
    vt = vertices
    itera = int(log2(vertices))
    dist = -1
    ini = 0
    for i in range(itera):
        a = distancia(s,grafo,vt,ini,vertices)
        if a > dist:
            dist = a
        ini += 1
        vertices -= 1
    return dist


s = int(input("Qual será o método de representação, aperte 0 para matriz e 1 para lista: "))
t = 0
arestas = 0
matriz = []
vetor = []


with open("grafo_XX.txt","r") as arquivo:
    aresta = arquivo.readlines()

if s == 0:
    for par in aresta:
        if t == 0:
            vertices = int(par)
            grau = [0 for x in range(vertices)]
            matriz = np.zeros((vertices,vertices), dtype=np.byte)
            t+=1
        else:
            a,b = par.split()
            c,f = int(a), int(b)
            matriz[c-1][f-1] = 1
            matriz[f-1][c-1] = 1
            grau[c-1] += 1
            grau[f-1] += 1
            arestas +=1 

elif s == 1:
    for par in aresta:
        if t == 0:
            vertices = int(par)
            grau = np.zeros((vertices), dtype=np.uint16)
            for k in range(int(par)):
                vetor.append(linked_list())
            t+=1
        else:
            a,b = par.split()
            c,f = int(a), int(b)
            vetor[c-1].add_value(f)
            vetor[f-1].add_value(c)
            grau[c-1] += 1
            grau[f-1] += 1
            arestas += 1
arquivo.close()

grau.sort()
media = sum(grau)/vertices
mediana = grau[int(vertices/2)]
maior = grau[-1]
menor = grau[0]

if s == 1:
    cone = Conexas(s,vetor,vertices)
else:
    cone = Conexas(s,matriz,vertices)

with open("resultado.txt","w") as arquivo:
    arquivo.write("")
with open("resultado.txt","a") as arquivo:
    arquivo.write(f"Vertices = {vertices}\n")
    arquivo.write(f"Grau medio = {media}\n")
    arquivo.write(f"Mediana de grau = {mediana}\n")
    arquivo.write(f"Maior grau = {maior}\n")
    arquivo.write(f"Menor grau = {menor}\n")
    if type(cone) is list:
        arquivo.write(f"Componentes: {len(cone)} \n")
        for co in cone:
            arquivo.write(f"Tamanho: {len(co)}, vertices: {co}\n")
    else:
        arquivo.write(f"Grafo conexo")
