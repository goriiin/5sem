`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    15:58:33 06/07/2024 
// Design Name: 
// Module Name:    l2 
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
module l2(
    input rst, //  
	input clk, // 
	input count, //   
	output wire cnt, // ,   
	output wire[1:0] s_out //  
	);
	//       13
	localparam STATE0 = 2'b10;
	localparam STATE1 = 2'b00;
	localparam STATE2 = 2'b01;
	localparam STATE3 = 2'b11;
	//     t
	reg[1:0]  s;
	//      t+1
	wire[1:0]  sn;
	reg [20:0] counter; //  2^20
	wire dly_ovf; // " "
	wire dly_en;//    
	assign s_out = s;
	//  
	always @(posedge clk)
		if(rst) 
			s <= STATE0;
		else 
			s <= sn;
		//      CNT  DLY_EN (  )
	assign cnt = ~s[1];
	assign dly_en = s[1] & s[0] | (~(s[1] & s[0]));
		//      (  )
	assign sn[0] = (dly_ovf & ~s[1]) | (s[0] & ~dly_ovf);// 1

	assign sn[1] = (s[1] & s[0]) | (s[0] & ~count) | (s[1] & ~count);// 2
		//  
	always @(posedge clk) 
		if(rst || (dly_en == 1'b0)) 
			counter <= 0;
		else
			counter <= counter + 1;

	assign dly_ovf = (counter == 2**20); // 


endmodule