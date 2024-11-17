from kalah import *
from utils import *
from jogos import *

def linearPond(estado,jogador,pesos,funcoes,win):
    """Função que pega no estado e no jogador e se fim do jogo devolve win*utilidade (* 1 ou -1, dependendo do jogador)
    senão devolve a combinação linear de pesos e features."""
    if estado.is_game_over():
        aux = estado.result()
        return aux*win if jogador == 0 else aux*-win
    return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])

## Funções de peso
def func_38(estado, jogador):

    def func_win_38(estado, jogador):
        valorVitoria = 10000
        #Verificar se ganhamos 
        if (estado.state[estado.SOUTH_SCORE_PIT] > 24 and jogador == 0) or (estado.state[estado.NORTH_SCORE_PIT] > 24 and jogador == 1):
            return valorVitoria
        elif (estado.state[estado.SOUTH_SCORE_PIT] > 24 and jogador == 1) or (estado.state[estado.NORTH_SCORE_PIT] > 24 and jogador == 0):
            return -valorVitoria
        
        return 0

    def func_play_again_38(estado, jogador):
        playAgain = 15
        setUpPA = 20
        notPerfectSetup = 10
        ret = 0

        ##Ver se pode jogar outraves
        if estado.pass_turn and estado.to_move != jogador:
            ret += playAgain
        
        ##Ver se podemos jogar novamente no futuro
        if jogador == 0:
            for i in range(6):
                if(estado.state[i]%13 == 6-i): #verificar se pode jogar outra vez
                    for j in range(7,13):
                        if((j+estado.state[j])-14 >= i):
                            ret -= notPerfectSetup
                    ret += setUpPA
        else:
            for i in range(6):
                if(estado.state[i+7]%13 == 6-i): #verificar se pode jogar outra vez
                    for j in range(6):
                        if((j+estado.state[j])-14 >= i+7):
                            ret -= notPerfectSetup
                    ret += setUpPA

        return ret

    def func_steal_38(estado, jogador):
        addNrPecasRoubadasAgr = 50
        multNrPecasRoubadas = 5
        valorNossoCampo = 15
        ret = 0

        #Ver se pode roubar peças no futuro
        if jogador == 0:
            for i in range(6):
                pit = estado.NORTH_SCORE_PIT - (i+estado.state[i])%13 - 1
                #Ver se rouba peças com esta jogada
                if estado.state[i] == 0 and estado.state[12-i] == 0 and estado.state[6] > 1:
                    aux = 0
                    for j in range(6):
                        if i != j and estado.state[j] == 0:
                            aux = 1
                    ret += addNrPecasRoubadasAgr*aux
                #Dar setup para roubar
                if estado.state[i] > 0 and (i+estado.state[i])%13 < 6:
                    ret += valorNossoCampo
                    if estado.state[(i+estado.state[i])%13] == 0 or i+estado.state[i] == 13:
                        aux = 6
                        for j in range (7,13):
                            if (j+estado.state[j])-14 >= i or (j+estado.state[j])-14 >= (i+estado.state[i])%13:#tapar buracos
                                aux -= 1
                        ret += (estado.state[pit] + 1)*multNrPecasRoubadas*aux #nrPeças*mult*(6-opções para tapar)
            for i in range(7,13):
                pit = estado.NORTH_SCORE_PIT - (i+estado.state[i])%13 - 1
                #Ver se rouba peças com esta jogada
                if estado.state[i] == 0 and estado.state[12-i] == 0 and estado.state[13] > 1:
                    aux = 0
                    for j in range(7,13):
                        if i != j and estado.state[j] == 0:
                            aux = 1
                    ret -= addNrPecasRoubadasAgr*aux
                #Dar setup para roubar
                if estado.state[i] > 0 and 6 < (i+estado.state[i])%13 < 13:
                    ret -= valorNossoCampo
                    if estado.state[(i+estado.state[i])%13] == 0 or i+estado.state[i] == 13:
                        ret -= (estado.state[pit] + 1)*100
        else:
            for i in range(7,13):
                pit = estado.NORTH_SCORE_PIT - (i+estado.state[i])%13 - 1
                if estado.state[i] == 0 and estado.state[12-i] == 0 and estado.state[13] > 1:
                    aux = 0
                    for j in range(7,13):
                        if i != j and estado.state[j] == 0:
                            aux = 1
                    ret += addNrPecasRoubadasAgr*aux
                if estado.state[i] > 0 and 6 < (i+estado.state[i])%13 < 13:
                    ret += valorNossoCampo
                    if estado.state[(i+estado.state[i])%13] == 0 or i+estado.state[i] == 13:
                        aux = 6
                        for j in range (7,13):
                            if (j+estado.state[j])-14 >= i or (j+estado.state[j])-14 >= (i+estado.state[i])%13:#tapar buracos
                                aux -= 1
                        ret += (estado.state[pit] + 1)*multNrPecasRoubadas*aux #nrPeças*mult*(6-opções para tapar)
            for i in range(6): 
                pit = estado.NORTH_SCORE_PIT - (i+estado.state[i])%13 - 1
                if estado.state[i] == 0 and estado.state[12-i] == 0 and estado.state[13] > 1:
                    aux = 0
                    for j in range(7,13):
                        if i != j and estado.state[j] == 0:
                            aux = 1
                    ret -= addNrPecasRoubadasAgr*aux
                if estado.state[i] > 0 and (i+estado.state[i])%13 < 6:
                    ret -= valorNossoCampo
                    if estado.state[(i+estado.state[i])%13] == 0 or i+estado.state[i] == 13:
                        ret -= (estado.state[pit] + 1)*100 
        return ret            

    def func_basica_38(estado, jogador):
        multMaisPecas = 10
        ret = 0

        #Ver se temos mais peças que o inimigo no nosso kalah
        aux = -1
        if jogador == 0:
            aux = 1
        ret += (estado.state[estado.SOUTH_SCORE_PIT] - estado.state[estado.NORTH_SCORE_PIT])*aux*multMaisPecas
        
        return ret

    def func_longe_melhor_38(estado, jogador):
        #peças longe do nosso Kalah valem mais
        multPecas = 4

        ret = 0
        aux = 1

        if jogador == 0:
            for i in range(6):
                ret += estado.state[i]*aux*multPecas
                ret -= estado.state[7+i]*aux*multPecas
                aux -= 0.1
        else:
            for i in range(7,13):
                ret += estado.state[i]*aux*multPecas
                ret -= estado.state[i-7]*aux*multPecas
                aux -= 0.1

        return ret
        

    def func_stall_38(estado, jogador):
        #Caso tenhamos muitas peças e o inimigo poucas, tentar fazer com que ele acabe as peças (dar stall)
        ret = 0
        beans = 0
        op = 0
        pitsop = 0
        if jogador == estado.SOUTH:
            for i in range(7):
                beans += estado.state[i]
                if estado.state[7+i] > 0:
                    op += estado.state[7+i]
                    pitsop += 1
            op -= estado.state[13]
        else:
            for i in range(7,14):
                beans += estado.state[i]
                if estado.state[i-7] > 0:
                    op += estado.state[i-7]
                    pitsop += 1
            op -= estado.state[6]

        if beans >= 25 and ((op < 12 and pitsop < 3) or op < 3):
            ret += 50/op
                
        return ret
    

    values = [0.282, 0.059, 0.006, 0.298, 0.098, 0.257]
    funcs = [func_win_38,func_play_again_38,func_steal_38,func_basica_38,func_longe_melhor_38,func_stall_38]

    return linearPond(estado, jogador, values, funcs, 10000)

