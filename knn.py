class ClassificaPelosVizinhosMaisProximos:
    def __init__(self):
        self.rotulados = []
        self.registros_preditos = {}
        
    def fit(self,matriz_rotulada):
        ''' Guarda os dados já rotulados no atributo "rotulados" do objeto criado. 
        Cada chamada desse método adiciona mais registros ao atributo "rotulados". 
        A entrada desse método deve ser uma lista de listas, cada elemento da lista é um registro rotulado.
        Os registros devem ser no formato: [Identificacao, Categoria, (Coordenadas do ponto)].'''
        for registro in matriz_rotulada:
            self.rotulados.append([registro[1], registro[2]])
        
    def predict(self, k, matriz_nao_rotulada):
        ''' Rotula registros não rotulados utilizando a técnica KNN a partir dos pontos armazenados no atributo "rotulados".
            Guarda a predição dos rotulos no atributo dicionário "registros_preditos" onde a chave é a Identificação e o valor é o rótulo predito.
            A primeira entrada é a quantidade de vizinhos que será usada para rotular o registro.
            A segunda entrada desse método deve ser uma lista de listas, cada elemento da lista é um registro não rotulado.
            Os registros devem ser no formato: [Identificação, '', (Coordenadas do ponto)].'''
        try:
            for sem_rotulo in matriz_nao_rotulada:
                self.registros_preditos[sem_rotulo[0]] = self.__rotulaPonto(k, sem_rotulo[2])
        except IndexError:
            print('Antes de continuar é necessário incluir os dados já rotulados, utilize o método fit()')

    def __rotulaPonto(self, k, ponto_interesse):
        ''' Prevê o rótulo de um pontos'''
        distancias = []
        for ponto_rotulado in self.rotulados:
            distancias.append([ponto_rotulado[0], self.__distancia(
                ponto_interesse, ponto_rotulado[1])])
        distancias_ord = sorted(distancias, key=lambda classe: classe[1])[:k]
        categorias = []

        for i in range(k):
            categorias.append(distancias_ord[i][0])
        return self.__defineRotulo(categorias)

    def __distancia(self, coordenadas1, coordenadas2):
        ''' Calcula a distancia entre 2 pontos de n dimensões.'''
        if len(coordenadas1) == len(coordenadas2):
            somatorio = 0
            for i in range(len(coordenadas1)):
                somatorio = somatorio + (coordenadas1[i] - coordenadas2[i])**2
            return somatorio**(1 / 2)
        else:
            return print('Dimensões diferentes')

    def __defineRotulo(self, lista):
        ''' Conta a quantidade de cada rótulo da lista e retorna o rótulo com a maior quantidade.
        Se houver empate retorna uma lista com os rótulos empatados'''
        dicionario = {}
        maior = 0
        classes = []

        for elemento in lista:
            if dicionario.get(elemento) == None:
                dicionario[elemento] = 1
            else:
                dicionario[elemento] += 1

            if dicionario[elemento] > maior:
                maior = dicionario[elemento]

        for chave, valor in dicionario.items():
            if valor == maior:
                classes.append(chave)

        if len(classes) == 1:
            return classes[0]
        elif len(classes) > 1:
            return classes
        
    def __repr__(self):
        if self.registros_preditos != {}:
            representacao = '    CPF         PERFIL\n'
            for chave, valor in self.registros_preditos.items():
                representacao += f'{chave}   {valor}\n'
        else:
            representacao = 'Esse objeto não possui nenhum rótulo predito ainda, utilize o método predict()'
        return representacao