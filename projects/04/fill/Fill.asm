// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(OUTER)
    @8192 // # of screen addresses
    D=A
    @loc
    M=D
    @INNER
    0;JMP
(INNER)
    @24576 // keyboard
    D=M
    @WHITE
    D;JEQ // key = 0 (white)
    @BLACK
    0;JMP // key != 0 (black)
(WHITE)
    @16384 // screen
    D=A
    @loc
    D=D+M
    A=D
    M=0
    @ENDINNER
    0;JMP
(BLACK)
    @16384 // screen
    D=A
    @loc
    D=D+M
    A=D
    M=-1
    @ENDINNER
    0;JMP
(ENDINNER)
    @loc
    M=M-1 // decrement @loc
    D=M
    @OUTER
    D;JLT // restart loop if @loc < 0
    @INNER
    0;JMP