# main.py -- put your code here!
from time import sleep
from machine import Pin
from machine import mem32


rojopeatonal=Pin(2,Pin.OUT)
verdevehicular=Pin(13,Pin.OUT)
amarillovehicular=Pin(12,Pin.OUT)
rojovehicular=Pin(14,Pin.OUT)
verdepeatonal=Pin(4,Pin.OUT)

global variable
variable=0

def interrupcion(Pin):
    global variable
    print("Entre a la funcion interrupcion")
    variable=1

pulsador=Pin(25,Pin.IN)
pulsador.irq(trigger=Pin.IRQ_RISING,handler=interrupcion)

GPIO_SET=const(0x3FF44004) #posición en memoria

while True:
    mem32[GPIO_SET]=0B10000000000100 #bit 13(blanco/verde vehicular) y 2(azuldentro/rojo peatonal) encendidos 
    sleep(5)
    mem32[GPIO_SET]=0B00000000000100
    sleep(0.5)
    mem32[GPIO_SET]=0B10000000000100 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B00000000000100 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B10000000000100 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B00000000000100 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B01000000000100 #bit 13 y 2 encendidos
    sleep(2)
    mem32[GPIO_SET]=0B00000000000100 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B100000000010000 #bit 13 y 2 encendidos
    sleep(5)
    mem32[GPIO_SET]=0B100000000000000 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B100000000010000 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B100000000000000 #bit 13 y 2 encendidos
    sleep(0.5)
    mem32[GPIO_SET]=0B100000000010000 #bit 13 y 2 encendidos
    sleep(0.5)
    if variable==1:
        mem32[GPIO_SET]=0B110000000000100
        sleep(10)
        variable=0