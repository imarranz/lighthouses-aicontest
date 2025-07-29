
# AI Contest Bot | Euskal Encounter

> :sparkles: Preparando mi participación en el AI Contest de la próxima Euskal Encounter con un bot inteligente y competitivo.
> ¡Una mezcla perfecta de estrategia, programación y diversión!

![](https://repository-images.githubusercontent.com/1026837935/ca818406-a88f-46fd-89dd-d644e7f47b5e)

![Author](https://img.shields.io/badge/author-imarranz-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Language](https://img.shields.io/badge/python-3.9+-yellow?style=flat-square)
![Status](https://img.shields.io/badge/status-en%20desarrollo-orange?style=flat-square)
![AI Contest](https://img.shields.io/badge/AI%20Contest-Euskal%20Encounter%202026-purple?style=flat-square)
![Stars](https://img.shields.io/github/stars/imarranz/lighthouses-aicontest?style=flat-square)
![Forks](https://img.shields.io/github/forks/imarranz/lighthouses-aicontest?style=flat-square)
![Pull Request](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)

## :rocket: Introducción

El **AI Contest** de la [Euskal Encounter](https://www.euskalencounter.org) es un reto anual de programación donde desarrolladores crean bots autónomos para competir en un juego por turnos. Este evento reúne a entusiastas del software libre, la inteligencia artificial y los videojuegos en un ambiente creativo y altamente técnico.

En la próxima edición el reto girará en torno al juego **Laser Lighthouses**, un entorno de combate estratégico con información parcial. Los bots deben navegar por el mapa, capturar faros, evitar peligros y derrotar a su oponente, todo bajo condiciones de tiempo limitado y visión parcial del entorno.

Este proyecto tiene como objetivo desarrollar un bot competitivo, utilizando técnicas de programación, IA y estrategias adaptativas, y compartir el código como ejemplo didáctico y base para futuras mejoras.

## :video_game: ¿De qué va el juego?

- Juego por turnos con **información parcial del entorno**.
- Controlas una unidad que puede moverse, disparar o interactuar con el mundo.
- Objetivo: **capturar faros** y maximizar la puntuación.
- Dos o más bots se enfrentan en un mapa común. El mejor bot gana.

Más detalles y reglas en el repositorio oficial del juego: [https://github.com/marcan/lighthouses_aicontest](https://github.com/marcan/lighthouses_aicontest)

## :hammer_and_wrench: Tecnologías

- :snake: Python 3.9+ (bot principal)
- :computer: Motor de juego C++ (externo)
- :bookmark_tabs: Comunicación estándar por `stdin`/`stdout`
- :rocket: Opcional: uso de heurísticas, planificación, búsqueda o aprendizaje por refuerzo

## :file_folder: Estructura del repositorio

```
.
├── bot/                # Código fuente del bot
│ └── mybot.py          # Implementación principal
├── engine/             # Copia del motor oficial del juego (C++)
├── maps/               # Mapas de prueba o creados manualmente
├── examples/           # Bots de ejemplo y referencias externas
├── run_iacontest.sh    # Script para ejecutar el bot fácilmente
├── requirements.txt    # Dependencias de Python
├── aicontest_spec.txt  # Especificaciones del juego
└── README.md           # Este documento

````

## :zap: Cómo ejecutar

1. Clona este repositorio:

```bash
git clone https://github.com/imarranz/lighthouses-aicontest.git
cd lighthouses-aicontest
````

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta el bot contra el motor de juego:

```bash
./run_iacontest.sh
```

:warning: *Necesitas tener el motor de juego oficial descargado aparte y disponible en el PATH o configurado en `run_iacontest.sh`.*

## :brain: Estrategia del bot
  
* :gear: **Fase inicial**: bot reactivo con lógica heurística.
* :brain: **Fase intermedia**: incorporación de mapas internos, planificación y predicción de oponentes.
* :robot: **Fase avanzada**: experimentación con técnicas de IA (Monte Carlo, Q-learning...).
* :dart: **Objetivo final**: desarrollar un bot robusto y difícil de vencer.


## :trophy: ¿Por qué me gustaría participar?

* :nerd_face: Para aprender técnicas reales de IA aplicadas a entornos dinámicos.
* :keyboard: Para practicar escritura de bots y lógica de juego en tiempo real.
* :handshake: Para participar en una comunidad abierta y creativa.
* :fire: ¡Y para divertirme!

> :sparkles: ¡Nos vemos en la Euskal Encounter! Que gane el bot más listo. :robot:

## Otros proyectos

  - [https://github.com/ilopezgazpio/LightHouses_AIContest](https://github.com/ilopezgazpio/LightHouses_AIContest)
