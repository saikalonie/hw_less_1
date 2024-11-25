# Библеотека matplotlib, для создания графиков

from matplotlib import pyplot

months = ["January", "February", "March", "April", "May", "June"]
values = [1500, 2300, 5300, 8150, 6280, 5400]

pyplot.plot(months, values)

pyplot.title("Months sales in $")
pyplot.xlabel("Months")
pyplot.ylabel("Sales ($)")

pyplot.show()