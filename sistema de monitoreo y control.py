# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================
from machine import Pin, ADC, PWM
from utime import sleep, ticks_ms, ticks_diff   

# =========================
# CONFIGURACIÓN DE PINES
# =========================

# LEDs (nivel de luz)
led_rojo = Pin(12, Pin.OUT)
led_amarillo = Pin(14, Pin.OUT)
led_verde = Pin(27, Pin.OUT)

# Pulsador (INTERRUPCIÓN)
boton = Pin(22, Pin.IN, Pin.PULL_UP)

# ADC (sensores)
lm35 = ADC(Pin(34))       # Temperatura
ldr = ADC(Pin(35))        # Luz
pot = ADC(Pin(32))        # Referencia

# Configurar rango ADC
lm35.atten(ADC.ATTN_11DB)
ldr.atten(ADC.ATTN_11DB)
pot.atten(ADC.ATTN_11DB)

# Servo
servo = PWM(Pin(26), freq=50)

# =========================
# VARIABLES DE CONTROL
# =========================
bandera_sistema = False
ultimo_tiempo = 0   # agregado (para debounce) con el fin de evitar el rebote del boton

# =========================
# FUNCIONES
# =========================

#funcion angulo movimiento del servo
def set_servo(angle): 
    duty = int((angle / 90) * (77 - 26) + 26) #transformacion en duty (ciclo de trabjo del servo) utilizando PWM
    servo.duty(duty)

#funcion para apargar todos los sistemas 
def apagar_todo(): 
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)
    set_servo(0)

# funcion con debounce para control del sistema apagado o encendido 
def toggle_sistema(pin):
    global bandera_sistema, ultimo_tiempo #variables globales para poder modificarlas dentro de la funcion 

    ahora = ticks_ms() #tiempo que lleva el sistema activo
    # se verifica si ha pasado más de 300 ms desde la última pulsación válida, esto evita múltiples activaciones por el rebote del botón
    if ticks_diff(ahora, ultimo_tiempo) > 300:
        #se cambia el estado de la variable global
        bandera_sistema = not bandera_sistema
        #se imprime el estado actual del sistema
        print("Sistema ACTIVADO" if bandera_sistema else "Sistema DESACTIVADO")
        #se actualiza el tiempo
        ultimo_tiempo = ahora

# =========================
# INTERRUPCIÓN
# =========================
boton.irq(trigger=Pin.IRQ_FALLING, handler=toggle_sistema)

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    #poner todo en cero antes de inicar el sistema 
    if not bandera_sistema:
        apagar_todo()
        sleep(0.2)
        continue

    # =========================
    # 1. TEMPERATURA (LM35)
    # =========================
    valor_temp = lm35.read()
    voltaje = (valor_temp / 4095) * 3.3 #conversion de V a C
    temperatura = voltaje * 100

    # =========================
    # 2. REFERENCIA (POT)
    # =========================
    valor_pot = pot.read()
    temp_ref = 25 + (valor_pot / 4095) * (45 - 25) # esta formula escala linealmente desde 0–4095 a un rango de 25 °C a 45 °C para definir los valores de referencia

    print(f"Temp: {temperatura:.2f} °C | Ref: {temp_ref:.2f} °C")

    # =========================
    # 3. CONTROL SERVO
    # =========================
    if temperatura < temp_ref:
        set_servo(0)
    else:
        set_servo(90)

    # =========================
    # 4. SENSOR DE LUZ (LDR)
    # =========================
    valor_luz = ldr.read()
    # se verifica que todos esten en cero
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)

    #condicionales egun el control de luz y lectrura del sensor
    if valor_luz < 1000:
        led_rojo.value(1)
    elif valor_luz < 2500:
        led_amarillo.value(1)
    else:
        led_verde.value(1)

    sleep(0.5)   