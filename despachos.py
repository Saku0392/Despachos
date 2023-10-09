from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

def crear_base():
    con = sqlite3.connect('despachos.db')
    return con
crear_base()

def crear_tabla():
    con = crear_base()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_transporte varchar(128) NOT NULL,
            cliente varchar(128) NOT NULL,
            localidad varchar(128) NOT NULL, 
            transporte varchar(128) NOT NULL, 
            precio int(7),
            bultos int(7)
            );
            """
    cursor.execute(sql)
    con.commit()
crear_tabla()

def grabar():
    cadena_cliente = var_cliente.get()
    patron_cliente = "^[A-Za-z áéíóú]*$"
    cadena_localidad = var_localidad.get()
    patron_localidad = "^[A-Za-z áéíóú]*$"
    if(re.match(patron_cliente, cadena_cliente) and re.match(patron_localidad, cadena_localidad)):
        con = crear_base()
        cursor = con.cursor()
        data = (var_tipo_transp.get(), var_cliente.get(), var_localidad.get(), var_transporte.get(), var_precio.get(), var_bultos.get())
        sql = """INSERT INTO envios(tipo_transporte, cliente, localidad, transporte, precio, bultos) 
                VALUES (?, ?, ?, ?, ?, ?)
                """
        cursor.execute(sql, data)
        con.commit()
        actualizar_vista()
        limpiar_campos()
    else:
        print("Hay un error")
    calcular_tot()

def borrar():
    for tr in [tree, tree2]:
        valor = tr.selection()
        item = tr.item(valor)
        mi_id = item['text']
        con = crear_base()
        cursor=con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM envios WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
    actualizar_vista()
    calcular_tot()

def calcular_tot():
    con = crear_base()
    cursor = con.cursor()
    sql_terminal = "SELECT SUM(precio*bultos) FROM envios WHERE tipo_transporte='Terminal';"
    cursor.execute(sql_terminal)
    total_terminal = cursor.fetchone()[0] or 0
    sql_privado = "SELECT SUM(precio*bultos) FROM envios WHERE tipo_transporte='Privado';"
    cursor.execute(sql_privado)
    total_privado = cursor.fetchone()[0] or 0
    var_tot1.set(total_terminal)
    var_tot2.set(total_privado)
    con.commit()

def limpiar():
    if askyesno("Esta a punto de borrar todos los registros de la base", "Desea limpiar?"):
        con = crear_base()
        cursor = con.cursor()
        sql = "DELETE FROM envios"
        cursor.execute(sql)
        con.commit()
        actualizar_vista()
        limpiar_campos()
        showinfo("Si", "Limpiado con exito")
    else: 
        showinfo("No", "Esta a punto de salir")
    calcular_tot()

def actualizar_treeview(tr, tipo):
    records = tr.get_children()
    for element in records:
        tr.delete(element)
    sql = f"SELECT * FROM envios WHERE tipo_transporte = '{tipo}' ORDER BY id ASC"
    con=crear_base()
    cursor=con.cursor()
    datos=cursor.execute(sql)
    resultado = datos.fetchall()
    for fila in resultado:
        tr.insert("", "end", text=fila[0], values=(fila[2], fila[3], fila[4], fila[5], fila[6], fila[5]*fila[6]))

def actualizar_vista():
    actualizar_treeview(tree, 'Terminal')
    actualizar_treeview(tree2, 'Privado')

def limpiar_campos():
    var_tipo_transp.set('')
    var_cliente.set('')
    var_localidad.set('')
    var_transporte.set('')
    var_precio.set('0.0')
    var_bultos.set('0')

master = Tk()
style = ttk.Style(master)
style.theme_use("clam")

master.title("Despacho de pedidos")
        
titulo = Label(
    master, 
    text="Ingrese los datos de despacho del pedido", 
    bg="midnightblue", 
    fg="white", 
    height=1, 
    width=60, 
    font=("tahoma", 11, "bold"))
titulo.grid(row=0, column=0, columnspan=25, padx=1, pady=1, sticky=W+E)


tipo_transporte = Label(master, text="Tipo de transporte:")
tipo_transporte.grid(row=1, column=4, sticky=W)
cliente = Label(master, text='Cliente') 
cliente.grid(row=2, column=4, sticky=W)
localidad = Label(master, text='Localidad') 
localidad.grid(row=3, column=4, sticky=W)
transporte = Label(master, text='Transporte') 
transporte.grid(row=4, column=4, sticky=W)
precio = Label(master, text='Precio')
precio.grid(row=5, column=4, sticky=W)
bultos = Label(master, text='Bultos')
bultos.grid(row=6, column=4, sticky=W)
tit_tree = Label(master, text="POR TERMINAL:")
tit_tree.grid(row=8, column=4, sticky=W)
tit_tree2 = Label(master, text="TRANSP PRIVADO:")
tit_tree2.grid(row=8, column=10, sticky=W)
tot_tree = Label(master, text="TOTAL")
tot_tree.grid(row=22, column=4, sticky=W)
tot_tree2 = Label(master, text="TOTAL")
tot_tree2.grid(row=22, column=10, sticky=W)

var_tipo_transp = StringVar()
var_bultos = IntVar()
var_cliente = StringVar()
var_transporte = StringVar()
var_localidad = StringVar()
var_precio = DoubleVar()
var_tot1 = DoubleVar()
var_tot2 = DoubleVar()

combo_transporte = ttk.Combobox(
    state='readonly',
    values=['Terminal', 'Privado'],
    textvariable=var_tipo_transp
)
combo_transporte.grid(row=1, column=5)
entry_cliente = Entry(master, textvariable=var_cliente, width=25)
entry_cliente.grid(row=2, column=5)
entry_localidad = Entry(master, textvariable=var_localidad, width=25)
entry_localidad.grid(row=3, column=5)
entry_transporte = Entry(master, textvariable=var_transporte, width=25)
entry_transporte.grid(row=4, column=5)
entry_precio = Entry(master, textvariable=var_precio, width=25)
entry_precio.grid(row=5, column=5)
entry_bultos = Entry(master, textvariable=var_bultos, width=25)
entry_bultos.grid(row=6, column=5)
label_total1 = Label(master, textvariable=var_tot1, width=25)
label_total1.grid(row=22, column=6)
label_total2 = Label(master, textvariable=var_tot2, width=25)
label_total2.grid(row=22, column=21)

tree = ttk.Treeview(master)
tree["columns"] = ("col1", "col2", "col3","col4","col5","col6")
tree.column("#0", width=0, minwidth=0, anchor=W)
tree.column("col1", width=110, minwidth=100, anchor=W)
tree.column("col2", width=110, minwidth=80, anchor=W)
tree.column("col3", width=90, minwidth=80, anchor=W)
tree.column("col4", width=50, minwidth=50, anchor=CENTER)
tree.column("col5", width=60, minwidth=50, anchor=CENTER)
tree.column("col6", width=90, minwidth=50, anchor=CENTER)
tree.heading("col1", text="CLIENTE", anchor=W)
tree.heading("col2", text="LOCALIDAD", anchor=W)
tree.heading("col3", text="TRANSPORTE", anchor=W)
tree.heading("col4", text="PRECIO", anchor=CENTER)
tree.heading("col5", text="BULTOS", anchor=CENTER)
tree.heading("col6", text="TOTAL", anchor=CENTER)

tree.grid(column=0, row=13, columnspan=10)

tree2 = ttk.Treeview(master)
tree2["columns"] = ("col8", "col9", "col10","col11","col12","col13")
tree2.column("#0", width=0, minwidth=0, anchor=W)
tree2.column("col8", width=110, minwidth=100, anchor=W)
tree2.column("col9", width=110, minwidth=80, anchor=W)
tree2.column("col10", width=90, minwidth=80, anchor=W)
tree2.column("col11", width=50, minwidth=50, anchor=CENTER)
tree2.column("col12", width=60, minwidth=50, anchor=CENTER)
tree2.column("col13", width=90, minwidth=50, anchor=CENTER)
tree2.heading("col8", text="CLIENTE", anchor=W)
tree2.heading("col9", text="LOCALIDAD", anchor=W)
tree2.heading("col10", text="TRANSPORTE", anchor=W)
tree2.heading("col11", text="PRECIO", anchor=CENTER)
tree2.heading("col12", text="BULTOS", anchor=CENTER)
tree2.heading("col13", text="TOTAL", anchor=CENTER)

tree2.grid(column=10, row=13, columnspan=12)

boton_agregar = Button(
    master, 
    text='AGREGAR', 
    bg="#132294", 
    fg="white", 
    height=1, 
    width=15, 
    font=("tahoma", 11, "bold"), 
    command=grabar)
boton_agregar.grid(row=1, column=10)

boton_borrar = Button(
    master, 
    text='BORRAR', 
    bg="#132294", 
    fg="white", 
    height=1, 
    width=15, 
    font=("tahoma", 11, "bold"), 
    command=borrar)
boton_borrar.grid(row=3, column=10)

boton_limpiar = Button(
    master, 
    text='LIMPIAR', 
    bg="#132294", 
    fg="white", 
    height=1, 
    width=15, 
    font=("tahoma", 11, "bold"), 
    command=limpiar)
boton_limpiar.grid(row=5, column=10)

actualizar_vista()
calcular_tot()
master.mainloop()