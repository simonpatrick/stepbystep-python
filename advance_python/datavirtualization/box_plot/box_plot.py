import pygal

box_plot = pygal.Box()
box_plot.title = 'Cost of Whole Milk in early 2014'
box_plot.add('US Dollars', [2.08, 3.14, 3.89, 3.91, 3.94, 3.98])
box_plot.add('Pound Sterling', [2.78, 3.84, 1.69, 4.71, 4.84, 4.92])


box_plot.render_to_file('box_plot.svg')
