from machine import Pin, ADC, mem32
from time import sleep

# Pines de los LEDs para los semáforos
luces_semaforos = [2, 4, 5, 12, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26]
bandera = 0  # 0: Semáforo funcionando, 1: Medición de temperatura

# Función para manejar la interrupción del pulsador que cambia entre semáforo y temperatura
def cambiar_modo(pin):
    global bandera
    bandera = 1 if bandera == 0 else 0  # Alterna entre 0 (semaforo) y 1 (temperatura)

# Configurar el pulsador para cambiar de modo (GPIO25)
pulsador_modo = Pin(25, Pin.IN, Pin.PULL_UP)
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
        
        # 🚦 Fase 1: Vehicular Calle en rojo, giro vehicular en rojo, carr vehicular verde, peatonal calle verde, giro peatonal rojo 
        mem32[GPIO_OUT_REG] = 0b0000000110010001000000000000110000
        sleep(10)
        
        # 🚦 Fase 2: Vehicular amarillo en Calle,
        mem32[GPIO_OUT_REG] = 0b0000000010001001010000000000100100
        sleep(20)

        # 🚦 Fase 3: Vehicular Calle en Rojo, Carrera en Verde, Extra en Verde, Peatonal Calle en Verde
        mem32[GPIO_OUT_REG] = 0b00000000000010101000000000000000
        sleep(3)

        # 🚦 Fase 4: Precaución (Amarillo en Carrera)
        mem32[GPIO_OUT_REG] = 0b00000000000000101000000000000000
        sleep(2)

        # 🚦 Fase 5: Peatonales en Verde, Vehiculares en Rojo
        mem32[GPIO_OUT_REG] = 0b00000000000000000010000000010000
        sleep(5)

        # 🚦 Fase 6: Todo en Rojo antes de reiniciar el ciclo
        mem32[GPIO_OUT_REG] = 0b00000000000000000000000000000000
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