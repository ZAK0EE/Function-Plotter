import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast
# VARS CONSTS:
_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False,
         }

# Plot grid theme
plt.style.use('seaborn-whitegrid')

# GUI customization
AppFont = 'Any 16'
sg.theme('Reddit')

# GUI layout
layout = [[sg.Canvas(key='figCanvas', background_color='#FFFFFF')],
          [sg.Text(text="Please input your equation as a function of x:", font=AppFont)],
          [sg.InputText(font=AppFont, background_color='#FCFCFC'), sg.Button('Plot', font=AppFont)],
          [sg.Text(text="Min value:", font=AppFont), sg.InputText(size=(10, 1), background_color='#FCFCFC'),
           sg.Text(text="Max value:", font=AppFont),
           sg.InputText(size=(10, 1), background_color='#FCFCFC')],
          [sg.Button('Exit', font=AppFont), sg.Text(text="", font='Any 13', key='-ERROR-', text_color='#F44336')]
          ]

# Window initialization and customization
_VARS['window'] = sg.Window('Function Plotter',
                            layout,
                            finalize=True,
                            location=(100, 100),
                            element_justification="left",
                            background_color='#FFFFFF', enable_close_attempted_event=True)





def VerifyMinMax(min, max):
    # Initializations.
    Isgood = True
    GuiError = ""
    MaximumVal = 999999
    # Check if string of min or max is empty
    if not min or not max:
        GuiError = "[ERROR]Minimum and maximum values must not be empty"
        Isgood = False
    # Check if all the string is decimal
    # Replacing "." for solving real numbers problem
    # Left stripping '-' for solving negative numbers problem.
    elif not min.replace(".", "", 1).lstrip('-').isdecimal() or not max.replace(".", "", 1).lstrip('-').isdecimal():
        GuiError = "[ERROR]Minimum and maximum values must be decimals only"
        Isgood = False
    # Range check
    elif float(min) > MaximumVal or float(max) > MaximumVal:
        GuiError = f"[ERROR]Minimum and maximum must not exceed {MaximumVal}"
        Isgood = False
    elif float(min) > float(max):
        GuiError = "[ERROR]Minimum must not exceed the maximum value"
        Isgood = False

    _VARS['window']['-ERROR-'].update(GuiError)
    return Isgood

def VerifyEqn(eqn):
    # Checks for all syntax errors.
    x = 1
    try:
        eval(eqn)
    except SyntaxError:
        _VARS['window']['-ERROR-'].update("[ERROR]Syntax error detected")
        return 0
    except ZeroDivisionError:
        _VARS['window']['-ERROR-'].update("[ERROR]Division by zero detected")
        return 0
    except NameError:
        _VARS['window']['-ERROR-'].update("[ERROR]Unknown characters detected")
        return 0  
    except:
        VARS['window']['-ERROR-'].update("[ERROR]Equation cannot be evaluated")
        return 0         
   
    # If x doesn't exist in the equation or it's empty.
    if eqn.find('x') == -1 or not eqn:
        _VARS['window']['-ERROR-'].update("[ERROR]The equation must be a function of x")
        return 0
    return 1
    
    
# Draws the plot
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
    
    
# Initializing plot canvas.
def InitPlot():
    _VARS['pltFig'] = plt.figure()
    plt.plot(0, 0, 'g')
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

# Update the plot using the new "eqn"
# min, max are x values
def UpdatePlot(eqn, min, max):

    eqn = eqn.replace("^", "**")
    if not VerifyEqn(eqn):
        return 0
    if not VerifyMinMax(min, max):
        return 0
    
    # Forget last canvas to ensure that there's only one canvas on the GUI
    _VARS['fig_agg'].get_tk_widget().forget()

    min = float(min)
    max = float(max)
    x = np.linspace(min, max)
    y = eval(eqn)

    plt.clf() # Clear the current plot.
    plt.plot(x, y, 'g') # Plot the new equation.
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig']) # Draw the new plot




InitPlot()
# MAIN LOOP
while True:
    event, values = _VARS['window'].read(timeout=200)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
            'Do you really want to exit?') == 'Yes':
        break
    elif event == "Plot":
        UpdatePlot(values[0], values[1], values[2])

_VARS['window'].close()
