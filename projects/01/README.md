For multi-way multi-bit chips, I have two implementations:

`.hdl` implementations are simpler and use previously built chips.

`.opt.hdl` are optimized implementations which use only Or, Not, and And gates and manually address the bus. These implementations avoid some redunant gates (i.e. having only one Not gate per layer, rather than duplicating Not gates by reusing chips). They are less readable, but are likely preferable in real implementations where small speed gains matter.