/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    logic [7:0] range_out;
    logic debug_error;
    logic [7:0] high_q, low_q;

    RangeFinder #(.WIDTH(8)) rf (
        .data_in    (ui_in),
        .clock      (clk),
        .reset      (~rst_n),
        .go         (uio_in[0]),
        .finish     (uio_in[1]),
        .range      (range_out),
        .debug_error(debug_error),
        .high_q     (high_q),
        .low_q      (low_q)
    );

    assign uo_out  = range_out;
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire _unused = &{ena, debug_error, high_q, low_q, uio_in[7:2], 1'b0};

endmodule
