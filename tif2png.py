import glob
import shutil
import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def convert_folder(folder_path):
    # Obter lista de arquivos TIFF na pasta selecionada
    tif_files = glob.glob(f'{folder_path}/*.tif')
    num_files = len(tif_files)

    # Desabilitar botão e campo de seleção de pasta durante a conversão
    if (not HEADLESS):
        folder_button.config(state=tk.DISABLED)
        folder_entry.config(state=tk.DISABLED)

    # Exibir animação de "loading"
        loading_label = tk.Label(root, text='Converting...', font=('Helvetica', 16, 'bold'))
        loading_label.pack(pady=20)

    # Renomear arquivos substituindo espaços em branco por underscores
    for i, filename in enumerate(tif_files):
        new_filename = filename.replace(' ', '_')
        pathlib.Path(filename).rename(new_filename)

    # Converter arquivos TIFF em PNG
    for i, filename in enumerate(tif_files):
        png_filename = pathlib.Path(filename).with_suffix('.png')
        shutil.move(filename, png_filename)

    # Mover arquivos PNG para a pasta original selecionada
    for i, filename in enumerate(glob.glob(f'{folder_path}/*.png')):
        shutil.move(filename, pathlib.Path(folder_path) / pathlib.Path(filename).name)

    if (not HEADLESS):
        # Remover animação de "loading" e exibir mensagem de sucesso
        loading_label.pack_forget()
        messagebox.showinfo('Conversão Concluída', 'A conversão de arquivos foi concluída com sucesso.')
        root.destroy()


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)
        convert_folder(folder_path)

HEADLESS = False

if len(sys.argv) == 1:
    root = tk.Tk()
    root.title('CAIO - Conversor de Arquivos Instantaneo e Organizado')
    root.geometry('400x200')

    folder_path_var = tk.StringVar()

    folder_label = tk.Label(root, text='Selecione a pasta contendo os arquivos TIF:')
    folder_label.pack(pady=10)

    folder_frame = tk.Frame(root)
    folder_frame.pack()

    folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var, width=30)
    folder_entry.pack(side=tk.LEFT)

    folder_button = tk.Button(folder_frame, text='Selecionar', command=browse_folder)
    folder_button.pack(side=tk.LEFT, padx=10)
    root.mainloop()
else:
    HEADLESS = True
    print("You are running headless, if you want a GUI run without argument")
    if len(sys.argv) > 2:
        print("Use the folder path as the only argument")
    else:
        convert_folder(sys.argv[1])