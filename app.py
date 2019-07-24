import requests
import urllib.request
import os
import hashlib

threadapi = 'https://a.4cdn.org/{0}/thread/{1}.json'
imageapi = 'https://i.4cdn.org/{0}/{1}{2}'
boardsapi = 'https://a.4cdn.org/boards.json'

boardsjson = requests.get(boardsapi).json()
boardsjson = boardsjson['boards']
boards = list(map(lambda x: {'title': x['title'], 'board': x['board']}, boardsjson))

if os.name == 'nt':
    imagedirname = 'Pictures'
else:
    imagedirname = 'images'

userdir = os.path.expanduser("~")
imgcollectiondir = '4chan'
imagedir = os.path.join(userdir, imagedirname)
collectiondir = os.path.join(imagedir, imgcollectiondir)

if not os.path.exists(imagedir):
    os.makedirs(imagedir)

if not os.path.exists(collectiondir):
    os.makedirs(collectiondir)

chboard = input('Board: ')
chthread = input('Thread: ')

threaddir = os.path.join(collectiondir, chthread)

if not os.path.exists(threaddir):
    os.makedirs(threaddir)

jsonres = requests.get( threadapi.format(chboard, chthread) ).json()
jsonres = jsonres['posts']

imageposts = list(filter(lambda x: 'tim' in x, jsonres))

print('Number of images: {0}\n'.format(len(imageposts)))

for post in imageposts:
    print('Filename: {0}'.format(post['filename']))
    print('URL: {0}'.format( imageapi.format( chboard, post['tim'], post['ext'] ) ))
    print('')
    localfile = os.path.join( threaddir, post['filename'] + post['ext'] )
    if os.path.isfile(localfile):
        onlinechecksum = hashlib.md5(requests.get( imageapi.format( chboard, post['tim'], post['ext'] ) ).content).hexdigest()
        localchecksum = hashlib.md5(open(localfile,'rb').read()).hexdigest()
        if onlinechecksum != localchecksum:
            counter = 1
            while True:
                filecheck = os.path.join( threaddir, '{0}({1}){2}'.format(post['filename'], counter, post['ext']) )
                if not os.path.isfile( filecheck ):
                    open(
                        filecheck, 'wb'
                    ).write(
                        requests.get(
                            imageapi.format( chboard, post['tim'], post['ext'] )
                        ).content
                    )
                    break
                else:
                    counter = counter + 1
        else:
            pass
    else:
        open(
            localfile, 'wb'
        ).write(
            requests.get(
                imageapi.format( chboard, post['tim'], post['ext'] )
            ).content
        )
