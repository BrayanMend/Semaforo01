from machine import Pin, ADC, mem32
from time import sleep

# Pines de los LEDs del semáforo
luces_semaforos = [2, 4, 5, 15, 16, 17, 18, 19, 22, 23]
bandera = 0

# Función para manejar la interrupción del pulsador
def cambiar_modo(pin):
    global bandera
    bandera = 1 - bandera  # Alternar entre semáforo y sensor de temperatura

# Configurar el pulsador para cambiar entre modos
pulsador = Pin(25, Pin.IN)
pulsador.irq(trigger=Pin.IRQ_RISING, handler=cambiar_modo)

# Configurar el sensor de temperatura LM35
sensor_temperatura = ADC(Pin(39))  # Entrada analógica para el sensor
sensor_temperatura.atten(ADC.ATTN_11DB)  # Atenuación para rango completo (0-3.3V)
sensor_temperatura.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits

# Activar los pines de las luces de los semáforos
for pin_num in luces_semaforos:
    Pin(pin_num, Pin.OUT)

GPIO_OUT_REG = 0x03FF44004  # Dirección de los registros GPIO en el ESP32

# Bucle principal
while True:
    if bandera == 0:
        print("Semáforo funcionando ☑")
        mem32[GPIO_OUT_REG] = 0b00000000100000010000000000110000  # Pines 4, 5, 16 y 23 activos
        sleep(0.3)
        
        for _ in range(3):
            mem32[GPIO_OUT_REG] = 0b00000000100000000000000000010000  # Pines 4 y 19 activos
            sleep(0.11)
            mem32[GPIO_OUT_REG] = 0b00000000100000010000000000110000  # Pines 4, 5, 16 y 23 activos
            sleep(0.11)
        
        mem32[GPIO_OUT_REG] = 0b00000000100001100000000000010100  # Pines 2, 4, 17, 18 y 23 activos
        sleep(0.8)
        
        mem32[GPIO_OUT_REG] = 0b00000000010010101000000000000000  # Pines 15, 17, 19 y 22 activos
        sleep(0.3)
        
        for _ in range(3):
            mem32[GPIO_OUT_REG] = 0b00000000000010100000000000000000  # Pines 17 y 19 activos
            sleep(0.11)
            mem32[GPIO_OUT_REG] = 0b00000000010010101000000000000000  # Pines 15, 17, 19 y 22 activos
            sleep(0.11)
        
        mem32[GPIO_OUT_REG] = 0b00000000100011100000000000000100
        sleep(0.8)
    
    else:
        print("Sensor de temperatura activado ☑")
        valor_adc = sensor_temperatura.read()
        voltaje = (valor_adc / 1023.0) * 3.3  # Convertir lectura a voltaje (0-3.3V)
        temperatura = voltaje * 100  # LM35 tiene una relación de 10mV/°C
        print("Temperatura:", round(temperatura, 1), "°C")
        sleep(0.1)  # Espera para actualizar la lectura