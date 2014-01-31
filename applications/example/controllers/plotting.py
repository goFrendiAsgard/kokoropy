from kokoropy import template, request, draw_matplotlib_figure, Autoroute_Controller, load_view

class Default_Controller(Autoroute_Controller):
    
    def action_plot(self):
        max_range = 6.28
        if 'range' in request.GET:
            max_range = float(request.GET['range'])
        # import things
        import numpy as np
        from matplotlib.figure import Figure
        # determine x, sin(x) and cos(x)
        x = np.arange(0, max_range, 0.1)
        y1 = np.sin(x)
        y2 = np.cos(x)
        # make figure       
        fig = Figure()
        fig.subplots_adjust(hspace = 0.5, wspace = 0.5)
        fig.suptitle('The legendary sine and cosine curves')
        # first subplot
        ax = fig.add_subplot(2, 1, 1)
        ax.plot(x, y1, 'b')
        ax.plot(x, y1, 'ro')
        ax.set_title ('y = sin(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # second subplot
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x, y2, 'b')
        ax.plot(x, y2, 'ro')
        ax.set_title ('y = cos(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # make canvas
        return draw_matplotlib_figure(fig)
    
    def action_index(self):
        return load_view('example','plotting')