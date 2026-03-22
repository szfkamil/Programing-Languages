dates = [
    {'day': 15, 'month': 7, 'year': 2026},
    {'day': 8, 'month': 1, 'year': 2023},
    {'day': 10, 'month': 3, 'year': 2024},
    {'day': 25, 'month': 12, 'year': 2025},
    {'day': 12, 'month': 6, 'year': 2023}
]

month_list = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
n = len(dates)

for i in range(n):
    for j in range(n-i-1):
        change = False
        if dates[j]["year"] > dates[j+1]["year"]:
            change = True
        elif dates[j]["year"] == dates[j+1]["year"]:
            if dates[j]["month"] > dates[j+1]["month"]:
                change = True
            elif dates[j]["month"] == dates[j+1]["month"]:
                if dates[j]["day"] > dates[j+1]["day"]:
                    change = True
        if change:
            dates[j], dates[j+1] = dates [j+1], dates[j]

for i in range(len(dates)):
    print(f"{i+1}) {dates[i]["day"]} {month_list[dates[i]["month"]]} {dates[i]["year"]}")