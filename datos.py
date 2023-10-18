import tkinter as tk

# Función que se ejecutará cuando se presione el botón
def crear_archivo_con_lista():
    # Obtener el texto de cada label y almacenarlo en una lista
    lista_texto = [label.cget("text") for label in labels]

    # Crear un archivo de texto y escribir la lista
    with open('archivo_con_lista.txt', 'w') as archivo:
        archivo.write('\n'.join(lista_texto))

# Crear la ventana
ventana = tk.Tk()
ventana.title("Crear archivo con lista de textos")

# Crear varios labels con texto
labels = []
for i in range(1, 6):
    label = tk.Label(ventana, text=f"Label {i}")
    label.pack()
    labels.append(label)

# Crear un botón para crear el archivo
boton = tk.Button(ventana, text="Crear Archivo con Lista", command=crear_archivo_con_lista)
boton.pack()

# Iniciar el bucle de la ventana
ventana.mainloop()