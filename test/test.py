# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0  # go=bit0, finish=bit1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    dut._log.info("Test RangeFinder: input 10, 50, 30 -> range should be 40")

    # go=1, first data=10
    dut.ui_in.value = 10
    dut.uio_in.value = 0b00000001  # go=1
    await ClockCycles(dut.clk, 1)

    # go=0, data=50
    dut.ui_in.value = 50
    dut.uio_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)

    # go=0, data=30
    dut.ui_in.value = 30
    dut.uio_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)

    # finish=1
    dut.ui_in.value = 0
    dut.uio_in.value = 0b00000010  # finish=1
    await ClockCycles(dut.clk, 1)

    # finish=0, check output
    dut.uio_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)

    # range = max - min = 50 - 10 = 40
    assert dut.uo_out.value == 40, f"Expected 40, got {dut.uo_out.value}"
    dut._log.info("Test passed!")