@256 // 0
D=A // 1
@SP // 2
M=D // 3
@Sys.initRET0 // 4
D=A // 5
@SP // 6
A=M // 7
M=D // 8
@SP // 9
M=M+1 // 10
@LCL // 11
D=M // 12
@SP // 13
A=M // 14
M=D // 15
@SP // 16
M=M+1 // 17
@ARG // 18
D=M // 19
@SP // 20
A=M // 21
M=D // 22
@SP // 23
M=M+1 // 24
@THIS // 25
D=M // 26
@SP // 27
A=M // 28
M=D // 29
@SP // 30
M=M+1 // 31
@THAT // 32
D=M // 33
@SP // 34
A=M // 35
M=D // 36
@SP // 37
M=M+1 // 38
@SP // 39
D=M // 40
@LCL // 41
M=D // 42
@5 // 43
D=D-A // 44
@ARG // 45
M=D // 46
@Sys.init // 47
0;JMP // 48
(Sys.initRET0)
//////
// Class1
// function Class1.set 0
(Class1.set)
// push argument 0
@ARG // 49
D=M // 50
@0 // 51
A=D+A // 52
D=M // 53
@SP // 54
A=M // 55
M=D // 56
@SP // 57
M=M+1 // 58
// pop static 0
@Class1.0 // 59
D=A // 60
@R13 // 61
M=D // 62
@SP // 63
M=M-1 // 64
A=M // 65
D=M // 66
@R13 // 67
A=M // 68
M=D // 69
// push argument 1
@ARG // 70
D=M // 71
@1 // 72
A=D+A // 73
D=M // 74
@SP // 75
A=M // 76
M=D // 77
@SP // 78
M=M+1 // 79
// pop static 1
@Class1.1 // 80
D=A // 81
@R13 // 82
M=D // 83
@SP // 84
M=M-1 // 85
A=M // 86
D=M // 87
@R13 // 88
A=M // 89
M=D // 90
// push constant 0
@0 // 91
D=A // 92
@SP // 93
A=M // 94
M=D // 95
@SP // 96
M=M+1 // 97
// return
@LCL // 98
D=M // 99
@R13 // 100
M=D // 101
@R13 // 102
D=M // 103
@5 // 104
D=D-A // 105
A=D // 106
D=M // 107
@R14 // 108
M=D // 109
@SP // 110
M=M-1 // 111
A=M // 112
D=M // 113
@ARG // 114
A=M // 115
M=D // 116
@ARG // 117
D=M // 118
@SP // 119
M=D+1 // 120
@R13 // 121
D=M // 122
@1 // 123
D=D-A // 124
A=D // 125
D=M // 126
@THAT // 127
M=D // 128
@R13 // 129
D=M // 130
@2 // 131
D=D-A // 132
A=D // 133
D=M // 134
@THIS // 135
M=D // 136
@R13 // 137
D=M // 138
@3 // 139
D=D-A // 140
A=D // 141
D=M // 142
@ARG // 143
M=D // 144
@R13 // 145
D=M // 146
@4 // 147
D=D-A // 148
A=D // 149
D=M // 150
@LCL // 151
M=D // 152
@R14 // 153
A=M // 154
0;JMP // 155
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.0 // 156
D=M // 157
@SP // 158
A=M // 159
M=D // 160
@SP // 161
M=M+1 // 162
// push static 1
@Class1.1 // 163
D=M // 164
@SP // 165
A=M // 166
M=D // 167
@SP // 168
M=M+1 // 169
// sub
@SP // 170
M=M-1 // 171
A=M // 172
D=M // 173
@SP // 174
M=M-1 // 175
@SP // 176
A=M // 177
M=M-D // 178
@SP // 179
M=M+1 // 180
// return
@LCL // 181
D=M // 182
@R13 // 183
M=D // 184
@R13 // 185
D=M // 186
@5 // 187
D=D-A // 188
A=D // 189
D=M // 190
@R14 // 191
M=D // 192
@SP // 193
M=M-1 // 194
A=M // 195
D=M // 196
@ARG // 197
A=M // 198
M=D // 199
@ARG // 200
D=M // 201
@SP // 202
M=D+1 // 203
@R13 // 204
D=M // 205
@1 // 206
D=D-A // 207
A=D // 208
D=M // 209
@THAT // 210
M=D // 211
@R13 // 212
D=M // 213
@2 // 214
D=D-A // 215
A=D // 216
D=M // 217
@THIS // 218
M=D // 219
@R13 // 220
D=M // 221
@3 // 222
D=D-A // 223
A=D // 224
D=M // 225
@ARG // 226
M=D // 227
@R13 // 228
D=M // 229
@4 // 230
D=D-A // 231
A=D // 232
D=M // 233
@LCL // 234
M=D // 235
@R14 // 236
A=M // 237
0;JMP // 238
//////
// Class2
// function Class2.set 0
(Class2.set)
// push argument 0
@ARG // 239
D=M // 240
@0 // 241
A=D+A // 242
D=M // 243
@SP // 244
A=M // 245
M=D // 246
@SP // 247
M=M+1 // 248
// pop static 0
@Class2.0 // 249
D=A // 250
@R13 // 251
M=D // 252
@SP // 253
M=M-1 // 254
A=M // 255
D=M // 256
@R13 // 257
A=M // 258
M=D // 259
// push argument 1
@ARG // 260
D=M // 261
@1 // 262
A=D+A // 263
D=M // 264
@SP // 265
A=M // 266
M=D // 267
@SP // 268
M=M+1 // 269
// pop static 1
@Class2.1 // 270
D=A // 271
@R13 // 272
M=D // 273
@SP // 274
M=M-1 // 275
A=M // 276
D=M // 277
@R13 // 278
A=M // 279
M=D // 280
// push constant 0
@0 // 281
D=A // 282
@SP // 283
A=M // 284
M=D // 285
@SP // 286
M=M+1 // 287
// return
@LCL // 288
D=M // 289
@R13 // 290
M=D // 291
@R13 // 292
D=M // 293
@5 // 294
D=D-A // 295
A=D // 296
D=M // 297
@R14 // 298
M=D // 299
@SP // 300
M=M-1 // 301
A=M // 302
D=M // 303
@ARG // 304
A=M // 305
M=D // 306
@ARG // 307
D=M // 308
@SP // 309
M=D+1 // 310
@R13 // 311
D=M // 312
@1 // 313
D=D-A // 314
A=D // 315
D=M // 316
@THAT // 317
M=D // 318
@R13 // 319
D=M // 320
@2 // 321
D=D-A // 322
A=D // 323
D=M // 324
@THIS // 325
M=D // 326
@R13 // 327
D=M // 328
@3 // 329
D=D-A // 330
A=D // 331
D=M // 332
@ARG // 333
M=D // 334
@R13 // 335
D=M // 336
@4 // 337
D=D-A // 338
A=D // 339
D=M // 340
@LCL // 341
M=D // 342
@R14 // 343
A=M // 344
0;JMP // 345
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.0 // 346
D=M // 347
@SP // 348
A=M // 349
M=D // 350
@SP // 351
M=M+1 // 352
// push static 1
@Class2.1 // 353
D=M // 354
@SP // 355
A=M // 356
M=D // 357
@SP // 358
M=M+1 // 359
// sub
@SP // 360
M=M-1 // 361
A=M // 362
D=M // 363
@SP // 364
M=M-1 // 365
@SP // 366
A=M // 367
M=M-D // 368
@SP // 369
M=M+1 // 370
// return
@LCL // 371
D=M // 372
@R13 // 373
M=D // 374
@R13 // 375
D=M // 376
@5 // 377
D=D-A // 378
A=D // 379
D=M // 380
@R14 // 381
M=D // 382
@SP // 383
M=M-1 // 384
A=M // 385
D=M // 386
@ARG // 387
A=M // 388
M=D // 389
@ARG // 390
D=M // 391
@SP // 392
M=D+1 // 393
@R13 // 394
D=M // 395
@1 // 396
D=D-A // 397
A=D // 398
D=M // 399
@THAT // 400
M=D // 401
@R13 // 402
D=M // 403
@2 // 404
D=D-A // 405
A=D // 406
D=M // 407
@THIS // 408
M=D // 409
@R13 // 410
D=M // 411
@3 // 412
D=D-A // 413
A=D // 414
D=M // 415
@ARG // 416
M=D // 417
@R13 // 418
D=M // 419
@4 // 420
D=D-A // 421
A=D // 422
D=M // 423
@LCL // 424
M=D // 425
@R14 // 426
A=M // 427
0;JMP // 428
//////
// Sys
// function Sys.init 0
(Sys.init)
// push constant 6
@6 // 429
D=A // 430
@SP // 431
A=M // 432
M=D // 433
@SP // 434
M=M+1 // 435
// push constant 8
@8 // 436
D=A // 437
@SP // 438
A=M // 439
M=D // 440
@SP // 441
M=M+1 // 442
// call Class1.set 2
@Class1.setRET1 // 443
D=A // 444
@SP // 445
A=M // 446
M=D // 447
@SP // 448
M=M+1 // 449
@LCL // 450
D=M // 451
@SP // 452
A=M // 453
M=D // 454
@SP // 455
M=M+1 // 456
@ARG // 457
D=M // 458
@SP // 459
A=M // 460
M=D // 461
@SP // 462
M=M+1 // 463
@THIS // 464
D=M // 465
@SP // 466
A=M // 467
M=D // 468
@SP // 469
M=M+1 // 470
@THAT // 471
D=M // 472
@SP // 473
A=M // 474
M=D // 475
@SP // 476
M=M+1 // 477
@SP // 478
D=M // 479
@LCL // 480
M=D // 481
@7 // 482
D=D-A // 483
@ARG // 484
M=D // 485
@Class1.set // 486
0;JMP // 487
(Class1.setRET1)
// pop temp 0
@R5 // 488
D=A // 489
@R13 // 490
M=D // 491
@SP // 492
M=M-1 // 493
A=M // 494
D=M // 495
@R13 // 496
A=M // 497
M=D // 498
// push constant 23
@23 // 499
D=A // 500
@SP // 501
A=M // 502
M=D // 503
@SP // 504
M=M+1 // 505
// push constant 15
@15 // 506
D=A // 507
@SP // 508
A=M // 509
M=D // 510
@SP // 511
M=M+1 // 512
// call Class2.set 2
@Class2.setRET2 // 513
D=A // 514
@SP // 515
A=M // 516
M=D // 517
@SP // 518
M=M+1 // 519
@LCL // 520
D=M // 521
@SP // 522
A=M // 523
M=D // 524
@SP // 525
M=M+1 // 526
@ARG // 527
D=M // 528
@SP // 529
A=M // 530
M=D // 531
@SP // 532
M=M+1 // 533
@THIS // 534
D=M // 535
@SP // 536
A=M // 537
M=D // 538
@SP // 539
M=M+1 // 540
@THAT // 541
D=M // 542
@SP // 543
A=M // 544
M=D // 545
@SP // 546
M=M+1 // 547
@SP // 548
D=M // 549
@LCL // 550
M=D // 551
@7 // 552
D=D-A // 553
@ARG // 554
M=D // 555
@Class2.set // 556
0;JMP // 557
(Class2.setRET2)
// pop temp 0
@R5 // 558
D=A // 559
@R13 // 560
M=D // 561
@SP // 562
M=M-1 // 563
A=M // 564
D=M // 565
@R13 // 566
A=M // 567
M=D // 568
// call Class1.get 0
@Class1.getRET3 // 569
D=A // 570
@SP // 571
A=M // 572
M=D // 573
@SP // 574
M=M+1 // 575
@LCL // 576
D=M // 577
@SP // 578
A=M // 579
M=D // 580
@SP // 581
M=M+1 // 582
@ARG // 583
D=M // 584
@SP // 585
A=M // 586
M=D // 587
@SP // 588
M=M+1 // 589
@THIS // 590
D=M // 591
@SP // 592
A=M // 593
M=D // 594
@SP // 595
M=M+1 // 596
@THAT // 597
D=M // 598
@SP // 599
A=M // 600
M=D // 601
@SP // 602
M=M+1 // 603
@SP // 604
D=M // 605
@LCL // 606
M=D // 607
@5 // 608
D=D-A // 609
@ARG // 610
M=D // 611
@Class1.get // 612
0;JMP // 613
(Class1.getRET3)
// call Class2.get 0
@Class2.getRET4 // 614
D=A // 615
@SP // 616
A=M // 617
M=D // 618
@SP // 619
M=M+1 // 620
@LCL // 621
D=M // 622
@SP // 623
A=M // 624
M=D // 625
@SP // 626
M=M+1 // 627
@ARG // 628
D=M // 629
@SP // 630
A=M // 631
M=D // 632
@SP // 633
M=M+1 // 634
@THIS // 635
D=M // 636
@SP // 637
A=M // 638
M=D // 639
@SP // 640
M=M+1 // 641
@THAT // 642
D=M // 643
@SP // 644
A=M // 645
M=D // 646
@SP // 647
M=M+1 // 648
@SP // 649
D=M // 650
@LCL // 651
M=D // 652
@5 // 653
D=D-A // 654
@ARG // 655
M=D // 656
@Class2.get // 657
0;JMP // 658
(Class2.getRET4)
// label WHILE
(Sys$WHILE)
// goto WHILE
@Sys$WHILE // 659
0;JMP // 660