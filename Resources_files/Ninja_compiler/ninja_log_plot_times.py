import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
else:
    file_name = ".ninja_log"

with open(file_name,'r') as ninja_file:
    lines = ninja_file.readlines()

# removing trailing newline AND whitespaces than can mess with the comparison
lines = [line.rstrip() for line in lines]

lines = lines[1:-1]

all_times = []
all_times.append(0.0)
for line in lines:
    if len(line) > 0:
        splitted = line.split('\t')
        all_times.append(float(splitted[1])/1000)

counter = 0
total_times = {}
names = {}
for line in lines:
    if len(line) > 0:
        splitted = line.split('\t')

        long_name_strings = splitted[3]
        split_names = long_name_strings.split('/')

        root = split_names[0]
        if root == "kratos" and len(split_names) > 3:
            category = split_names[3]
        else:
            category = root
        if not category in names:
            names[category] = []
            total_times[category] = []
        names[category].append(split_names[-1])
        partial_time = float(splitted[1])/1000 - all_times[counter]
        total_times[category].append(partial_time)
        counter += 1

times = total_times.copy()
sum_time = []
for key, value in times.items():
    np.asarray(value)
    sum_time.append(sum(value))

np.asarray(sum_time)

fig, ax = plt.subplots()

data = sum_time
categories = names.keys()

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} s)".format(pct, absolute)

wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, categories,
          title="Compilation parts",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
ax.set(aspect="equal", title='Compilation time. Total = '+ str(sum(sum_time)/60) +' min')
plt.show()

# TODO: Nested https://matplotlib.org/gallery/pie_and_polar_charts/nested_pie.html#sphx-glr-gallery-pie-and-polar-charts-nested-pie-py
#cmap = plt.get_cmap("tab20c")
#outer_colors = cmap(np.arange(3)*4)
#inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

#size = 0.

#ax.pie(times.sum(axis=1), radius=1, colors=outer_colors,
       #wedgeprops=dict(width=size, edgecolor='w'))

#ax.pie(times.flatten(), radius=1-size, colors=inner_colors,
       #wedgeprops=dict(width=size, edgecolor='w'))

# save
fig.savefig( file_name + '.png', dpi=fig.dpi)
