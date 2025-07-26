#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import time
import AStar

class Botarate(interface.Bot):
    """Bot que juega aleatoriamente."""
    NAME = "Botarate"
    m_onLigth = False
    m_numberOfMovementsFromRecalculate = 0

    #Callback recurrente.
    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""

        
        cx, cy = state["position"]
        
        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])
        
        #self.log(str(lighthouses))

        indexOfTargetLight = self.steps[self.stepIndex]
        dest = self.lighthouses[indexOfTargetLight]

        #Recalcular el camino teniendo en cuenta los faros que estan cogidos.
        
        if self.m_numberOfMovementsFromRecalculate >20:

            available = []
            for lh in self.lighthouses:
                if lighthouses[lh]["owner"] == None:
                    available.append(lh)
                    
            if len(lh)>4:
                self.recalculateRoute(available)
            self.m_numberOfMovementsFromRecalculate = 0
        else:
            self.m_numberOfMovementsFromRecalculate+=1
            

        #Estamos en un faro!!
        if (cx, cy) in self.lighthouses:
            if not self.m_onLight and cx == dest[0] and cy == dest[1]:
                self.log ("NEXTSTEP FARO")
                self.nextStep()
            self.m_onLight=True
            
            #Primero pasamos al siguiente paso en la triangulacion de delonay.
            if lighthouses[(cx, cy)]["owner"] == self.player_num:
                possible_connections = []
                for dest in self.lighthouses:
                    # No conectar con sigo mismo
                    # No conectar si no tenemos la clave
                    # No conectar si ya existe la conexión
                    # No conectar si no controlamos el destino
                    # Nota: no comprobamos si la conexión se cruza.
                    if (dest != (cx, cy) and
                        lighthouses[dest]["have_key"] and
                        [cx, cy] not in lighthouses[dest]["connections"] and
                        lighthouses[dest]["owner"] == self.player_num):
                        possible_connections.append(dest)                        
                        
                    if possible_connections and not self.m_error:
                        return self.connect(random.choice(possible_connections))
                    
            else:
                myenergy = state["energy"] + 1
                lightEnergy = lighthouses[(cx, cy)]["energy"]
                if  lighthouses[(cx, cy)]["owner"] == None:
                    self.log("ATTACK %d %d"  %  (lightEnergy, myenergy))
                    return self.attack(myenergy)
                elif lightEnergy < myenergy and (lightEnergy - myenergy) > 4:
                    self.log ("ENEMY ATTACK!! %d %d"  %  (lightEnergy, myenergy))
                    return self.attack(myenergy)


                #elif myenergy>lightEnergy:
                #    self.log ("ATTACK OTHER STUFF")
                #    return self.attack(myenergy)


        
        #Mover al siguiente sitio chachi ;)
        #Paranoid check!!
        if self.stepIndex < len(self.steps):
            indexOfNextLight = self.steps[self.stepIndex]
        else:
            indexOfNextLight = random.randint(0,len(self.steps))
        dest = self.lighthouses[indexOfNextLight]
        #self.log('MOVE TO')
        #self.log(str(dest))
        #self.log('Position')
        #self.log(str(state["position"]))


        #Use A_STAR to determine next movement!!
        astar = AStar.AStar(AStar.SQ_MapHandler(self.m_map4Path,self.m_mapw,self.m_maph))
        start = AStar.SQ_Location(cx,cy)
        end = AStar.SQ_Location(dest[0],dest[1])
        #s = time()
        p = astar.findPath(start,end)
        #e = time()
        move = [0,0]

        if p.nodes[0].location.x > cx:
            move[0] = 1;
        if p.nodes[0].location.x < cx:
            move[0] = -1;
            
        if p.nodes[0].location.y > cy:
            move[1] = 1;
        if p.nodes[0].location.y < cy:
            move[1] = -1;

        #self.log("MOVEMENT->")
        #self.log(str(move))
        self.m_onLight = False


        return self.move(*move)

if __name__ == "__main__":
    iface = interface.Interface(Botarate)
    iface.run()
