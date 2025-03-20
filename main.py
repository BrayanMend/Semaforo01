from machine import Pin, ADC, mem32
from time import sleep

# Pines de los LEDs para los semáforos
luces_semaforos = [2, 4, 5, 12, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26]
bandera = 0  # 0: Semáforo funcionando, 1: Medición de temperatura

# Función para manejar la interrupción del pulsador que cambia entre semáforo y temperatura
def cambiar_modo(pin):
    global bandera
    bandera = 1 if bandera == 0 else 0  # Alterna entre 0 (semaforo) y 1 (temperatura)

# Configurar el pulsador para cambiar de modo (GPIO25)
pulsador_modo = Pin(14, Pin.IN, Pin.PULL_UP)
pulsador_modo.irq(trigger=Pin.IRQ_RISING, handler=cambiar_modo)

# Configurar el sensor de temperatura LM35
sensor_temperatura = ADC(Pin(39))  # Entrada analógica para el sensor
sensor_temperatura.atten(ADC.ATTN_11DB)  # Atenuación para rango completo (0-3.3V)
sensor_temperatura.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits

# Activar los pines de las luces de los semáforos
for pin_num in luces_semaforos:
    Pin(pin_num, Pin.OUT)

GPIO_OUT_REG = 0x03FF44004  # Dirección de los registros GPIO en el ESP32

# Ciclo principal
while True:
    
    while bandera == 0:  # Modo Semáforo
        
        print("Semáforo funcionando ☑")
        
        # 🚦 Fase 1: Vehicular Calle en rojo, giro vehicular en rojo, carr vehicular verde, peatonal calle verde, giro peatonal verde y carrera peatonal rojo 
        mem32[GPIO_OUT_REG] = 0b0000000110010001000000000000110000
        sleep(5)

        mem32[GPIO_OUT_REG] = 0b0000000110000001000000000000110100 
        sleep(5)
        
        mem32[GPIO_OUT_REG] = 0b0000000010001001000000000000110100
        sleep(5)
        
         # 🚦 Fase 1: Vehicular Calle en amari, giro vehicular en rojo, carr vehicular amari, peatonal calle verde y rojo, giro peatonal verde y carrera peatonal verde 
        mem32[GPIO_OUT_REG] = 0b0000000000101000110001000000100000
        sleep(5)

        mem32[GPIO_OUT_REG] = 0b0000000000101010110001000000000000
        sleep(5)

         # 🚦 Fase 1: Vehicular Calle en amari, giro vehicular en rojo, carr vehicular amari, peatonal calle verde y rojo, giro peatonal verde y carrera peatonal verde 
        mem32[GPIO_OUT_REG] = 0b0000000000101010101001000000000000
        sleep(5)

         # 🚦 Fase 6: Todo en Rojo antes de reiniciar el ciclo
        mem32[GPIO_OUT_REG] = 0b0000000000000000000000000000000000
        sleep(2)

    while bandera == 1:  # Modo Temperatura
        
        print("Sensor de temperatura activado ☑")
        
        # Apagar todos los semáforos
        mem32[GPIO_OUT_REG] = 0b00000000000000000000000000000000
        
        # Leer el valor del sensor LM35
        valor_adc = sensor_temperatura.read()

        # Conversión de la lectura ADC a temperatura en grados Celsius
        voltaje = (valor_adc / 1023.0) * 3.3  # Convertir lectura a voltaje (0-3.3V)
        temperatura = voltaje * 100  # LM35 tiene una relación de 10mV/°C

        print("Temperatura:", round(temperatura, 2), "°C")
        
        sleep(1)  # Espera para actualizar la lectura