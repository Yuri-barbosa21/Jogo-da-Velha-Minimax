import copy
import numpy as np
from random import randint

class Jogo:
    def __init__(self):
        self.jogador1 = 'X'
        self.minimax = 'O'
        self.tabuleiro =  [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.jogos = [[' ', ' ', ''], [' ', ' ', ' '], [' ', ' ', ' ']]       
    
    def imprimir_jogos(self):
        for jogo in self.jogos:
            jogo_array = np.array(jogo)
            print(jogo_array)
            print() # adiciona uma linha em branco após cada jogo

    def validar_jogada(self, linha, coluna):
        if linha < 0 or linha > 2 or coluna < 0 and coluna > 2:
            return False

        if self.tabuleiro[linha][coluna]  == 'X' or self.tabuleiro[linha][coluna]  == 'O':
            return False
        return True

    def jogada_minimax(self):
        melhor_pontuacao = float('-inf')
        melhor_jogada = None
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == " ":
                    novo_estado = copy.deepcopy(self.tabuleiro)
                    novo_estado[i][j] = 'O'
                    pontuacao = self.fminimax(novo_estado, True)
                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (i, j)
        self.jogar(melhor_jogada[0], melhor_jogada[1], 'O')

    def jogar(self, linha, coluna, peca):
        if self.validar_jogada(linha, coluna):
            self.tabuleiro[linha][coluna] = peca;

            self.tabuleiro_copy = copy.deepcopy(self.tabuleiro)
            self.jogos.append(self.tabuleiro_copy)

            return True
        else: 
            print('Jogada Invalida')
            return False

    def verificar_ganhador(self, peca, estado):
        # Verifica Linhas
        for i in range(3):
            ganhou = 0
            for j in range(3):
                if estado[j][i] == peca:
                    ganhou += 1
                    if ganhou == 3:
                        return ganhou

        # Verifica Colunas
        for i in range(3):
            ganhou = 0
            for j in range(3):
                if estado[i][j] == peca:
                    ganhou += 1
                    if ganhou == 3:
                        return ganhou

        # Verifica Diagonal principal
        ganhou = 0
        for i in range(3):
            if estado[i][i] == peca:
                ganhou += 1
                if ganhou == 3:
                    return True
            else: ganhou = 0

        # Verifica Diagonal secundária
        ganhou = 0
        for i in range(2, -1, -1):
            j = 2 - i
            if estado[i][j] == peca:
                ganhou += 1
                if ganhou == 3:
                    return True
            else:
                ganhou = 0

    def verificar_empate(self, estado):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == ' ':
                    return False # ainda existem posições vazias
        return True # não há mais posições vazias, portanto ocorreu um empate

    def verificar_estado_terminal(self, estado):
        if self.calcular_utilidade(estado):
            return self.calcular_utilidade(estado)
        return -2

    def calcular_utilidade(self, estado):
        if self.verificar_ganhador('X', estado):
            return -1
        if self.verificar_ganhador('O', estado):
            return 1
        if self.verificar_empate(estado):
            return 0    

    def fminimax(self, estado, mini_jogador):
        if self.verificar_estado_terminal(estado) != -2:
            return self.verificar_estado_terminal(estado)

        if mini_jogador:
            melhor_pontuacao = float('inf')
            for i in range(3):
                for j in range(3):
                    if estado[j][i] == ' ':
                        estado[j][i] = 'X'
                        pontuacao = self.fminimax(estado, False)
                        estado[j][i] = ' '
                        melhor_pontuacao = min(melhor_pontuacao, pontuacao)
            return melhor_pontuacao
        else:
            melhor_pontuacao = float('-inf')
            for i in range(3):
                for j in range(3):
                    if estado[j][i] == ' ':
                        estado[j][i] = 'O'
                        pontuacao = self.fminimax(estado, True)
                        estado[j][i] = ' '
                        melhor_pontuacao = max(melhor_pontuacao, pontuacao)
            return melhor_pontuacao

    def imprimir_tabuleiro(self):
        print("   0   1   2 ")
        print("  +---+---+---+")
        for i in range(3):
            row = str(i) + " "
            for j in range(3):
                if self.tabuleiro[i][j] == '':
                    row += '| - '
                else:
                    row += '| ' + self.tabuleiro[i][j] + ' '
            row += '|'
            print(row)
            print("  +---+---+---+")
        print()

    def iniciar_jogo(self):
        self.jogador_atual = self.jogador1
        self.imprimir_tabuleiro()
        jogo_ativo = True

        self.jogador_atual = randint(0, 2)
        if self.jogador_atual == 1:
            self.jogador_atual = self.jogador1
        else:
            self.jogador_atual = self.minimax

        self.jogador_atual = self.minimax
        
        empatou = False
        ganhou = False

        self.imprimir_tabuleiro()

        while jogo_ativo:
            #print(self.verificar_estado_terminal(self.tabuleiro))

            if self.jogador_atual == self.jogador1:
                print('Jogador 1')
                linha = int(input('Linha: '))
                coluna = int(input('Coluna: '))

                if self.jogar(linha, coluna, 'X'):
                    #print (self.calcular_utilidade(self.tabuleiro))
                    if self.verificar_ganhador('X', self.tabuleiro):
                        ganhou = True
                        jogo_ativo = False
                    if self.verificar_empate(self.tabuleiro):
                        empatou = True
                        jogo_ativo = False
                
                self.jogador_atual = self.minimax
            else:
                print("Computador está pensando...")
                self.jogada_minimax()
                #self.imprimir_tabuleiro()
                if self.verificar_ganhador(self.minimax, self.tabuleiro):
                    ganhou = True
                    jogo_ativo = False
                elif self.verificar_empate(self.tabuleiro):
                    empatou = True
                    jogo_ativo = False
                else:
                    self.jogador_atual = self.jogador1
            
                
            self.imprimir_tabuleiro()

        #self.imprimir_jogos()
                        
        if empatou:
            print('EMPATOU')
        if ganhou:
            if self.jogador_atual == self.jogador1:
                print('Jogador 1 Ganhou')
            else:
                print('Minimax Ganhou')

        #print(self.verificar_estado_terminal(self.tabuleiro))

if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar_jogo()
