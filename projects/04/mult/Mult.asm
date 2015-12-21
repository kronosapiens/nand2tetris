// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @prod
    M=0
(LOOP)
    @R0
    D=M // load counter
    @END
    D;JEQ // leave loop if counter == 0
    @prod
    D=M // load product so far (psf)
    @R1
    D=D+M // psf + base
    @prod
    M=D // save psf
    @R0
    M=M-1 // decrement counter
    @LOOP
    0;JMP
(END)
    @prod
    D=M // load product
    @R2
    M=D // put product in R2
