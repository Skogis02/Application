from plotter import FunctionPlotter
import numpy as np

PI = np.pi


def f(x: np.ndarray) -> np.ndarray:
    return x**2


def g(x: np.ndarray) -> np.ndarray:
    return 3*PI*np.exp(5*np.sin(2*PI*x))

def h(x: np.ndarray) -> np.ndarray:
    return np.sin(2*PI*x)


plotter = FunctionPlotter(g, number_of_points=1000)
plotter.create_plot()
plotter.display()
