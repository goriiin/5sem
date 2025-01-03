`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:21:24 06/07/2024 
// Design Name: 
// Module Name:    main 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module main (
	input clk,
	input count, 
	input rst,  
	output [3:0] a, 
	output [7:0] led,
	output [1:0] state
);
    wire cnt;
    lab2_example lab2_example_inst (
        .clk(clk),
        .rst(rst),
        .count(count), 
        .cnt(cnt),
        .s_out(state)
    );

	//   
	reg [16:0] counter;
	wire counter_ovf = (counter == 2**16);
	always @(posedge clk) 
		if(rst || counter_ovf) 
			counter <= 0;
		else
			counter <= counter + 1;

	//   CNT
    reg cnt_ff;
    wire cnt_rise = (cnt==1'b1) && (cnt_ff==1'b0);
    always @(posedge clk) 
        if(rst)
            cnt_ff <= 1'b0;
        else
            cnt_ff <= cnt;

    // 
    reg [15:0] main_counter;
    always @(posedge clk) 
        if(rst)
            main_counter <= 0;
        else 
            if(cnt_rise) 
                main_counter <= main_counter + 1;

    wire [3:0] d_wire;
    seven_segment_driver ssd_inst (
        .clk(clk),
        .rst(rst),
        .q(main_counter),
        .clk_div(counter_ovf),
        .d(d_wire),
        .a(a)
    );
   
    led_decode led_decode_inst (
        .dh(d_wire),
        .seg_data(led)
    );

endmodule 

