#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys, copy
import interface

class intheniteBot(interface.Bot):
	"""Bot que juega de pila master."""
	NAME = "inthenite"

        def FarosMios(self,faros):
                """Devuelvo el número de faros que son míos"""
                mios=0
                for dest in self.lighthouses:
                        if faros[(dest)]["owner"] == self.player_num:
                                mios=mios+1
                return mios

        def FarosAjenos(self,faros):
                """Devuelvo el número de faros que no son míos"""
                ajenos=0
                for dest in self.lighthouses:
                        if faros[(dest)]["owner"] != self.player_num and faros[(dest)]["owner"]>=0:
                                ajenos=ajenos+1
                return ajenos

        def FarosLibres(self,faros):
                """Devuelvo el número de faros que no son de nadie"""
                libres=0
                for dest in self.lighthouses:
                        if faros[(dest)]["owner"] is None :
                                libres=libres+1
                return libres

        def FarosTotal(self,faros):
                """Devuelvo el número total de faros"""
                return len(faros)

        def TengoTriangulos(self,faros,quien):
                """Devuelo cuantos triángulos tengo yo, o los demás, en principio los míos"""
                total=0
                for dest in self.lighthouses:
                        if faros[(dest)]["owner"]==quien and len(faros[(dest)]["connections"])>1:
                                self.log("Este faro tiene posibilidades "+str(faros[(dest)]))
                return total
        def PruebaTriangulo(self,listado,origen,faros):
                """Pruebo si puedo hacer un triangulo con la nueva conexión"""
                buenos=[]
                if len(listado)>0:
                        #self.log("Tengo Varias conexiones posibles :"+str(listado))
                        #self.log("conexiones: "+str(self.lighthouses))
                        #self.log("conexiones -> faros extend: "+str(faros))
                        for dest in listado:
                                #self.log("conexiones: Está "+str(origen)+" en "+str(faros[(dest)]["connections"]))
                                for redest in faros[(dest)]["connections"]:
                                        #self.log("conexiones con:"+str(redest)+" son:"+str(faros[(redest[0],redest[1])]["connections"]))
                                        if [origen[0],origen[1]] in faros[(redest[0],redest[1])]["connections"]:
                                                #self.log("conexiones: Posible triángulo! :"+str(origen)+"-"+str(dest)+"-"+str(faros[(dest)]["connections"]))
                                                buenos.append(dest)
                return buenos                                        

        def Interseccion(self,x1,y1,x2,y2,x3,y3,x4,y4):
                """Devuelvo si entre las dos líneas hay una intersección"""
                #self.log("INTENTO: ("+str(x1)+","+str(y1)+"-"+str(x2)+","+str(y2)+") - ("+str(x3)+","+str(y3)+"-"+str(x4)+","+str(y4)+")")
                #Si tiene el mismo origen, o mismo destino No hay
                if (x1,y1)==(x3,y3) or (x1,y1)==(x4,y4):
                        return False
                if (x2,y2)==(x3,y3) or (x2,y2)==(x4,y4):
                        return False

                d=(x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if int(d)==0:
                        return False  #No hay intersección

                pre = (x1*y2 - y1*x2)
                post = (x3*y4 - y3*x4)

                x = ( pre * (x3 - x4) - (x1 - x2) * post ) / d
                y = ( pre * (y3 - y4) - (y1 - y2) * post ) / d

                if ( x < min(x1, x2) or x > max(x1, x2) or x < min(x3, x4) or x > max(x3, x4) ):
                        return False #No hay intersección
                if ( y < min(y1, y2) or y > max(y1, y2) or y < min(y3, y4) or y > max(y3, y4) ):
                        return False  #No hay intersección

                #self.log("ACI: ("+str(x1)+","+str(y1)+"-"+str(x2)+","+str(y2)+") - ("+str(x3)+","+str(y3)+"-"+str(x4)+","+str(y4)+")")
                #Si hay intersección
                
                return True

        def AtraviesaConexiones(self,x1,y1,x2,y2,lighthouses):
                """Reviso si desde donde estamos y hasta el faro, atravesamos una conexión"""

                #self.log("AC0: "+str(lighthouses))
                for dest in lighthouses:
                        #self.log("AC: "+str(dest))
                        for conex in lighthouses[(dest)]["connections"]:
                                #self.log("Conexiones a comprobar: "+str(conex))
                                if self.Interseccion(x1,y1,x2,y2,dest[0],dest[1],conex[0],conex[1]):
                                        return True
                
                return False

        
        def orient2d(self,a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

        def Colinear(self, a, b, c):
            return self.orient2d(a, b, c) == 0

        def AtraviesaFaros(self,orig_x,orig_y,dest_x,dest_y):
                atravieso=False
                 
                x0, x1 = sorted((orig_x, dest_x))
                y0, y1 = sorted((orig_y, dest_y))
                origpos=(orig_x,orig_y)
                destpos=(dest_x,dest_y)
                for lh in self.lighthouses:
                        #self.log("Pruebo ¿Qué pruebo lh=?"+str(lh))
                        if (x0 <= lh[0] <= x1 and y0 <= lh[1] <= y1 and
                                lh not in (origpos, destpos) and
                                self.Colinear(origpos, destpos, lh)):
                                #self.log("Pruebo que el que atraviesa es:"+str(lh))
                                atravieso=True

                #self.log("Pruebo si atravieso un faro en esta conexión "+str(orig_x)+","+str(orig_y)+"-"+str(dest_x)+","+str(dest_y)+"="+str(atravieso))
                return atravieso
                

        def Distancia(self,estado,pos_x,pos_y,faropx,faropy):
                casillas_distancia=0
                mueve_x=0
                mueve_y=0
                seguir=True

                #Mapa a usar, es de unos y ceros. Uno es machacable, los ceros NO
                inundacion=copy.deepcopy(self.map)
            
                #Lista de inundación-inicio. Inundo con TRESES
                inunda_ini=[[pos_x,pos_y]]
                inunda_ini_sig=[]
                inundacion[pos_y][pos_x]=3

                #Lista de inundacion-destino. Inundo con CUATROS
                inunda_fin=[[faropx,faropy]]
                inunda_fin_sig=[]
                inundacion[faropy][faropx]=4
           
                while seguir:
                        #Inundación inicial
                        casillas_distancia=casillas_distancia+1
                        inunda_ini_sig=[]
                        #self.log("En la inundación inicial hay que procesar "+str(len(inunda_ini)))

                        for iterador in inunda_ini:
                                moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
                                #Movimientos válidos, ni mi posición, ni muro, ni ocupada por inundación inicio(3)
                                moves = [(x,y) for x,y in moves if (inundacion[y+iterador[1]][x+iterador[0]]!=0 and inundacion[y+iterador[1]][x+iterador[0]]!=3)]
                                for move in moves:
                                        #Inundo con 3, a no ser que encuentre un 4
                                        if inundacion[move[1]+iterador[1]][move[0]+iterador[0]]==4 and seguir:
                                                seguir=False
                                                mueve_x=move[0]+iterador[0]
                                                mueve_y=move[1]+iterador[1]
                                                break
                                        else:
                                                inundacion[move[1]+iterador[1]][move[0]+iterador[0]]=3
                                                inunda_ini_sig.append([move[0]+iterador[0],move[1]+iterador[1]])
                                                #self.log("Añado a ini :"+str(inunda_ini_sig))
                        #Ya he acabado la primera parte
                        inunda_ini=copy.deepcopy(inunda_ini_sig)
                        #self.log("Hemos sacado para la siguiente inundación de inicio "+str(len(inunda_ini)))                                        

                        #Inundación destino
                        if seguir:
                                casillas_distancia=casillas_distancia+1
                        inunda_fin_sig=[]
                        #self.log("En la inundación destino hay que procesar "+str(len(inunda_fin)))

                        for iterador in inunda_fin:
                                moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
                                #Movimientos válidos, ni mi posición, ni muro, ni ocupada por inundación destino(4)
                                moves = [(x,y) for x,y in moves if inundacion[y+iterador[1]][x+iterador[0]]!=0 and inundacion[y+iterador[1]][x+iterador[0]]!=4 ]
                                for move in moves:
                                        #Inundo con 4, a no ser que encuentre un 3
                                        if inundacion[move[1]+iterador[1]][move[0]+iterador[0]]==3 and seguir:
                                                seguir=False
                                                mueve_x=move[0]+iterador[0]
                                                mueve_y=move[1]+iterador[1]
                                                break
                                        else:
                                                inundacion[move[1]+iterador[1]][move[0]+iterador[0]]=4
                                                inunda_fin_sig.append([move[0]+iterador[0],move[1]+iterador[1]])
                                                #self.log("Añado a fin :"+str(inunda_fin_sig))
                        #Ya he acabado la segunda parte
                        inunda_fin=copy.deepcopy(inunda_fin_sig)
                        #self.log("Hemos sacado para la siguiente inundación de destino "+str(len(inunda_fin)))     

                #self.log("Distancia acabada con "+str(casillas_distancia)+" en "+str(mueve_x)+","+str(mueve_y))


                return(casillas_distancia,mueve_x,mueve_y)

        def IrFaro(self,estado,ocupado_por,a_cual_ir):
                """Voy a un faro mio/ajeno/libre que esté cerca/poco_energico"""
                #-1 libres #0 mios #1 de los otros
                mejor_x=0
                mejor_y=0

                faro_cercano=-1;
                casillas_mejor=0;
                energia_peor=0;

                pos_x,pos_y=estado["position"]
                
                #self.log("Voy a un faro de "+str(ocupado_por)+" que esté "+str(a_cual_ir))
                #self.log("Voy desde "+str(pos_x)+","+str(pos_y))

                faros = dict((tuple(lh["position"]), lh)
							for lh in estado["lighthouses"])
                
                #self.log("Cuantos faros hay???? más o menos: "+str(faros))
                for i in self.lighthouses:
                        #self.log("Procesando faro de "+str(i))
                        if (faros[(i)]["owner"] is None  and ocupado_por==-1) or (faros[(i)]["owner"]==self.player_num and ocupado_por==0) or (faros[(i)]["owner"] is not None and faros[(i)]["owner"]!=self.player_num and ocupado_por==1):
                                
                                if a_cual_ir=="cercano":
                                        faropx,faropy=faros[(i)]["position"]
                                        (casillas,mueve_x,mueve_y)=self.Distancia(estado,pos_x,pos_y,faropx,faropy)
                                        #self.log("Faro "+str(pos_x)+","+str(pos_y)+" a una distancia de: "+str(casillas))
                                        if casillas<=casillas_mejor or faro_cercano==-1:
                                                casillas_mejor=casillas
                                                mejor_x=mueve_x
                                                mejor_y=mueve_y
                                                faro_cercano=0
                                                #self.log("Me quedo con este faro")
                                                
                                else:   #Al menos energico----NO COMPROBADO-----
                                        #self.log("Procesando menos energico :"+str(i))
                                        if energia_peor>=faros[(i)]["energy"] or faro_cercano==-1:
                                                energia_peor=faros[(i)]["energy"]
                                                mejor_x,mejor_y=faros[(i)]["position"]
                                                casillas_mejor=3
                                                faro_cercano=0
                                                #self.log("Acepto nuevo menos enérgico con:"+str(energia_peor)+" en "+str(faros[(i)]["position"]))

                while casillas_mejor>2:
                        (casillas_mejor,mejor_x,mejor_y)=self.Distancia(estado,pos_x,pos_y,mejor_x,mejor_y)
                        
                #self.log("Ir a faro de: "+str(pos_x)+","+str(pos_y)+" a "+str(mejor_x)+","+str(mejor_y))

                return (mejor_x-pos_x,mejor_y-pos_y)     


        def RecolectarMaximo(self,estado,cx,cy,recursividad):
                """Función recursiva que me da la mejor posición a donde ir para recolectar más"""
                if recursividad==0:
                        return (0,0,0)

                mejor_valor=0
                rec_x=0
                rec_y=0

                moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
		# Determinar movimientos válidos, "en principio" no puedo pasar por los 0's, no es interesante
		moves = [(x,y) for x,y in moves if estado["view"][cy+y][cx+x]>=1 ]
		for dest in moves:
                        #self.log("Pruebo movimiento:"+str(dest[0])+","+str(dest[1])+" corr:"+str(dest[0]+cx)+","+str(dest[1]+cy)+" valor:"+str(estado["view"][cy+dest[1]][cx+dest[0]]))
                        (recmax,y,x)=self.RecolectarMaximo(estado,cx+dest[0],cy+dest[1],recursividad-1)
                        if mejor_valor<=recmax+estado["view"][cy+dest[1]][cx+dest[0]]:                             
                                mejor_valor=recmax+estado["view"][cy+dest[1]][cx+dest[0]]
                                rec_y=dest[1]
                                rec_x=dest[0]

                return (mejor_valor,rec_x,rec_y)


        
        def Recolectar(self,estado):
                """Devuelvo cual es la mejor posición a la que moverse para recolectar el máximo"""
                #Recursividad=3 Ya que es el máximo de casillas que se pueden ver
                #Mis posición es el centro de la matriz view
                cx=len(estado["view"][0])//2
                cy=cx 
                #self.log("El centro de la matriz es "+str(cx))
                (energia_recolectable,pos_x,pos_y)=self.RecolectarMaximo(estado,cx,cy,3) #A 2 va peor
                #self.log("Me sale que el máximo es "+str(energia_recolectable))

                #Cuidado amiguitos, si sale que el máximo es 0, estoy LEJOS de un faro!!!, hay que ir a uno
                if energia_recolectable==0:
                        return self.IrFaro(estado,-1,"cercano")

                return (pos_x,pos_y)

           

	def play(self, state):
		"""Jugar: llamado cada turno.
		Debe devolver una acción (jugada)."""
		cx, cy = state["position"]
		lighthouses = dict((tuple(lh["position"]), lh)
							for lh in state["lighthouses"])
                mi_energia= state["energy"]

                #Me guardo mi estado anterior y actualizo los faros
                estado_anterior=self.estado
                faros_mios=self.FarosMios(lighthouses)
                faros_ajenos=self.FarosAjenos(lighthouses)
                faros_libres=self.FarosLibres(lighthouses)
                faros_total=self.FarosTotal(lighthouses)
                #tentri=self.TengoTriangulos(lighthouses,self.player_num)

                

                #Revisión del estado anterior para ver si se puede cambiar
		if estado_anterior=="recolectar_energia_inicial":
                        #Si mis faros son 0 y sus faros son 0 y no tengo energia
                        if faros_mios==0 and faros_ajenos==0 and mi_energia<=self.energ_min_faro_vacio:
                                #Necesito seguir buscando energia
                                self.estado="recolectar_energia_inicial"
                        else:
                                #self.log("Debo de cambiar de estado")
                                if faros_ajenos>=1:
                                        self.estado="atacar_faro"
                                        self.a_cual_ir="menos_energico"
                                        #self.log("Voy a atacar el faro menos enérgico")
                                elif mi_energia>=self.energ_min_faro_vacio:
                                        self.estado="ir_a_faro_libre"
                                        self.a_cual_ir="cercano"
                                        #self.log("Voy a buscar un faro libre cercano")
                elif estado_anterior=="ir_a_faro_libre":
                        #Mientras no haya llegado, o se acaben los faros libres
                        if (cx,cy) in lighthouses: 
                                self.estado="estoy_en_faro"
                                #self.log("He llegado a un faro y actuo")
                        elif faros_libres==0:
                                if faros_mios==0:
                                        self.estado="atacar_faro"
                                        self.a_cual_ir="cercano"
                                        #self.log("Se han acabado los faros, y no tengo, a atacar - modo lokis")
                                elif faros_mios>=faros_ajenos:
                                        self.estado="recargar_faro"
                                        self.a_cual_ir="menos_energico"
                                        #self.log("Se han acabado los faros, y recargo los míos")
                                elif faros_ajenos>faros_mios:
                                        self.estado="atacar_faro"
                                        self.a_cual_ir="menos_energico"
                                        #self.log("Se han acabado los faros, y ataco los suyos, que tiene más")
                elif estado_anterior=="estoy_en_faro":
                        #¿Me he salido?
                        if (cx,cy) in lighthouses:
                                #Sigo haciendo cosas en el faro
                                pass
                        else:
                                #he salido,no sigo en el faro
                                self.estado="recolectar_energia"
                elif estado_anterior=="recolectar_energia":
                        if state["energy"]>=self.energ_min_recarga:
                                if faros_mios<=faros_ajenos:
                                        if faros_libres>faros_ajenos:
                                                self.estado="ir_a_faro_libre"
                                                self.a_cual_ir="cercano"
                                        else:
                                                self.estado="atacar_faro"
                                                self.a_cual_ir="menos_energico" #antes cercano
                                else: #Tengo más faros :-)
                                        #Parametrización en función del número de faros
                                        if (faros_mios<4 and faros_total>4) or (faros_mios<3 and faros_total<=4): #Con 3 va bien y con 4 va mal si hay 4 faros
                                                if faros_libres>faros_ajenos:
                                                        self.estado="ir_a_faro_libre"
                                                        self.a_cual_ir="cercano"
                                                else:
                                                        self.estado="atacar_faro"
                                                        self.a_cual_ir="menos_energico"
                                        else:
                                                #Tengo 3 o más faros
                                                if faros_libres>faros_ajenos:
                                                        self.estado="recargar_faro"
                                                        self.a_cual_ir="menos_energico"
                                                else:
                                                        self.estado="atacar_faro"
                                                        self.a_cual_ir="menos_energico"
                elif estado_anterior=="recargar_faro":
                        if (cx,cy) in lighthouses:
                                #Ya he llegado al faro
                                self.estado="estoy_en_faro"
                        if faros_mios==0:
                                #Ya no tengo faros que recargar
                                if faros_libres>=faros_ajenos:
                                        self.estado="ir_a_faro_libre"
                                        self.a_cual_ir="cercano"
                                else:
                                        self.estado="atacar_faro"
                                        self.estado="cercano"
                        else:   #Sigo en el proceso de recarga
                                if state["energy"]<=self.energ_min_recarga:
                                        self.estado="recolectar_energia"
                elif estado_anterior=="atacar_faro":
                        if (cx,cy) in lighthouses:
                                self.estado="estoy_en_faro"
                        elif faros_ajenos==0:
                                self.estado="recolectar_energia"
                                
                else:
                        self.log("noooooo nooooo noooo")
                
                                
                #self.log("Estado anterior :"+estado_anterior+ " actual :"+self.estado)

                #Actuar en consecuencia del estado que se ha decidido
                if self.estado=="recolectar_energia_inicial":
                        move=self.Recolectar(state)
                        return self.move(*move)
                elif self.estado=="recolectar_energia":
                        move=self.Recolectar(state)
                        return self.move(*move)
                elif self.estado=="atacar_faro":
                        move=self.IrFaro(state,1,self.a_cual_ir)
                        return self.move(*move)
                elif self.estado=="ir_a_faro_libre":
                        move=self.IrFaro(state,-1,self.a_cual_ir)
                        return self.move(*move)
                elif self.estado=="recargar_faro":
                        move=self.IrFaro(state,0,self.a_cual_ir)
                        return self.move(*move)
                elif self.estado=="estoy_en_faro":
                        #self.log("Dueño del faro:"+str(lighthouses[(cx,cy)]["owner"]))
                        if lighthouses[(cx,cy)]["owner"]==self.player_num:
                                #El faro es mío, si tengo energía lo recargo, si tengo clave lo conecto
                                if state["energy"]>=self.energ_min_recarga:
                                        #energy=int(state["energy"]*self.porcentaje_recarga)
                                        energy=state["energy"]
                                        return self.attack(energy)
                                else:
                                        #Compruebo si hay conexiones posibles
                                        possible_connections = []
                                        for dest in self.lighthouses:
                                                # No conectar con sigo mismo - ok
                                                # No conectar si no tenemos la clave - ok
                                                # No conectar si ya existe la conexión - ok
                                                # No conectar si no controlamos el destino - ok
                                                # Nota: no comprobamos si la conexión se cruza.
                                                if (dest != (cx, cy) and
                                                    lighthouses[dest]["have_key"] and
                                                    [cx, cy] not in lighthouses[dest]["connections"] and
                                                    lighthouses[dest]["owner"] == self.player_num):
                                                    #Comprobar si la conexión se cruza
                                                        if not self.AtraviesaConexiones(cx,cy,dest[0],dest[1],lighthouses):
                                                                if not self.AtraviesaFaros(cx,cy,dest[0],dest[1]):
                                                                        possible_connections.append(dest)

                                        if possible_connections:
                                                if len(possible_connections)>1:
                                                        #self.log("Para elegir entre "+str(len(possible_connections))+ " conexiones")
                                                        buenos=self.PruebaTriangulo(possible_connections,(cx,cy),lighthouses)
                                                        if len(buenos)>=1:
                                                                #self.log("conexiones: marchando una de triangulos")
                                                                conecto=random.choice(buenos)
                                                        else:
                                                                #self.log("conexiones: no han salido posibles triangulos")
                                                                conecto=random.choice(possible_connections)
                                                else:
                                                        #self.log("conexiones: oh, no se comprueba si hay")
                                                        conecto=random.choice(possible_connections)
                                                #self.log("Conecto "+str(conecto))
                                                return self.connect(conecto)
                                        #Si llego aquí no he conectado, así que salgo
                                        move=self.Recolectar(state)
                                        #self.log("Salgo del faro aleatoriamente")
                                        return self.move(*move)
                        elif lighthouses[(cx,cy)]["owner"] is None:
                                #Llego a un faro libre
                                #Le meto todo?
                                if state["energy"]>self.energ_min_faro_vacio:
                                        return self.attack(state["energy"])
                                else:
                                        move=self.Recolectar(state)
                                        return self.move(*move)
                        else:
                                #Llego a un faro ajeno
                                #self.log("Estoy en faro ajeno con +"+str(state["energy"]))
                                if state["energy"]>self.energ_min_ataque:
                                        #Full attack - modo lokis
                                        #self.log("Ataco al faro ajeno con ")
                                        return self.attack(state["energy"])
                                else:
                                        #No tengo energía y me piro
                                        move=self.Recolectar(state)
                                        #self.log("Ojimeter que no ataco y me voy a :"+str(move))
                                        return self.move(*move)
                        #Si llego aquí no he conectado, así que salgo
                        move=self.Recolectar(state)
                        return self.move(*move)
                #elif self.estado==:
                else:
                        self.log("ojooooooo que no procesamos nada")
                                
                        
                        

                #Aquí no debería de llegar para mover aleatoriamente       
		# Mover aleatoriamente
		self.log("Soy un chungo en el estado "+self.estado)
		moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
		# Determinar movimientos válidos
		moves = [(x,y) for x,y in moves if self.map[cy+y][cx+x]]
		move = random.choice(moves)
		return self.move(*move)



if __name__ == "__main__":
	iface = interface.Interface(intheniteBot)
	iface.run()
