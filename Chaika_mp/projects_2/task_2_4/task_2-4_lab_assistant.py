volume = float(input('Введите необходимый объём раствора, мл: '))
mass = round(volume*0.009, 3)
water_vol = volume


with open("report.txt", "w", encoding="utf-8") as file:
    file.write('ОТЧЁТ ПО ПРИГОТОВЛЕНИЮ:\n')
    file.write('-'*23)
    file.write('\n')
    file.write(f'Общий объём:\t {volume} мл\n')
    file.write(f'VМасса соли:\t {mass} мл\n')
    file.write(f'Объём воды:\t\t {water_vol} мл\n')
