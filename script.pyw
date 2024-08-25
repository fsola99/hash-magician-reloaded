import hashlib
import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Función para calcular los hashes de los archivos
def calcular_hashes(folder_path, file_list, hash_list, values):
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file_current:
                content = file_current.read()

                md5_value = hashlib.md5(content).hexdigest()
                sha1_value = hashlib.sha1(content).hexdigest()
                sha256_value = hashlib.sha256(content).hexdigest()
                if values['-UPPER-'].get():
                    md5_value = md5_value.upper()
                    sha1_value = sha1_value.upper()
                    sha256_value = sha256_value.upper()
                hash_list.append({'filename': file_name, 'md5': md5_value, 'sha256': sha256_value, 'sha1': sha1_value})
        else:
            calcular_hashes(file_path, os.listdir(file_path), hash_list, values)
    return hash_list

# Función para iniciar el cálculo
def iniciar():
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("Error", "No se ha seleccionado una carpeta. Por favor, seleccione una carpeta y vuelva a intentarlo.")
        return
    
    algoritmos_seleccionados = []
    if values['-MD5-'].get():
        algoritmos_seleccionados.append('md5')
    if values['-SHA1-'].get():
        algoritmos_seleccionados.append('sha1')
    if values['-SHA256-'].get():
        algoritmos_seleccionados.append('sha256')
    if not algoritmos_seleccionados:
        messagebox.showerror("Error", "No se ha seleccionado ningún algoritmo. Por favor, seleccione un tipo de algoritmo y vuelva a intentarlo.")
        return

    # Calcular los hashes de los archivos
    hash_list = []
    hashes = calcular_hashes(folder_path, os.listdir(folder_path), hash_list, values)

    # Output
    # Crear la lista de nombres de campo a partir de los algoritmos seleccionados
    fieldnames = ['filename']
    if 'md5' in algoritmos_seleccionados:
        fieldnames.append('md5')
    if 'sha1' in algoritmos_seleccionados:
        fieldnames.append('sha1')
    if 'sha256' in algoritmos_seleccionados:
        fieldnames.append('sha256')

    # Escribir las filas en el archivo CSV solo con los valores correspondientes a los algoritmos seleccionados
    output_path = os.path.join(folder_path, 'hashes.csv')
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fileWithHashes in hashes:
            row = {'filename': fileWithHashes['filename']}
            if 'md5' in algoritmos_seleccionados:
                row['md5'] = fileWithHashes['md5']
            if 'sha1' in algoritmos_seleccionados:
                row['sha1'] = fileWithHashes['sha1']
            if 'sha256' in algoritmos_seleccionados:
                row['sha256'] = fileWithHashes['sha256']
            writer.writerow(row)

    messagebox.showinfo("Ejecución completada", f"Se ha creado el archivo CSV en: {output_path}")

# Función para seleccionar carpeta
def seleccionar_carpeta():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Hash-Magician")
root.iconbitmap('mago.ico')


# Variables de control para los valores de los widgets
folder_path_var = tk.StringVar()
values = {
    '-MD5-': tk.BooleanVar(value=True),
    '-SHA1-': tk.BooleanVar(value=True),
    '-SHA256-': tk.BooleanVar(value=True),
    '-UPPER-': tk.BooleanVar(value=False),
}

# Widgets
ttk.Label(root, text="Seleccionar carpeta objetivo:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
ttk.Entry(root, textvariable=folder_path_var, width=40, state='readonly').grid(row=0, column=1, padx=10, pady=10)
ttk.Button(root, text="Buscar...", command=seleccionar_carpeta).grid(row=0, column=2, padx=10, pady=10)

ttk.Label(root, text="Seleccionar algoritmos hash a utilizar:").grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)
ttk.Checkbutton(root, text="MD5", variable=values['-MD5-']).grid(row=2, column=0, sticky='w', padx=20)
ttk.Checkbutton(root, text="SHA1", variable=values['-SHA1-']).grid(row=2, column=1, sticky='w')
ttk.Checkbutton(root, text="SHA256", variable=values['-SHA256-']).grid(row=2, column=2, sticky='w')

ttk.Checkbutton(root, text="Mayúsculas", variable=values['-UPPER-']).grid(row=3, column=0, columnspan=2, sticky='w', padx=20, pady=10)

ttk.Button(root, text="Iniciar", command=iniciar).grid(row=4, column=1, pady=10)
ttk.Button(root, text="Cancelar", command=root.quit).grid(row=4, column=2, pady=10)

root.mainloop()

# Un saludo para la clase de Ingeniería de Software.                                                                                                                                             Eh?