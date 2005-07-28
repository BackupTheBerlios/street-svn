#Module that provides miscellaneous screen utilities.

from pyui.desktop import getRenderer

def center(w, h, ):
    (wScr, hScr) = getRenderer().getScreenSize()
    return ((wScr-w)/2, (hScr-h)/2)
