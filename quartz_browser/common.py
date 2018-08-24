import os, time
from urllib import parse
from cgi import parse_header
from PyQt5 import QtCore

extensions = {
'application/pdf': '.pdf',
'audio/mpeg': '.mp3',
'video/mpeg': '.mp4',
'video/mp4': '.mp4',
'video/3gpp': '.3gp',
'video/matroska': '.mkv',
'image/jpeg': '.jpg',
'image/png': '.png',
}

def validateFileName(text, mimetype=None):
    """ Removes all forbidden chars and extra spaces"""
    if text == '':
        text = time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        chars = [ '/', '\\', '|', '*', '"', '`', '<', '>', '^', '?', '$', '=']
        for char in  chars:
            text = text.replace(char, ' ')
        while '  ' in text:
            text = text.replace('  ', ' ')
    text = text[:255] # maximum filename length
    text = os.path.splitext(text)[0][:100] + os.path.splitext(text)[1] # limit it around 100
    if mimetype and (mimetype in extensions):
        text = os.path.splitext(text)[0] + extensions[mimetype]
    return text

def wait(millisec):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(millisec, loop.quit)
    loop.exec_()

# rename filename if already exists
def autoRename(filename):
    name, ext = os.path.splitext(filename)
    i = 0
    while 1:
        if not os.path.exists(filename) : return filename
        i+=1
        filename = name + str(i) + ext

# get filename from Content-Disposition header
def filenameFromHeader(header):
    value, params = parse_header(header)
    if 'filename*' in params:
        filename = params['filename*']
        if filename.startswith("UTF-8''"):
            filename = parse.unquote(filename[7:])
    elif 'filename' in params:
        filename = params['filename']
    else:
        filename = ''
    return filename

# get filename from url string
def filenameFromUrl(addr):
    Url = QtCore.QUrl.fromUserInput(addr)
    Url.setFragment(None)
    url = Url.toString(QtCore.QUrl.RemoveQuery)
    return QtCore.QFileInfo(parse.unquote_plus(url)).fileName()
