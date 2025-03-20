# main.py -- put your code here!
from machine import Pin, ADC, mem32
from time import sleep

# Pines de los LEDs del semáforo
luces_semaforos = [2, 4, 5, 15, 16, 17, 18, 19, 22, 23]
bandera = 0

# Función para manejar la interrupción del pulsador que cambia al modo de temperatura
def activar_temperatura(pin):
    global bandera
    bandera = 2  # Se activa la medición de temperatura

# Configurar el pulsador que activa la medición de temperatura
pulsador_temperatura = Pin(25, Pin.IN)
pulsador_temperatura.irq(trigger=Pin.IRQ_RISING, handler=activar_temperatura)

# Configurar el sensor de temperatura LM35
sensor_temperatura = ADC(Pin(39))  # Entrada analógica para el sensor
sensor_temperatura.atten(ADC.ATTN_11DB)  # Atenuación para rango completo (0-3.3V)
sensor_temperatura.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits

# Función para manejar la interrupción del pulsador que activa el semáforo normal
def activar_semaforo(pin):
    global bandera
    bandera = 0  # Regresa al semáforo normal

# Configurar el pulsador que activa el semáforo
pulsador_semaforo = Pin(26, Pin.IN)
pulsador_semaforo.irq(trigger=Pin.IRQ_RISING, handler=activar_semaforo)

# Activar los pines de las luces de los semáforos
for pin_num in luces_semaforos:
    Pin(pin_num, Pin.OUT)

GPIO_OUT_REG = 0x03FF44004  # Dirección de los registros GPIO en el ESP32

# Bucle principal
while True:
    if bandera == 0:
        print("Semáforo funcionando ☑")
        
        # Carrera: inicia con el ROJO vehicular encendido y el VERDE peatonal encendido
        # Calle: inicia con el VERDE vehicular encendido y el ROJO peatonal encendido
        mem32[GPIO_OUT_REG] = 0b00000000100000010000000000110000  # Pines 4, 5, 16 y 23 activos
        sleep(3)
        
        for _ in range(3):
            # Intermitencia del semáforo antes de cambiar
            mem32[GPIO_OUT_REG] = 0b00000000100000000000000000010000  # Pines 4 y 19 activos
            sleep(1)
            mem32[GPIO_OUT_REG] = 0b00000000100000010000000000110000  # Pines 4, 5, 16 y 23 activos
            sleep(1)
        
        # Cambio a AMARILLO antes de cambiar la vía
        mem32[GPIO_OUT_REG] = 0b00000000100001100000000000010100  # Pines 2, 4, 17, 18 y 23 activos
        sleep(8)
        
        # Cambio de vía
        mem32[GPIO_OUT_REG] = 0b00000000010010101000000000000000  # Pines 15, 17, 19 y 22 activos
        sleep(3)
        
        for _ in range(3):
            mem32[GPIO_OUT_REG] = 0b00000000000010100000000000000000  # Pines 17 y 19 activos
            sleep(1)
            mem32[GPIO_OUT_REG] = 0b00000000010010101000000000000000  # Pines 15, 17, 19 y 22 activos
            sleep(1)
        
        # Cambio a AMARILLO antes de regresar al estado inicial
        mem32[GPIO_OUT_REG] = 0b00000000100011100000000000000100
        sleep(8)
    
    elif bandera == 2:
        print("Sensor de temperatura activado ☑")
        
        # Leer el valor del sensor LM35
        valor_adc = sensor_temperatura.read()
        
        # Conversión de la lectura ADC a temperatura en grados Celsius
        voltaje = (valor_adc / 1023.0) * 3.3  # Convertir lectura a voltaje (0-3.3V)
        temperatura = voltaje * 100  # LM35 tiene una relación de 10mV/°C
        
        print("Temperatura:", round(temperatura, 2), "°C")
        
        sleep(1)  # Espera para actualizar la lectura
        
        # Al presionar el pulsador de semáforo, volverá al modo normal