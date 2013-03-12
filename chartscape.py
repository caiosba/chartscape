#!/usr/bin/env python
'''
Copyright (C) 2008 Caio Almeida, dcc.ufba.br

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''
import math, inkex, simplestyle

class statisticsGraph(inkex.Effect):
	# Just gets parameters
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("-t", "--title",
			action="store", type="string",
			dest="title", default="Statistics Graph",
			help="Title of the graph")
		self.OptionParser.add_option("-v", "--values",
			action="store", type="string",
			dest="values", default="10 15 25 50",
			help="Values to be represented on the graph (separated by spaces)")
		self.OptionParser.add_option("-s", "--size",
			action="store", type="float",
			dest="size", default=500.00,
			help="Size of the graph")
	
	def effect(self):
		
		# Gets values as an array of strings
		values = self.options.values.split(' ')
		
		# Dimensions based on the size parameter
		size = self.options.size
		center = size/2
		r = center*0.6
		text_size = size*0.05
		arcs_dist = size*0.004
		min_stroke = size*0.002
		label_size = size*0.03
		
		# This group will enrol everything
		svg = self.document.getroot()
		container = inkex.etree.SubElement(svg, 'g')
		container.set(inkex.addNS('id'), 'container')
		
		# Creates the border
		border_style = {
			'fill'         : 'white',
			'stroke'       : 'black',
			'stroke-width' : str(min_stroke)	
		}
		border = inkex.etree.SubElement(svg, 'rect')
		border.set('id','border')
		border.set('x','0')
		border.set('y','0')
		border.set('width',str(size*1.4))
		border.set('height',str(size))
		border.set('style',simplestyle.formatStyle(border_style))
		container.append(border)
		
		# Creates the title
		textStyle = {
			'font-size'   : str(text_size),
			'font-family' : 'sans-serif',
			'text-anchor' : 'middle',
			'fill'        : 'black'
		}
		title = inkex.etree.SubElement(svg, 'text')
		title.set('id','title')
		title.set('x',str(size*0.7))
		title.set('y',str(center*0.2))
		title.set('style',simplestyle.formatStyle(textStyle))
		title.text = self.options.title
		container.append(title)
		
		# Creates the graph group
		graph = inkex.etree.SubElement(svg, 'g')
		graph.set('id','graph')
		
		# Creates group to join labels
		arc_labels = inkex.etree.SubElement(svg, 'g')
		
		# Graph background circle, works like a shadow
		shadow_style = {
			'fill'         : 'gray',
			'stroke'       : 'black',
			'stroke-width' : str(min_stroke),
			'opacity'      : '0.4'	
		}
		shadow = inkex.etree.SubElement(svg, 'circle')
		shadow.set('id','shadow')
		shadow.set('cx',str(center))
		shadow.set('cy',str(center))
		shadow.set('r',str(r + size/100))
		shadow.set('style',simplestyle.formatStyle(shadow_style))
		graph.append(shadow)
		
		# Creates the legend group
		legend = inkex.etree.SubElement(svg, 'g')
		legend.set('id','legend')
		
		# Legend box
		legend_style = {
			'fill'         : 'white',
			'stroke'       : 'gray',
			'stroke-width' : str(min_stroke)
		}
		legend_box = inkex.etree.SubElement(svg, 'rect')
		legend_box.set('id','legend_box')
		legend_box.set('width',str(size*0.2))
		legend_box.set('x',str(size*0.9))
		legend_box.set('y',str(size*0.2))
		legend_box.set('ry',str(size*0.02))
		legend_box.set('style',simplestyle.formatStyle(legend_style))
		legend.append(legend_box)
		
		# Color themes
		theme = 'blue'
		colors = {
			'blue'     : [ '#216778', '#2C89A0', '#37ABC8', '#5FBCD3', '#CFDCE6', '#406480', '#507EA1', '#00487D' ],
			'orange'   : [ '#c50404', '#af7704', '#f6d295', '#d9bb7a', '#f44800', '#fb8b00', '#eec73e', '#f0a513' ]
		}

		# We need to store previous values to generate a new arc
		previous = { 
			'per' : 0,
			'x'   : 0,
			'y'   : 0
		}

		n = 0 			# Just a counter
		big = 0			# Only one arc can have more than 180 degrees, so we must know if it has occoured 
		longest = 0		# Stores the width of the longest absolute value string to calculate the legend box width

		# Calculates the total
		total = 0		
		for i in values:
			total += int(i)
		
		# Iterates with each value by creating an arc
		antx = anty = 0
		for value in values:
			arc_style = {
				'stroke'          : 'white',
				'stroke-width'    : str(arcs_dist)+'px',
				'stroke-linecap'  : 'round',
				'stroke-linejoin' : 'round'
			}
			
			arc = inkex.etree.SubElement(svg, 'path')
			
			# Calculates the arc data and sets the path element - here the magic happens! ;-)
			if antx == 0 and anty == 0:
				antx = center
				anty = center-r
			else:
				antx = previous['x']
				anty = previous['y']
			value = float(value)
			abs_per = 100*value/total
			arc_case = "0,1"
			rel_per = abs_per
			if abs_per < 50:
				rel_per = abs_per + previous['per']
				previous['per'] += abs_per
			angle = rel_per*3.6 - 90
			if abs_per >= 50: 
				angle = 180 - angle
				if not big:
					arc_case = "1,0"
					big = 1
			rad = math.radians(angle)
			x = center + r*math.cos(rad)	
			y = center + r*math.sin(rad)
			d = "M%f,%f " % (center,center)
			if previous['x'] == 0 or abs_per >= 50: d += "v-%f " % (r)
			else: d += "L%f,%f " % (previous['x'], previous['y'])
			if abs_per < 50:
				previous['x'] = x
				previous['y'] = y
			d += "A%f,%f 0 %s %f,%f z" % (r,r,arc_case,x,y)

			arc.set('d',d)
			
			# Ugly hack for 100%
			if abs_per == 100:
				arc = inkex.etree.SubElement(svg, 'circle')
				arc.set('r',str(r))
				arc.set('cx',str(center))
				arc.set('cy',str(center))
	
			# Sets other attributes of the arc and inserts it in the graph
			color = colors[theme].pop()
			arc.set('fill',color)
			arc.set('id','arc'+str(n))
			arc.set('style',simplestyle.formatStyle(arc_style))
			graph.append(arc)

			# Puts percentage around the arc
			arc_label_style = {
				'font-size' : str(label_size*1.2)+'px',
				'font-family' : 'sans-serif',
				'fill' : '#000'
			}
			arc_label = inkex.etree.SubElement(svg, 'text')
			arc_label.set('id','arc_label'+str(n))
			mpoint_x = (x+antx)/2
			mpoint_y = (y+anty)/2
			module = math.sqrt((mpoint_x-center)**2+(mpoint_y-center)**2)
			rvector_x = r*1.1*(mpoint_x-center)/module
			rvector_y = r*1.1*(mpoint_y-center)/module
			if abs_per < 50:
				arc_label.set('x',str(rvector_x+center))
				arc_label.set('y',str(rvector_y+center))
			else:
				arc_label.set('x',str(center-rvector_x*1.2))
				arc_label.set('y',str(center-rvector_y*1.2))
			arc_label.text = str(int(round(abs_per))) + '%'
			arc_label.set('style',simplestyle.formatStyle(arc_label_style))
			arc_labels.append(arc_label)
	
			# Creates the cell in the legend with the same color
			cell = inkex.etree.SubElement(svg, 'rect')
			cell.set('id','cell'+str(n))
			cell.set('width',str(size*0.09))
			cell.set('height',str(size*0.04))
			cell.set('x',str(size*0.91))
			cell.set('y',str(size*0.21+n*size*0.052))
			cell.set('ry',str(size*0.015))
			cell.set('fill',color)
			legend.append(cell)
			
			# Calculates legend row vertical position
			h = size*0.242+n*size*0.052
			
			# Creates the first label (which represents percentage value)
			label_rel_style = {
				'font-size' : str(label_size)+'px',
				'font-family' : 'sans-serif',
				'fill' : color
			}
			label_rel = inkex.etree.SubElement(svg, 'text')
			label_rel.set('id','label_rel'+str(n))
			label_rel.set('x',str(size*1.012))
			label_rel.set('y',str(h))
			label_rel.set('style',simplestyle.formatStyle(label_rel_style))
			label_rel.text = str(int(round(abs_per)))+'%'
			legend.append(label_rel)
			
			# Creates the second label (which represents absolute value)
			label_abs_style = {
				'font-size' : str(label_size)+'px',
				'font-family' : 'sans-serif',
				'fill' : 'gray'
			}
			label_abs = inkex.etree.SubElement(svg, 'text')
			label_abs.set('id','label_abs'+str(n))
			label_abs.set('x',str(size*1.1))
			label_abs.set('y',str(h))
			label_abs.set('style',simplestyle.formatStyle(label_abs_style))
			label_abs.text = str(int(value))
			legend.append(label_abs)
			
			# Calculates legend box width and height
			legend_box.set('height',str(float(cell.get('y'))+float(cell.get('height'))*1.24-float(legend_box.get('y'))))
			width = len(str(int(value)))*label_size*0.74 + float(label_abs.get('x'))
			if width > longest: longest = width
			
			n+=1
			
		# The legend box width must fit the longest number
		legend_box.set('width',str(longest-float(legend_box.get('x'))))
		
		# The border must fit everything
		border.set('width',str(size+float(legend_box.get('width'))*1.1))
		
		# Finishes
		container.append(legend)
		container.append(graph)
		container.append(arc_labels)
		svg.append(container)

# Applies the effect
e = statisticsGraph()
e.affect()
