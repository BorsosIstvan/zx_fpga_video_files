module top (
    input wire clk,
    input wire reset_n,

    output wire tmds_clk_n,
    output wire tmds_clk_p,
    output wire [2:0] tmds_data_n,
    output wire [2:0] tmds_data_p
);

// =============== hdmi =================

hdmi my_hdmi (
    .clk(clk),
    .reset_n(reset_n),
    .tmds_clk_n(tmds_clk_n),
    .tmds_clk_p(tmds_clk_p),
    .tmds_data_n(tmds_data_n),
    .tmds_data_p(tmds_data_p),
    .rgb_clk(clk_video),
    .video_addr(video_addr),
    .video_dout(video_dout)
);

// =============== video ram ============
wire [12:0] video_addr;
wire [7:0] video_dout;

dual_port_ram_dualclk dram_8k (
    .clk_video(clk_video),
    .video_addr(video_addr),
    .video_dout(video_dout),
    .clk_cpu(clk),
    .cpu_addr(),
    .cpu_din(),
    .cpu_we()
);

endmodule