import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Jeamhowards Montiel - 1910234
# Constantes
X = 2
Y = 3
Z = 4

# Parámetros Algoritmo PSO
alpha_max = 0.7 # Inercia máxima
alpha_min = 0.3 # Inercia mínima
max_iter = 10 # Número máximo de iteraciones
num_particulas = 4 # Número de partículas
r_1 = 0.4  # Influencia del mejor personal
r_2 = 0.6  # Influencia del mejor global
a0 = 1.5 # Aceleración

# Inicialización con tipo de datos float64
x = np.array([[0, X+1], [Y+1, 0], [0, -X-1], [-Y-1, 0]], dtype=np.float64)
v = np.array([[0, (Z+1)/2], [(Z+1)/2, 0], [0, (Z+1)/2], [(Z+1)/2, 0]], dtype=np.float64)
x_star = x.copy()

def f(x):
    return x[0]**2 + x[1]**2  - 10*(np.cos(2*np.pi*x[0]) + np.cos(2*np.pi*x[1])) + 20

def a(t):
    return alpha_max - (alpha_max - alpha_min) * t / max_iter

f_x = np.array([f(x) for x in x])
x_g = x[np.argmin(f_x)].copy()

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 10))
# Color de las partículas
colores = ['r', 'g', 'b', 'y'] 
# Configuración de los ejes
range_xy = np.arange(-7, 7, 0.5)
ax.set_xticks(range_xy) 
ax.set_yticks(range_xy)
lns = [
    plt.plot(
        [], [], marker='o', color=colores[i], 
        label=(
            f'Partícula {i+1}\n'
            f'x : ({x[i][0]:.1f}, {x[i][1]:.1f})\n'
            f'v : ({v[i][0]:.1f}, {v[i][1]:.1f})\n'
            f'x*: ({x_star[i][0]:.1f}, {x_star[i][1]:.1f})'
        )
    )[0] 
    for i in range(num_particulas)
]
title = ax.text(0.5, 1.05, "", 
                bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, 
                transform=ax.transAxes, ha="center")

def init():
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.grid()
    ax.legend()
    print('-------- Inicialización --------')
    for i in range(num_particulas):
        print(f'Partícula {i+1}\n'
              f'x : ({x[i][0]:.1f}, {x[i][1]:.1f})\n'
              f'v : ({v[i][0]:.1f}, {v[i][1]:.1f})\n'
              f'x*: ({x_star[i][0]:.1f}, {x_star[i][1]:.1f})')
    for i in range_xy:
        ax.axvline(x=i, color='0.9')
        ax.axhline(y=i, color='0.9')
    ax.axhline(y=0, color='0.5')
    ax.axvline(x=0, color='0.5')
    ax.text(-7, 7.5, "Jeamhowards Montiel - 1910234")
    return lns 

def update(frame):
    global x, v, x_star, f_x, x_g
    if frame < max_iter:
        print(f'-------- Iteración {frame+1} --------')
    t = frame + 1
    leg = ax.get_legend()
    leg.remove()
    ax.legend()
    if frame == 0:
        title.set_text(f'Inicialización\nxg: ({x_g[0]:.1f}, {x_g[1]:.1f})')
    else:
        title.set_text(f'Iteración {frame}\nxg: ({x_g[0]:.1f}, {x_g[1]:.1f})')
    for i, ln in enumerate(lns):
        ln.set_data([x[i, 0]], [x[i, 1]])
        info = (
            f'Partícula {i+1}\n'
            f'x : ({x[i][0]:.1f}, {x[i][1]:.1f})\n'
            f'v : ({v[i][0]:.1f}, {v[i][1]:.1f})\n'
            f'x*: ({x_star[i][0]:.1f}, {x_star[i][1]:.1f})'
        )
        ln.set_label(info)
        ln.set_zorder(3)
    for j in range(num_particulas):
        # Actualizar velocidad y posición
        v[j] = a(t)*v[j] + a0 * (r_1 * (x_star[j] - x[j]) + r_2 * (x_g - x[j]))
        x[j] += v[j]
        # Evaluar la función objetivo
        f_x_j = f(x[j])
        # Actualizar el valor de x* y xg si es necesario
        if f_x_j < f_x[j]:
            x_star[j] = x[j]
            f_x[j] = f_x_j
        if f_x_j < f(x_g):
            x_g = x[j].copy()
        if frame < max_iter:
            print(
                f'Partícula {j+1}\n'
                f'x : ({x[j][0]:.1f}, {x[j][1]:.1f})\n'
                f'v : ({v[j][0]:.1f}, {v[j][1]:.1f})\n'
                f'x*: ({x_star[j][0]:.1f}, {x_star[j][1]:.1f})'
            )
    if frame < max_iter:
        print(f'xg: ({x_g[0]:.1f}, {x_g[1]:.1f})')
    return lns + [title]
    
# Crear la animación
ani = FuncAnimation(fig, update, frames=range(max_iter+1), 
                    init_func=init, blit=True, interval=3000, repeat=False)

# Guardar la animación en un archivo GIF
ani.save('pso.gif', writer='imagemagick', fps=0.6)