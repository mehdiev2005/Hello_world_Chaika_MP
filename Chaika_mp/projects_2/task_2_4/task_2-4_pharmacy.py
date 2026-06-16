caps = int(input('Введите количество капсул: '))
capacity = int(input('Введите вместимость упаковки: '))


print('--- Отчёт фасовочного цеха ---',
      f'Полных упаковок:\t {caps//capacity}',
      f'Остаток капсул:\t {caps%capacity}',
      sep='\n')
