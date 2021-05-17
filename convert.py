import os
import shutil
os.makedirs('converted', exist_ok=True)
items = []
for f in os.listdir('codes/accepted_codes'):
    src = 'codes/accepted_codes/'+f
    f = f.lower().replace(' ', '-')
    head = f.split('_')[0]
    tail = f.split('.')[1]
    dst = 'converted/'+head+'.'+tail
    dst = dst.replace(',', '').replace(
        '(', '').replace(')', '').replace(':', '')
    items.append((f.split('_')[-1].split('.')[0], src, dst))
items = sorted(items)
for _, src, dst in items:
    shutil.copy(src, dst)
