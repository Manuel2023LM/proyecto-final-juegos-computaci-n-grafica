# Furia de Zeus: Ecos del Caos

Juego arcade de acción hecho con Pygame, cámara, controles por gestos y recursos
gráficos y de audio incluidos en el proyecto.

## Ejecutar

```powershell
python -m pip install -r requirements.txt
python juego.py
```

Entorno de referencia validado: Python 3.11. La cámara es opcional.

El juego comienza en una ventana redimensionable de **960 × 720**; puedes
maximizarla o pulsar **F11** para alternar a pantalla completa. `fondo.jpg`
rellena los márgenes y cada mundo se presenta centrado. Si la cámara no está
disponible, puedes jugar con teclado.

## Organización y puesta en marcha

- `juego.py`: punto de entrada, reglas y pantallas del juego.
- `assets/images/backgrounds/`, `assets/images/sprites/` y
  `assets/images/powers/`: escenarios, personajes y poderes.
- `assets/audio/music/`, `assets/audio/powers/` y `assets/audio/effects/`:
  música, poderes y efectos de interfaz/disparo.
- `assets/video/`: video de introducción.
- `requirements.txt`: dependencias de Python.

Desde la carpeta del proyecto, instala las dependencias y verifica los recursos
con `python juego.py --self-test`; luego inicia con `python juego.py`. Los
recursos se resuelven desde la ubicación del juego, no desde la carpeta actual
de la terminal.

En el menú:

- **JUGAR** reproduce `video introduccion.mp4`; pulsa **Enter** para saltarlo.
- **ELEGIR NIVEL** permite iniciar cualquiera de los diez mundos directamente,
  haciendo clic o usando las teclas **1-9** y **0** para el nivel 10.
- **INSTRUCCIONES**, **PUNTAJE** y **SALIR** conservan sus funciones.

Cada mundo tiene escenario, enemigos, aura del jugador, música y jefe propios.
El nivel comienza con pocos enemigos, luego aparecen dos oleadas cada vez mayores
y, tras vencer a la última, llega el jefe final del mundo. Las formaciones tienen
un límite inferior y no pueden salir de la pantalla. Los enemigos y los jefes se
vuelven más difíciles al avanzar. Cada nivel nuevo comienza con las **3 vidas
completas**. La barra de poderes está en el lateral para no tapar al jugador. La
barra de salud está en la esquina superior izquierda, junto al nivel; absorbe
**4 impactos** antes de descontar una vida y se repone al perderla.
El décimo mundo ahora es el **Mundo de Ares**, con sus dos escenarios, dos tipos
de enemigos, música de fuego y Ares como jefe final.
Las canciones renombradas se asignan por su etiqueta de audio: `sonido1` al menú,
`sonido6`, `sonido4`, `sonido8` y `sonido7` a los niveles 7-10, y `sonido3`,
`sonido2` y `sonido5` a las fases del jefe final.
Después de cada jefe aparece una crónica original sobre Aster en una pantalla
negra, con tipografía serif cinematográfica original en rojo. Pulsa **Enter**
para revelar el texto y otra vez para continuar; **Esc** permite volver a elegir
un mundo. Al vencer al jefe del décimo nivel aparece la ilustración final con su
música; después de 10 segundos o al pulsar **Enter**, se muestra el mensaje de
victoria.

## Controles

**Mano derecha**

- Solo índice: mover a la izquierda; índice y medio: mover a la derecha.
- Tres dedos: pausar/reanudar.
- Puño cerrado: disparar. **Espacio** también dispara con el teclado.
- Los botones usan el efecto de espada incluido. El láser se mantiene mientras
  disparas y se detiene al soltar el puño o la barra espaciadora.

**Mano izquierda**

- Solo índice: rayo de Zeus.
- Índice y medio: congelar a los enemigos mientras mantienes el gesto.
- Índice, medio y anular: energía.
- Índice, medio, anular y meñique: olas de Poseidón.
- Mano izquierda abierta, con los cinco dedos levantados y separados: fuego de Ares.

Mientras mantienes un gesto de poder, su imagen y sonido permanecen activos;
la ilustración del rayo azul acompaña cada poder. Al soltarlo, el sonido y el
efecto visual se detienen. Los ataques se ejecutan una vez al reconocer el gesto
y respetan su enfriamiento. Las imágenes de los poderes aparecen más grandes y
conservan sus colores originales. El hielo también daña y aturde una vez al jefe
cuando se activa; con una vida y salud crítica aparece un filtro rojo de alerta.

**Teclado**

- Flechas o WASD: mover; **Espacio**: disparar; **Esc**: pausa.
- **1** o **E**: rayo; **2**: activar/desactivar congelamiento; **3**: energía;
  **4**: olas de Poseidón; **5**: fuego de Ares.
- Mantén **1**, **E**, **3**, **4** o **5** para mantener el efecto visual y el
  sonido; suelta la tecla para detenerlos. **2** alterna el congelamiento y sus
  efectos.
- En el menú, **Enter** inicia JUGAR, **N** abre la selección de niveles,
  **I** abre instrucciones y **P** muestra el puntaje. **V** alterna la vista
  de cámara.

FFmpeg prepara localmente la música, los efectos y el audio de la introducción.
Los archivos WAV temporales se guardan fuera del proyecto y se eliminan al
cerrar el juego. Para comprobar los recursos y las funciones principales:

```powershell
python juego.py --self-test
```
