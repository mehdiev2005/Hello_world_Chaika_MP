print('=== Анализ последовательности ДНК ===')

dna_raw = input('Введите последовательность ДНК: ')
dna = dna_raw.upper()

length = len(dna)
am_A = dna.count('A')
am_T = dna.count('T')
am_G = dna.count('G')
am_C = dna.count('C')

print('Подсчёт нуклеотидов:',
      f'A: {am_A}',
      f'T: {am_T}',
      f'G: {am_G}',
      f'C: {am_C}',
      '',
      f'Общая длина: {length}',
      sep='\n')
