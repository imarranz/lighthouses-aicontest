
# Euskal Encounter 34 - AI Contest Bot (2026)

> :sparkles: Participación en el AI Contest de la Euskal Encounter 34 con un bot inteligente y competitivo.  
> ¡Una mezcla perfecta de estrategia, programación y diversión!

---

## :rocket: Introducción

El **AI Contest** de la [Euskal Encounter](https://www.euskalencounter.org) es un reto anual de programación donde desarrolladores crean bots autónomos para competir en un juego por turnos. Este evento reúne a entusiastas del software libre, la inteligencia artificial y los videojuegos en un ambiente creativo y altamente técnico.

En la próxima edición (EE34 - 2026), el reto girará en torno al juego **Laser Lighthouses**, un entorno de combate estratégico con información parcial. Los bots deben navegar por el mapa, capturar faros, evitar peligros y derrotar a su oponente, todo bajo condiciones de tiempo limitado y visión parcial del entorno.

Este proyecto tiene como objetivo desarrollar un bot competitivo, utilizando técnicas de programación, IA y estrategias adaptativas, y compartir el código como ejemplo didáctico y base para futuras mejoras.

---

## :video_game: ¿De qué va el juego?

- Juego por turnos con **información parcial del entorno**.
- Controlas una unidad que puede moverse, disparar o interactuar con el mundo.
- Objetivo: **capturar faros** y maximizar la puntuación.
- Dos bots se enfrentan en un mapa común. El mejor bot gana.

Más detalles y reglas en el repositorio oficial del juego: [https://github.com/marcan/lighthouses_aicontest](https://github.com/marcan/lighthouses_aicontest)

---

## :hammer_and_wrench: Tecnologías

- :snake: Python 3.10+ (bot principal)
- :computer: Motor de juego C++ (externo)
- :bookmark_tabs: Comunicación estándar por `stdin`/`stdout`
- :rocket: Opcional: uso de heurísticas, planificación, búsqueda o aprendizaje por refuerzo

---

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

---

## :zap: Cómo ejecutar

1. Clona este repositorio:

```bash
git clone https://github.com/imarranz/ee34_aicontest_bot.git
cd ee34_aicontest_bot
````

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta el bot contra el motor de juego:

```bash
./run_iacontest.sh
```

:warning: *Necesitas tener el motor de juego oficial descargado aparte y disponible en el PATH o configurado en `run.sh`.*

---

## :brain: Estrategia del bot
  
* **Fase inicial**: bot reactivo con lógica heurística.
* **Fase intermedia**: incorporación de mapas internos, planificación y predicción de oponentes.
* **Fase avanzada**: experimentación con técnicas de IA (Monte Carlo, Q-learning...).
* :dart: **Objetivo final**: desarrollar un bot robusto y difícil de vencer.

---

## :bust\_in\_silhouette: Autor

Desarrollado por \[Tu nombre o nick].
Licencia: MIT

---

## :trophy: ¿Por qué participar?

* :nerd\_face: Aprendes técnicas reales de IA aplicadas a entornos dinámicos.
* :keyboard: Practicas escritura de bots y lógica de juego en tiempo real.
* :handshake: Participas en una comunidad abierta y creativa.
* :fire: ¡Y es realmente divertido!

---

> :sparkles: ¡Nos vemos en la Euskal Encounter 34! Que gane el bot más listo. :robot:

---


https://github.com/ilopezgazpio/LightHouses_AIContest
