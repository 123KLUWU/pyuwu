import tkinter as tk # librería para interfaz gráfica
from tkinter import ttk, messagebox
import sqlite3 # librería para usar base de datos

# esta es la clase Sala
class Sala:
    def __init__(self, idSala, capacidad): # los atributos de la sala
        self.idSala = idSala # el id de la sala
        self.capacidad = capacidad # la capacidad de la sala

    def __str__(self): # este es el mensaje que mostrará cuando se mande a imprimir
        return f"Sala {self.idSala} Capacidad de: {self.capacidad} personas"

# esta es la clase Reserva
class Reserva:
    def __init__(self, idReserva, nombrePersona, horaReservacion, sala): # lo mismo que arriba, estos son los atributos
        self.idReserva = idReserva # id de la reserva
        self.nombrePersona = nombrePersona # el nombre de la persona que reservó
        self.horaReservacion = horaReservacion # la hora de la reservación
        self.sala = sala # la sala que reservó

    def __str__(self): # el mensaje que dará cuando se mande a llamar
        return f"Reserva {self.idReserva} - {self.nombrePersona} a las {self.horaReservacion} en {self.sala}"

def crearConexion():
    conexion = None
    try:
        conexion = sqlite3.connect('baseDeDatos.db')
        print("Conexión establecida a baseDeDatos.db")
    except sqlite3.Error as error:
        print(error)
    return conexion

def crearTabla(conexion):
    try:
        sqlCrearTabla = """ CREATE TABLE IF NOT EXISTS reservas (
                                id INTEGER PRIMARY KEY,
                                nombrePersona TEXT NOT NULL,
                                horaReservacion TEXT NOT NULL,
                                idSala INTEGER NOT NULL,
                                capacidad INTEGER NOT NULL
                            ); """
        cursor = conexion.cursor()
        cursor.execute(sqlCrearTabla)
    except sqlite3.Error as error:
        print(error)

def insertarReserva(conexion, reserva):
    sql = ''' INSERT INTO reservas(nombrePersona, horaReservacion, idSala, capacidad)
              VALUES(?,?,?,?) '''
    cursor = conexion.cursor()
    cursor.execute(sql, reserva)
    conexion.commit()
    return cursor.lastrowid

def cargarReservas(conexion):
    sql = ''' SELECT * FROM reservas '''
    cursor = conexion.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        sala = next((s for s in salas if s.idSala == row[3]), None)
        if sala:
            reserva = Reserva(row[0], row[1], row[2], sala)
            reservas.append(reserva)

# función para hacer una reserva
def hacerReservacion(): 
    nombrePersona = entryNombrePersona.get() # el nombre de la persona que va a usar la sala
    horaReservacion = comboHoras.get() # la hora de la reservación
    salaSeleccionada = comboSalas.get() # la sala seleccionada
    
    if not nombrePersona or not horaReservacion or not salaSeleccionada: # este if nos dará un mensaje de error en caso de que no se rellenara algún campo de arriba
        messagebox.showwarning("Error", "Por favor, rellenar todos los campos.") # el mensaje de error
        return

    salaObj = None # aquí se guardará la reservación
    for sala in salas:
        if str(sala.idSala) == salaSeleccionada.split()[1]:
            salaObj = sala
            break

    # Verificar si ya existe una reserva para esa sala en la misma hora
    for reserva in reservas:
        if reserva.sala.idSala == salaObj.idSala and reserva.horaReservacion == horaReservacion:
            messagebox.showwarning("Hora no disponible", "La sala ya está reservada para esa hora.")
            return

    # Realizar la reserva
    reserva = Reserva(len(reservas) + 1, nombrePersona, horaReservacion, salaObj) # el valor que se asigna a la reserva
    reservas.append(reserva) 
    insertarReserva(conexion, (nombrePersona, horaReservacion, salaObj.idSala, salaObj.capacidad))
    messagebox.showinfo("Reservación exitosa", f"Reservación hecha por {nombrePersona} a las {horaReservacion} en la Sala {salaObj.idSala}") # mensaje cuando se hace la reservación 
    entryNombrePersona.delete(0, tk.END) # se limpia el entry del nombre de la persona
    comboHoras.set('') # limpiar el combobox de horas después de hacer una reservación
    actualizarSalas() # se actualiza la sala

# función para mostrar las reservas
def mostrarReservas():
    listaReservas.delete(0, tk.END) # limpiar la lista antes de mostrar
    for reserva in reservas:
        listaReservas.insert(tk.END, reserva) # muestra las reservas hechas

# función para actualizar la lista de salas disponibles para mostrar solo las disponibles
def actualizarSalas():
    horasDisponibles = [f'{hora}:00' for hora in range(9, 22)] # horas de 9 a.m. a 9 p.m.
    salasDisponibles = [str(sala) for sala in salas]

    # Verificar horas disponibles para cada sala
    for reserva in reservas:
        if reserva.horaReservacion in horasDisponibles:
            horasDisponibles.remove(reserva.horaReservacion)

    comboHoras['values'] = horasDisponibles
    comboSalas['values'] = salasDisponibles

# Listas para almacenar datos
salas = [Sala(1, 40), Sala(2, 30)]
reservas = []

# Inicializar la base de datos y cargar reservas
conexion = crearConexion()
crearTabla(conexion)
cargarReservas(conexion)

root = tk.Tk()
root.title("Sistema de Gestión de Reservas") # título del programa

# Etiquetas y campos de entrada
labelNombrePersona = tk.Label(root, text="Nombre de la persona que reserva:")
labelNombrePersona.pack()
entryNombrePersona = tk.Entry(root)
entryNombrePersona.pack()

labelHora = tk.Label(root, text="Hora de reservación:")
labelHora.pack()

# Combo box para seleccionar la hora de reservación
comboHoras = ttk.Combobox(root, state="readonly")
comboHoras.pack()

labelSala = tk.Label(root, text="Seleccionar Sala:")
labelSala.pack()
comboSalas = ttk.Combobox(root, state="readonly")
comboSalas.pack()
actualizarSalas()

# Botón para hacer una reservación
botonReservar = tk.Button(root, text="Hacer Reservación", command=hacerReservacion)
botonReservar.pack()

# Lista para mostrar reservas
listaReservas = tk.Listbox(root) # listbox donde se mostrarán
listaReservas.pack()

# Botón para mostrar reservas
botonMostrar = tk.Button(root, text="Mostrar Reservas", command=mostrarReservas)
botonMostrar.pack()

root.mainloop()
conexion.close()
