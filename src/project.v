/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_amin_hong_ooo_cpu (
    input  wire [7:0] ui_in,    // instruction[7:0]
    output wire [7:0] uo_out,   // output[7:0]
    input  wire [7:0] uio_in,   // instruction[11:8] = uio_in[3:0]
    output wire [7:0] uio_out,  // output[11:8] = uio_out[7:4]
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [11:0] io_in_internal;
    wire [11:0] io_out_internal;

    assign io_in_internal = {uio_in[3:0], ui_in[7:0]};

    assign uo_out          = io_out_internal[7:0];
    assign uio_out[7:4]    = io_out_internal[11:8];
    assign uio_out[3:0]    = 4'b0000;

    assign uio_oe = 8'b1111_0000;

    my_chip mchip (
        .io_in  (io_in_internal),
        .io_out (io_out_internal),
        .clock  (clk),
        .reset  (~rst_n)         
    );

endmodule
