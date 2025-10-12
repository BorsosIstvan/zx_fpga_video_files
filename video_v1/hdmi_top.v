module hdmi_tmds_top (
    input  wire        resetn,
    input  wire        clk,

/*    // parallel pixel input (one pixel per clk_pixel)
    input  wire [23:0] pixel_in,      // {R[7:0], G[7:0], B[7:0]}
    input  wire        in_de,         // data enable (active video)
    input  wire        in_hsync,
    input  wire        in_vsync,
*/
    // HDMI differential outputs (map pins in constraints)
    output wire tmds_clk_p,
    output wire tmds_clk_n,
    output wire [2:0] tmds_d_p,
    output wire [2:0] tmds_d_n
);

    wire        clk_pixel;      // pixel clock (PCLK)
    wire        clk_5x_pixel;   // 5x pixel clock (FCLK)

    // CLOCK pixel & 5x pixel 
    Gowin_rPLL rpll (.clkin(clk), .clkout(clk_5x_pixel), .lock(resetn));

    Gowin_CLKDIV clkdiv (.hclkin(clk_5x_pixel), .clkout(clk_pixel), .resetn(resetn));

    // TIMING 1024x768
    wire de;
    timing_1024x768_flow timing_flow(
    .clk_pixel(clk_pixel),
    .resetn(resetn),
    .de(de)
);

    // COLORBAR flow
    wire [23:0] rgb_pixel;
    video_ram_datapijp colorbar(
    .clk(clk_pixel),
    .resetn(resetn),
    .de(de),
    .rgb(rgb_pixel)
);

    // split RGB channels
    wire [7:0] r = rgb_pixel[23:16];
    wire [7:0] g = rgb_pixel[15:8];
    wire [7:0] b = rgb_pixel[7:0];

    // TMDS encoder outputs (per channel)
    wire [9:0] tmds_r;
    wire [9:0] tmds_g;
    wire [9:0] tmds_b;


    // instantiate three encoders
    tmds_std_enc enc_r (.clk(clk_pixel), .resetn(resetn), .de(de), .c0(hsync), .c1(vsync), .din(r), .dout(tmds_r));
    tmds_std_enc enc_g (.clk(clk_pixel), .resetn(resetn), .de(de), .c0(1'b0), .c1(1'b0), .din(g), .dout(tmds_g));
    tmds_std_enc enc_b (.clk(clk_pixel), .resetn(resetn), .de(de), .c0(1'b0), .c1(1'b0), .din(b), .dout(tmds_b));

    // Prepare OSER10 parallel inputs.
    // Gowin OSER10 array instantiation expects D0..D9 buses where each Dx is 3 bits (one per channel).
    // We map bit [2]=R, [1]=G, [0]=B so that tmds_d[2] is red channel, etc.
    wire [2:0] tmds_d0  = { tmds_r[0], tmds_g[0], tmds_b[0] };
    wire [2:0] tmds_d1  = { tmds_r[1], tmds_g[1], tmds_b[1] };
    wire [2:0] tmds_d2  = { tmds_r[2], tmds_g[2], tmds_b[2] };
    wire [2:0] tmds_d3  = { tmds_r[3], tmds_g[3], tmds_b[3] };
    wire [2:0] tmds_d4  = { tmds_r[4], tmds_g[4], tmds_b[4] };
    wire [2:0] tmds_d5  = { tmds_r[5], tmds_g[5], tmds_b[5] };
    wire [2:0] tmds_d6  = { tmds_r[6], tmds_g[6], tmds_b[6] };
    wire [2:0] tmds_d7  = { tmds_r[7], tmds_g[7], tmds_b[7] };
    wire [2:0] tmds_d8  = { tmds_r[8], tmds_g[8], tmds_b[8] };
    wire [2:0] tmds_d9  = { tmds_r[9], tmds_g[9], tmds_b[9] };

    // serializer outputs (one Q bus for all three OSER10 instances)
    wire [2:0] tmds_serial_q; // each bit is the serial output for red/green/blue respectively

    // Gowin OSER10 primitive array (3 serializers in parallel)
    // NOTE: this is Gowin-specific instantiation; keep names/signature same as vendor example.
    OSER10 tmds_serdes [2:0] (
        .Q(tmds_serial_q),
        .D0(tmds_d0),
        .D1(tmds_d1),
        .D2(tmds_d2),
        .D3(tmds_d3),
        .D4(tmds_d4),
        .D5(tmds_d5),
        .D6(tmds_d6),
        .D7(tmds_d7),
        .D8(tmds_d8),
        .D9(tmds_d9),
        .PCLK(clk_pixel),
        .FCLK(clk_5x_pixel),
        .RESET(~resetn)
    );

    // Connect serializer output plus pixel clock into ELVDS differential buffers
    // The ordering here: .I({clk_pixel, tmds_serial_q}) -> I is 4-bit bus {clk, dR, dG, dB}
    ELVDS_OBUF tmds_bufds [3:0] (
        .I({ clk_pixel, tmds_serial_q }),
        .O({ tmds_clk_p, tmds_d_p }),
        .OB({ tmds_clk_n, tmds_d_n })
    );

endmodule
