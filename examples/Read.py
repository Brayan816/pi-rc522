#!/usr/bin/env python
"""
Based on PI-RC522
htttps://github.com/ondryaso/pi-rc522.git
Modified bt Brayan Stiven Garcia Peña
Mail: Brayang2111@gmail.com
Phone: 3227779328
Modification Date: 27/05/2019
"""
import mysql.connector
import smbus2 as smbus
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
import lcddriver
lcd = lcddriver.lcd()
lcd.lcd_clear()

import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = True
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)
Nombre=""
Sexo=""
Edad=""
Identificacion=""
Identificacion2=""
Cargo=""
Celular=""
Correo1=""
Correo=""
Universidad=""


print("Starting")

while run:
    lcd.lcd_display_string("Salon Tecno      ", 1)
    lcd.lcd_display_string("                 ", 2)
    GPIO.output(37, True)
    rdr.wait_for_tag()
    
    (error, data) = rdr.request()
    
    if not error:
        print("\nDetected: " + format(data, "02x"))
    

    (error, uid) = rdr.anticoll()
    
    if not error:
        
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        print("Setting tag")
        util.set_tag(uid)
        util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
       
        print("Sexo   ")
        Sexo=util.read_out(9)
        print(Sexo)
        print("Edad")
        Edad=util.read_out(10)
        print(Edad)
        print("Identificacion")
        Identificacion=util.read_out(12)
        print(Identificacion)
        print("Cargo")
        Cargo=util.read_out(13)
        print(Cargo)
        print("Celular")
        Celular=util.read_out(14)
        print(Celular)
        print("CORREO")
        Correo1=util.read_out(16)
        Correo=Correo1 + util.read_out(17)
        print(Correo)
        print("Universidad")
        Colegio=util.read_out(20)
        print(Universidad)
        print("Nombre y apelldido")
        Nombre=util.read_out(8)
        print(Nombre)
        Fecha=time.strftime("%c")
        time.sleep(0.1)

        if Identificacion2==Identificacion:
            lcd.lcd_display_string("Quite la tarjeta", 1)
            time.sleep(1.2)
        else:
            if Nombre != "0" and Sexo != "0" and Edad != "0" and Identificacion and Cargo != "0" and Celular != "0" and Correo != "0" and Colegio != "0":
              if Sexo =="Hombre          ":
                    lcd.lcd_display_string("Bienvenido      ", 1)
              else:
                    lcd.lcd_display_string("Bienvenida      ", 1)
                
              lcd.lcd_display_string(Nombre,2)
              GPIO.output(37,False)
              GPIO.output(40,True)
              GPIO.output(38,True)
              time.sleep(.2)
              GPIO.output(40,False)                
              time.sleep(0.5)
              con = mysql.connector.connect(user="root",password="bsgp4444",host="127.0.0.1",database="Salon Tecno")
              cursor=con.cursor()
              cursor.execute('''INSERT INTO asistencia (Nombre,Sexo,Edad,Identificacion,Cargo,Celular,Correo,Colegio,Fecha) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)''',(Nombre,Sexo,Edad,Identificacion,Cargo,Celular,Correo,Colegio,Fecha))
              con.commit()
              con.close()
              util.deauth()
              time.sleep(1)
              GPIO.output(40,False)
              GPIO.output(37,True)
              GPIO.output(38,False)
              Identificacion2=Identificacion
        
          
            
            else:
                lcd.lcd_display_string("Error           ",1)
                GPIO.output(35,True)
                GPIO.output(37,False)   
                time.sleep(3)
                GPIO.output(35,False)
                GPIO.output(37,True)
                util.deauth()
        
            
            
        
        
        


        
       
