from tkinter import * #la libreria para la interfaz grafica
root = Tk()
#esta es la clase sala
class sala:
    #aqui definimos los atributos de la sala
    def __init__(self, idSala, capacidad, disponibilidad):
        self.idSala = idSala #el id de la sala
        self.capacidad = capacidad #la capacidad de la sala
        self.disponibilidad = disponibilidad #y si esta disponible

    def __str__(self): #qui el mensaje que nos dara cuando se mande a imprimir la clase de sala
        return f"Sala (El ID de la sala es: {self.idSala}, Esta sala tiene una capacidad de: {self.capacidad} personas y esta {self.disponibilidad})"

class reserva: #esta es la clase reserva
    def __init__(self, idReserva, personaQueReservo, horaReservacion): #otra vez se definen los atributos de la clase 
        self.idReserva = idReserva #el id de la reserva
        self.personaQueReservo = personaQueReservo #el nombre de la persona que reservo
        self.horaReservacion = horaReservacion # la hora de la reserva

    def __str__(self): #el mensaje que nos dara cuando se mande a llamar 
        return f"reserva (hay una reserva con id {self.idReserva}, para la persona {self.personaQueReservo} a la hora {self.horaReservacion})"
        #soy un comentario inutil uwu
        #estas dos variables solo son de prueba para llenar las clases de arriba
sala1 = sala(idSala=1, capacidad=40, disponibilidad="reservada")
reserva1 = reserva(idReserva=1, personaQueReservo="heisenberg", horaReservacion="3 pm")
#importante, esta funcion sera la que nos desplegara el texto al usar el boton para mostrar el estado de la sala
def mostrarSala():
        Label(root, text=sala1).pack()
#el boton para imprimir el estado de la sala
Button(root, text="mostrar estado del la sala 1", command=mostrarSala).pack()

def mostrarReservacion(): #la funcion para mostrar la reservacion de ejemplo
     Label(root, text=reserva1).pack()

Button(root, text="reservaciones", command=mostrarReservacion).pack() #boton para mostrar la informacion de la reserva
root.mainloop()
#por favor ya comente todo lo mejor que pude, no se te vaya a olvidar que hace este codigo por favor.