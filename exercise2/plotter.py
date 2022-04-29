import matplotlib.pyplot as plt
import matplotlib.widgets as widget
import numpy as np
from typing import Union, Callable

PI = np.pi


class FunctionPlotter:
    def __init__(self, function: Callable, lower_bound: float = -2, upper_bound: float = 2,
                 number_of_points: int = 100, width: float = 15, height: float = 9,
                 name: str = "My Plot", read_from: str = 'data_in.csv', write_to: str = 'data_out.csv'):

        # Plotting
        self.function = function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.number_of_points = number_of_points
        self.width = width
        self.height = height
        self.name = name
        self.read_from = read_from
        self.write_to = write_to
        self.xdata = None
        self.ydata = None
        self.fig = None

        # Fast Fourier Transform

        self.x_width = self.upper_bound - self.lower_bound
        self.sample_frequency = self.number_of_points/self.x_width
        self.sample_period = 1/self.sample_frequency
        self.fft_frequencies = None
        self.fft_amplitudes = None


    # Hidden Methods:
    def __generate_figure(self):
        if self.fig is None:
            # Layout and Design
            self.fig = plt.figure(num=0, figsize=(self.width, self.height))
            self.ax_graph = plt.subplot2grid(shape=(5, 5), loc=(0, 0), rowspan=3, colspan=3)
            self.ax_fft = plt.subplot2grid(shape=(5, 5), loc=(3, 0), rowspan=2, colspan=3)
            self.ax_name = plt.subplot2grid(shape=(10, 15), loc=(2, 10), rowspan=1, colspan=3)
            self.ax_lower_bound = plt.subplot2grid(shape=(10, 15), loc=(0, 10), rowspan=1, colspan=3)
            self.ax_upper_bound = plt.subplot2grid(shape=(10, 15), loc=(1, 10), rowspan=1, colspan=3)
            self.ax_read_from = plt.subplot2grid(shape=(10, 15), loc=(3, 10), rowspan=1, colspan=3)
            self.ax_write_to = plt.subplot2grid(shape=(10, 15), loc=(4, 10), rowspan=1, colspan=3)
            self.ax_read_button = plt.subplot2grid(shape=(10, 15), loc=(3, 13), rowspan=1, colspan=3)
            self.ax_write_button = plt.subplot2grid(shape=(10, 15), loc=(4, 13), rowspan=1, colspan=3)

            self.ax_graph.set_title('Plotter')
            self.ax_fft.set_title('Frequency Domain')
            self.ax_fft.grid()
            self.ax_graph.grid()
            plt.tight_layout()

            # Functionality
            self.lower_bound_textbox = widget.TextBox(ax=self.ax_lower_bound,
                                                      label='Lower Bound: ', initial=str(self.lower_bound))
            self.upper_bound_textbox = widget.TextBox(ax=self.ax_upper_bound,
                                                      label='Upper Bound: ', initial=str(self.upper_bound))
            self.name_textbox = widget.TextBox(ax=self.ax_name, label='Name: ', initial=self.name)
            self.read_textbox = widget.TextBox(ax=self.ax_read_from, label='Read from: ', initial=self.read_from)
            self.write_textbox = widget.TextBox(ax=self.ax_write_to, label='Write to: ', initial=self.write_to)
            self.read_button = widget.Button(ax=self.ax_read_button, label='Read')
            self.write_button = widget.Button(ax=self.ax_write_button, label='Write')

            self.lower_bound_textbox.on_submit(self.update_from_all)
            self.upper_bound_textbox.on_submit(self.update_from_all)
            self.name_textbox.on_submit(self.update_from_all)
            self.read_textbox.on_submit(self.change_read_file)
            self.write_textbox.on_submit(self.change_write_file)
            self.read_button.on_clicked(self.read_from_csv)
            self.write_button.on_clicked(self.write_to_csv)

    def __generate_xdata(self):
        self.xdata = np.linspace(self.lower_bound, self.upper_bound, self.number_of_points)

    def __get_xdata(self) -> np.ndarray:
        if self.xdata is None:
            self.__generate_xdata()
        return self.xdata

    def __generate_ydata(self):
        self.ydata = self.function(self.__get_xdata())

    def __get_ydata(self) -> np.ndarray:
        if self.ydata is None:
            self.__generate_ydata()
        return self.ydata

    def __generate_fft_frequencies(self):
        fft_frequencies = np.fft.fftfreq(self.number_of_points, d=self.sample_period)
        self.fft_frequencies = np.split(fft_frequencies, 2)[0]   # keeps only positive frequency data

    def __get_fft_frequencies(self) -> np.ndarray:
        if self.fft_frequencies is None:
            self.__generate_fft_frequencies()
        return self.fft_frequencies

    def __generate_fft_amplitudes(self):
        fft_result_complex = np.fft.fft(self.__get_ydata())     # runs Fast Fourier Transform on current ydata
        fft_result_magnitudes = np.abs(fft_result_complex)/self.number_of_points    # gets magnitudes and normalizes
        self.fft_amplitudes = 2*np.split(fft_result_magnitudes, 2)[0]     # keeps only positive frequency data

    def __get_fft_amplitudes(self) -> np.ndarray:

        if self.fft_amplitudes is None:
            self.__generate_fft_amplitudes()
        return self.fft_amplitudes

    # Data Methods:
    def update_data(self):
        self.__generate_xdata()
        self.__generate_ydata()

    def change_read_file(self, read_file):
        self.read_from = read_file

    def change_write_file(self, write_file):
        self.write_to = write_file

    def change_function(self, new_function: Callable):
        self.function = new_function

    def find_freq(self) -> Union[None, list[float]]:
        raise NotImplementedError("Yet to be implemented!")

    def read_from_csv(self, *args):
        with open(self.read_from, 'r') as csv_file:
            for line in csv_file:
                pass
            name = line.split('# ')[-1].strip()
        [xdata, ydata] = np.genfromtxt(self.read_from, delimiter=',', comments='#').T
        lower_bound = xdata[0]
        upper_bound = xdata[-1]
        self.update_to_textboxes(name, lower_bound, upper_bound)
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.xdata = xdata
        self.ydata = ydata
        self.update_graph()

    def write_to_csv(self, *args):
        data = np.vstack((self.xdata, self.ydata)).T
        np.savetxt(self.write_to, data, delimiter=',', header='x,y', footer=self.name)

    # Visualizing Methods
    def create_plot(self):
        self.__generate_figure()
        self.ax_graph.plot(self.__get_xdata(), self.__get_ydata())
        self.ax_fft.plot(self.__get_fft_frequencies(), self.__get_fft_amplitudes())

    def display(self):
        plt.show()

    def update_graph(self):
        self.ax_fft.clear()
        self.ax_fft.grid()
        self.ax_graph.clear()
        self.ax_graph.grid()
        self.create_plot()
        plt.draw()

    def update_from_textboxes(self):
        self.name = self.name_textbox.text
        self.lower_bound = float(self.lower_bound_textbox.text)
        self.upper_bound = float(self.upper_bound_textbox.text)

    def update_to_textboxes(self, name, lower_bound, upper_bound):
        self.name_textbox.set_val(name)
        self.lower_bound_textbox.set_val(str(lower_bound))
        self.upper_bound_textbox.set_val(str(upper_bound))

    def update_from_all(self, *args):
        self.update_from_textboxes()
        self.update_data()
        self.update_graph()

    def close(self):
        plt.close()
