# Sistema_de_monitero_y_control
El sistema permite medir la temperatura y el nivel de iluminación del entorno, y controlar automáticamente un sistema de ventilación representado por un servomotor y alerta de intensidad en iluminacion representados por diodos leds.  Además, el usuario puede activar o desactivar el sistema mediante un pulsador con interrupción, y ajustar la temperatura de referencia usando un potenciómetro.
Este proyecto consiste en el diseño e implementación de un sistema de monitoreo ambiental utilizando una ESP32 programada en MicroPython. Se cuenta con simulación funcional atraves de Wokwi.

## Funcionalidades principales:
- Medición de temperatura mediante sensor analógico (LM35 / NTC en simulación)
- Ajuste de temperatura de referencia (25 °C a 45 °C)
- Control automático de ventilación (servo)
- Medición de iluminación (LDR)
- Indicadores visuales con LEDs (bajo, medio, alto)
- Activación/desactivación del sistema mediante botón con interrupción y debounce

## Pines utilizados
- Componente -> Pin ESP32
- LED rojo (oscuro)	-> GPIO 12
- LED amarillo (luz media) ->	GPIO 14
- LED verde (alta luz) ->	GPIO 27
- Botón (interruptor) ->	GPIO 22
- Sensor de temperatura ->	GPIO 34
- LDR (luz) ->	GPIO 35
- Potenciómetro (referencia)	-> GPIO 32
- Servomotor	-> GPIO 26

## Instrucciones de operación
1. Ejecutar el programa en la ESP32.
2. Presionar el botón para activar el sistema.
3. Ajustar el potenciómetro para definir la temperatura de referencia.
4. El sistema medirá la temperatura ambiente y comparará con la referencia:
   - Si la temperatura es menor → ventilación cerrada (servo en 0°)
   - Si la temperatura es mayor o igual → ventilación activada (servo en 90°)
5. El nivel de iluminación se indica con LEDs:
   - Baja luz → LED rojo
   - Luz media → LED amarillo
   - Alta iluminación → LED verde
6. Presionar nuevamente el botón para desactivar el sistema.

### Notas adicionales
- Se implementó debounce por software para evitar rebote del botón.
- El sistema incluye un estado seguro que apaga LEDs y servo cuando está desactivado.
- En simulación (Wokwi), algunos sensores son representados con otra referencia diferente al LM35.

### LINK de simulación:
https://wokwi.com/projects/460402031625764865 
