# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 30MHz clock → period ≈ 33ns
    clock = Clock(dut.clk, 33, unit="ns")
    cocotb.start_soon(clock.start())

    # Helper function to set instruction inputs
    def set_instr(instr):
        dut.ui_in.value  = instr & 0xFF          # [7:0]
        dut.uio_in.value = (instr >> 8) & 0xF    # [11:8]

    # Reset
    dut.rst_n.value = 0
    dut.ena.value   = 1
    set_instr(0)
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1

    # Instructions
    instr_mem = [
        (0b101 << 9) | (0 << 6) | (0 << 3) | 0,  # LD  R0, MEM[0]
        (0b000 << 9) | (1 << 6) | (0 << 3) | 2,  # ADD R1, R0, R2
        (0b001 << 9) | (4 << 6) | (5 << 3) | 3,  # SUB R4, R5, R3
        (0b011 << 9) | (4 << 6) | (6 << 3) | 7,  # OR  R4, R6, R7
        (0b101 << 9) | (6 << 6) | (6 << 3) | 2,  # LD  R6, MEM[2]
        (0b100 << 9) | (2 << 6) | (3 << 3) | 6,  # XOR R2, R3, R6
        (0b010 << 9) | (3 << 6) | (7 << 3) | 6,  # AND R3, R7, R6
        (0b111 << 9) | 0,                          # HALT
    ]

    # Feed instructions
    for instr in instr_mem:
        set_instr(instr)
        await RisingEdge(dut.clk)

    set_instr(0)

    # wait for some cycles to let the CPU execute instructions
    await ClockCycles(dut.clk, 100)

    # Check outputs (uo[7:0] and uio[7:4])
    for _ in range(8):
        out = (dut.uio_out.value.integer & 0xF0) << 4 | dut.uo_out.value.integer
        dut._log.info(f"out = {out:#014b} | uo={dut.uo_out.value:#010b} uio={dut.uio_out.value:#010b}")
        await RisingEdge(dut.clk)

    dut._log.info("Done")
    assert dut.uo_out.value is not None