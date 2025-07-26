#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, json
import numpy as np
from scipy.spatial import Delaunay


# ==============================================================================
# ROBOT
# Los robots definidos deben heredar de esta clase.
# ==============================================================================

class Bot(object):
    """Bot base. Este bot no hace nada (pasa todos los turnos)."""
    NAME = "Botijo"
    m_error = False
    m_map4Path = []
    m_mapw = 0
    m_maph = 0
    # ==========================================================================
    # Comportamiento del bot
    # Métodos a implementar / sobreescribir (opcionalmente)
    # ==========================================================================

    def __init__(self, init_state):
        """Inicializar el bot: llamado al comienzo del juego."""
        self.player_num = init_state["player_num"]
        self.player_count = init_state["player_count"]
        self.init_pos = init_state["position"]
        self.map = init_state["map"]

        for line in self.map:
            for number in line:
                if int(number) == 0:
                    self.m_map4Path.append(-1)
                else:
                    self.m_map4Path.append(1)
                    
        self.m_maph = len(self.map)
        self.m_mapw = len(self.map[0])

        self.lighthouses = map(tuple, init_state["lighthouses"])
        self.log('START')
        self.log(str(self.lighthouses))
        self.tri = Delaunay(self.lighthouses)
        self.log(str(self.tri.vertices))
        self.steps = []
        for triVerts in self.tri.vertices:
            self.steps.append(triVerts[0])
            self.steps.append(triVerts[1])
            self.steps.append(triVerts[2])
            
        self.stepIndex = self.findNearestLighthouse(self.init_pos[0], self.init_pos[1])
        self.log(str(self.steps))


    def findNearestLighthouse (self, _x, _y):
        minValue = sys.float_info.min
        retValue = -1
        for i in xrange (len(self.lighthouses)):
            target = self.lighthouses[i]
            distance = abs(target[0] - _x) + abs (target[1] - _y)
            if distance < minValue:
                retValue = i
        return retValue



    def nextStep(self):
        """ Pass to the next step in the delonay triangulation"""
        self.log('NEXTSTEP_CALL')
        self.log(str(self.stepIndex))
        self.stepIndex +=1
        if self.stepIndex >= len(self.steps):
            self.stepIndex = 0


    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada).
        
        state: estado actual del juego.
        """
        return self.nop()

    def success(self):
        """Éxito: llamado cuando la jugada previa es válida."""
        self.m_error = False
        pass

    def error(self, message, last_move):
        """Error: llamado cuando la jugada previa no es válida."""
        self.log("Recibido error: %s", message)
        self.log("Jugada previa: %r", last_move)
        self.m_error = True

    # ==========================================================================
    # Utilidades
    # No es necesario sobreescribir estos métodos.
    # ==========================================================================

    def log(self, message, *args):
        """Mostrar mensaje de registro por stderr"""
        print >>sys.stderr, "[%s] %s" % (self.NAME, (message % args))

    # ==========================================================================
    # Jugadas posibles
    # No es necesario sobreescribir estos métodos.
    # ==========================================================================

    def nop(self):
        """Pasar el turno"""
        return {
            "command": "pass",
        }

    def move(self, x, y):
        """Mover a una casilla adyacente
        
        x: delta x (0, -1, 1)
        y: delta y (0, -1, 1)
        """
        return {
            "command": "move",
            "x": x,
            "y": y
        }

    def attack(self, energy):
        """Atacar a un faro
        
        energy: energía (entero positivo)
        """
        return {
            "command": "attack",
            "energy": energy
        }

    def connect(self, destination):
        """Conectar a un faro remoto
        
        destination: tupla o lista (x,y): coordenadas del faro remoto
        """
        return {
            "command": "connect",
            "destination": destination
        }

# ==============================================================================
# Interfaz
# ==============================================================================

class Interface(object):
    def __init__(self, bot_class):
        self.bot_class = bot_class
        self.bot = None
    
    def _recv(self):
        line = sys.stdin.readline()
        if not line:
            sys.exit(0)
        return json.loads(line)

    def _send(self, msg):
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()

    def run(self):
        init = self._recv()
        self.bot = self.bot_class(init)
        self._send({"name": self.bot.NAME})
        while True:
            state = self._recv()
            move = self.bot.play(state)
            self._send(move)
            status = self._recv()
            if status["success"]:
                self.bot.success()
            else:
                self.bot.error(status["message"], move)

if __name__ == "__main__":
    iface = Interface(Bot)
    iface.run()
