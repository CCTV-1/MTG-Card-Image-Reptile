#!/usr/bin/python3
# coding=utf-8

import os
#import re
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup


def GetSetInfo( SetShortName ):
    CardInfo = []
    try:
        resp = requests.get( 'http://magiccards.info/' + SetShortName + '/en.html' , timeout=13 )
    except (requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout):
        print( "\nTimeOutError:\n\tGet set %s info time out" %SetShortName )
        exit( False )
    html = resp.text
    soup = BeautifulSoup( html , 'html.parser' )
    try:
        table = soup.find( 'table' , { 'cellpadding' : 3 } )
        for row in table.findAll( 'tr' ):
            NameObj = row.find( 'a' )
            NumberObj = row.find( 'td' , { 'align' : 'right' } )
            name = NameObj.get_text()
            #name = re.sub( r'</?\w+[^>]*>' , '' , str( row.find( 'a' ) ) )
            number = NumberObj.get_text()
            #number = re.sub( r'</?\w+[^>]*>' , '' , str( row.find( 'td' , { 'align' : 'right' } ) ) )
            CardInfo.append( ( number , name ) )
        return CardInfo
    except ( AttributeError , TypeError ):
        print( "Set %s info not find" %SetShortName )
        exit( False )

def DownloadImage( SetShortName , CardID , CardName ):
    ImageDownloadUrl = 'http://magiccards.info/scans/cn/' + SetShortName + '/' + CardID  +'.jpg'
    try:
        imageobject = requests.get( ImageDownloadUrl , timeout = 13 )
    except ( requests.exceptions.ReadTimeout , requests.exceptions.ConnectTimeout ):
        print( "\nTimeOutError:\n\tDownload Card %s request timeout stop downloading!" %CardName )
        exit( False )
    if imageobject.headers[ 'Content-Type' ] == 'image/jpeg':
        open( CardName + '.full.jpg' , 'wb' ).write( imageobject.content )
        print( "Download card:%s success,the number is:%s" %( CardName , CardID ) )
    else:
        print( "\nContent-Type Error:\n\trequest not is jpeg image file,the card is %s number is:%s" %( CardName , CardID ) )

if __name__ == '__main__':
    SetShortName = input( 'You plan download setshortname:' )
    CardInfo = GetSetInfo( SetShortName )
    if os.path.exists( './' + SetShortName ) == False:
        os.mkdir( './' + SetShortName )
    os.chdir( './' + SetShortName )
    p = Pool( processes = 4 )
    print( "Download start,Card total %d" %len( CardInfo ) )
    for i in CardInfo:
        p.apply_async( DownloadImage , args=( SetShortName , i[0] , i[1] ) )
        #DownloadImage( SetShortName , i[0] , i[1] )
    p.close()
    p.join()
    print( 'All download success' )
