#!/usr/bin/env python3
"""
pyplottst.py - pyplot examples and test
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2023-08-27'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = ''
__status__      = 'Production'
__printdebug__  = False

from datetime import datetime
import matplotlib.pyplot as plt

chess_pieces={
                'white_king'   :'\u2654',
                'white_queen'  :'\u2655',
                'white_rook'   :'\u2656',
                'white_bishop' :'\u2657',
                'white_knight' :'\u2658',
                'white_pawn'   :'\u2659',
                'black_king'   :'\u265a',
                'black_queen'  :'\u265b',
                'black_rook'   :'\u265c',
                'black_bishop' :'\u265d',
                'black_knight' :'\u265e',
                'black_pawn'   :'\u265f',
                }

def printchessboard():
    dpi = 600
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'

    nCols = 2
    nRows = 2
    n=8 
    fig, axs = plt.subplots(nCols,nRows,figsize=(6.4, 6.4), dpi=dpi)

    board = []
    for i in range(n):
        line=[]
        for j in range(n):
            line += [([((i+j)%2)*63+128]*3)]
        board += [line]

    print(board)

    #text = f'Chess pieces: \u2654 \u2655 \u2656 \u2657 \u2658 \u2659 \u265a \u265b \u265c \u265d \u265e \u265f' 
    #axs[i,j].text(0., 0., text, ha='left', va='bottom', color='black')
    text = chess_pieces['black_queen']
    for i in range(nCols): 
        for j in range(nRows):
            axs[i,j].set_axis_off()
            axs[i,j].imshow(board,origin='lower',extent=(0,n,0,n))
            for k in range(n):
                axs[i,j].text(k+0.5,k+0.5,text,ha='center',va='center',color='black',
                              fontweight='bold', fontfamily='monospace',fontsize=20)

    #plt.text(0., 0., text, ha='left', va='bottom', color='black')

#    fig.canvas.manager.window.wm_geometry('+10+10')
    #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9,top=0.9, wspace=0.1, hspace=0.1)
    #plt.show()
    plt.savefig('chesboard')


def main():
    printchessboard()

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    print(f'Chess pieces: \u2654 \u2655 \u2656 \u2657 \u2658 \u2659 \u265a \u265b \u265c \u265d \u265e \u265f')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')
    #input("Press Enter to continue.")
