import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import math
import csv

matplotlib.use('TkAgg')

# Equations' settings
t = 0
delta_time = 1
g = 9.81
v0 = 0
angle_a = 0
hauteur = 0

# Equations' functions
def vx(t):
    return v0*math.cos(math.radians(angle_a))

def vy(t):
    return -g*t+v0*math.sin(math.radians(angle_a))

def omx(t):
    return (float(v0)*math.cos(math.radians(float(angle_a))))*t

def omy(t):
    return -0.5*g*(t**2)+(float(v0)*math.sin(math.radians(float(angle_a))))*t+float(hauteur)

# Specifications' equations
def delta(a, b, c=0):
    return b**2-4*float(a)*float(c)

def x_1(a, b, d):
    return ((-b-math.sqrt(d))/(2*a))

def x_2(a, b, d):
    return ((-b+math.sqrt(d))/(2*a))

def x_0(a, b):
    return -b/(2*a)

# Create, show and delete graph 1st graph
def create_plot_1():
    global t_range
    global x
    global y
    x = [0]
    y = [0]
    t_range = []
    t = 0
    while y[len(y)-1] >= 0:
        x.append(omx(t))
        y.append(omy(t))
        t_range.append(float(t))
        t += float(delta_time)
    del x[0]
    del y[0]
    fig, axs = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.33)
    axs[0].plot(x, y)
    axs[0].scatter(x, y)
    axs[0].grid()
    axs[0].set_xlabel('Distance (m)')
    axs[0].set_ylabel('Altitude (m)')
    axs[1].scatter(t_range, y)
    axs[1].grid()
    axs[1].set_xlabel('Temps (s)')
    axs[1].set_ylabel('Altitude (m)')
    return fig

def draw_figure_1(canvas):
   tkcanvas = FigureCanvasTkAgg(create_plot_1(), canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)
   return tkcanvas

# Delete all graphs
def delete_fig_agg(tkcanvas):
    tkcanvas.get_tk_widget().forget()
    plt.close('all')

# Create a .csv file which save the data
def export_csv(t, x, y):
    data = [t, x, y]
    with open("export_"+v0+"_"+angle_a+"_"+hauteur+"_"+delta_time+".csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def extract_graph():
    plt.show()

# Functions that calculate the specifications of the movement
def caracteristiques_temps_hf():
    d = delta(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), hauteur)
    if d > 0:
        x1 = x_1(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), d)
        if x1 >= 0:
            window['-FALLTIME-'].update(round(x1, 2))
        else:
            x2 = x_2(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), d)
            window['-FALLTIME-'].update(x2)
    if d == 0:
        x = x_0(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))))
        window['-FALLTIME-'].update(x)

def altitude_maximum():
    t_max = (float(v0)*math.sin(math.radians(float(angle_a))))/g
    window['-MAXALT-'].update(round(omy(t_max), 2))

def zeros():
    d = delta(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), hauteur)
    if d > 0:
        x1 = x_1(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), d)
        if x1 >= 0:
            window['-DIST-'].update(round(omx(x1), 2))
        else:
            x2 = x_2(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))), d)
            window['-DIST-'].update(round(omx(x2), 2))
    if d == 0:
        x = x_0(-0.5*g, float(v0)*math.sin(math.radians(float(angle_a))))
        window['-DIST-'].update(round(omx(x), 2))

# Create program's layout
input_layout = [[sg.Text('Données', font='Arial 15')],
                [sg.Text('V0 (m/s): ', ), sg.Push(), sg.Input('0', size=6, key='-V0INPUT-')],
                [sg.Text('Angle a (°): '), sg.Push(), sg.Input('0', size=6, key='-AINPUT-')],
                [sg.Text('Hauteur (m):'), sg.Push(), sg.Input('0', size=6, key='-HINPUT-')],
                [sg.Text('Delta Temps (s):'), sg.Push(), sg.Input('1', size=6, key='-DTEMPS-')],
                [sg.Push(), sg.Button('Tracer', key='-BUTTON-')],
                [sg.HSep()],
                [sg.Text('Caractéristiques', font='Arial 15')],
                [sg.Text('Distance Parcourue (m)'), sg.Push(), sg.Text('', key='-DIST-')],
                [sg.Text('Altitude Maximale (m)'), sg.Push(), sg.Text('', key='-MAXALT-')],
                [sg.Text('Temps de Chute (s)'), sg.Push(), sg.Text('', key='-FALLTIME-')]]

graph_layout = [[sg.Push(), sg.Text('Vecteurs Position', font='Arial 15'), sg.Push()],
                [sg.Canvas(key='-CANVAS1-')]]

menu_def = [['Fichier', ['Quitter']], 
            ['Données', ['Exporter en CSV', 'Fenêtre spécialisée']]]

layout = [[sg.MenuBar(menu_def, font='Helvetica 9')],
          [sg.Column(layout=input_layout), sg.VerticalSeparator(), sg.Column(layout=graph_layout)]]

# Initiate the window
window = sg.Window('Trajectoire Chute Libre - Référentiel Galiléen - Frottements Négligés', layout, finalize=True, resizable=True, element_justification='center', font='Arial 13')

tkcanvas = draw_figure_1(window['-CANVAS1-'].TKCanvas)
caracteristiques_temps_hf()
altitude_maximum()
zeros()

# Events loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quitter':
        break
    if event == '-BUTTON-':
        v0 = values['-V0INPUT-']
        angle_a = values['-AINPUT-']
        hauteur = values['-HINPUT-']
        delta_time = values['-DTEMPS-']
        if tkcanvas is not None:
            delete_fig_agg(tkcanvas)
        tkcanvas = draw_figure_1(window['-CANVAS1-'].TKCanvas)
        caracteristiques_temps_hf()
        altitude_maximum()
        zeros()
    if event == 'Exporter en CSV':
        export_csv(t_range, x, y)
    if event == 'Fenêtre spécialisée':
        extract_graph()
window.close()