phenotype_donor = input("Введите фенотип группы крови донора (I, II, III, IV): ").strip().upper()
phenotype_recip = input("Введите фенотип группы крови реципиента (I, II, III, IV): ").strip().upper()

if phenotype_donor == phenotype_recip or phenotype_donor == 'I':
    print('Этому реципиенту можно периливать кровь от этого донора!')
else:
    print('Этому реципиенту нельзя периливать кровь от этого донора!')
