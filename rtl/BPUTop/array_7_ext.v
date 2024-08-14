
module array_7_ext(
  input W0_clk,
  input [7:0] W0_addr,
  input W0_en,
  input [23:0] W0_data,
  input [3:0] W0_mask,
  input R0_clk,
  input [7:0] R0_addr,
  input R0_en,
  output [23:0] R0_data
);

  reg reg_R0_ren;
  reg [7:0] reg_R0_addr;
  reg [23:0] ram [255:0];
  `ifdef RANDOMIZE_MEM_INIT
    integer initvar;
    initial begin
      #`RANDOMIZE_DELAY begin end
      for (initvar = 0; initvar < 256; initvar = initvar+1)
        ram[initvar] = {1 {$random}};
      reg_R0_addr = {1 {$random}};
    end
  `endif
  integer i;
  always @(posedge R0_clk)
    reg_R0_ren <= R0_en;
  always @(posedge R0_clk)
    if (R0_en) reg_R0_addr <= R0_addr;
  always @(posedge W0_clk)
    if (W0_en) begin
      if (W0_mask[0]) ram[W0_addr][5:0] <= W0_data[5:0];
      if (W0_mask[1]) ram[W0_addr][11:6] <= W0_data[11:6];
      if (W0_mask[2]) ram[W0_addr][17:12] <= W0_data[17:12];
      if (W0_mask[3]) ram[W0_addr][23:18] <= W0_data[23:18];
    end
  `ifdef RANDOMIZE_GARBAGE_ASSIGN
  reg [31:0] R0_random;
  `ifdef RANDOMIZE_MEM_INIT
    initial begin
      #`RANDOMIZE_DELAY begin end
      R0_random = {$random};
      reg_R0_ren = R0_random[0];
    end
  `endif
  always @(posedge R0_clk) R0_random <= {$random};
  assign R0_data = reg_R0_ren ? ram[reg_R0_addr] : R0_random[23:0];
  `else
  assign R0_data = ram[reg_R0_addr];
  `endif

endmodule