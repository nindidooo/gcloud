from firebase import firebase

root = '31_12_2017_02_52_33'
firebase = firebase.FirebaseApplication('https://sheetmuse.firebaseio.com/')
result = firebase.get(root, 'mididownload')

# firebase.delete(root, '')
# resultPut = firebase.put(root, 'username', 'matthewcsbrown@gmail.com')
# resultPut = firebase.put(root, 'audiofile', root + '.3gp')
resultPut = firebase.put(root, 'midifile', root + '.mid')

print(resultPut)

# print(result)
