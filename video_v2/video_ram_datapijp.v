module video_ram_datapijp (
    input clk,
    input resetn,
    input de,               // flow control
    output reg [23:0] rgb,      // 24-bit RGB

    output reg [12:0] sp_ad,
    input wire [7:0] sp_dout,
    output clk_6_25,
    output busy
);

    localparam HOR_PIXELS = 1024;
    localparam VER_PIXELS = 768;

    // Pixel counters
    reg [11:0] hcount = 0;
    reg [11:0] vcount = 0;

    // RAM interface
    reg [12:0] ram_addr;
    reg [12:0] ram_ada;
    wire [7:0] ram_dout;
    reg [7:0] ram_din = 0;
    reg ram_wre = 0;
    reg ram_ce  = 1;
    reg ram_oce = 1;
    reg ram_cea = 1;

    // Instantie Gowin_SDPB RAM
    Gowin_SDPB dram (
        .dout(ram_dout),
        .clkb(clk),
        .clka(cnt[2]),
        .oce(ram_oce),
        .ceb(ram_ce),
        .cea(ram_cea),
        .resetb(~resetn),
        .reseta(~resetn),
        .adb(ram_addr),
        .ada(ram_ada),
        .din(ram_din)
    );
//------------------------------------------------//
    // clk 6,25 Mhz 25 / 4
    reg [2:0] cnt;
    always @(posedge clk) begin cnt <= cnt +1; end
    wire clk_6_25 = cnt[2];

    // Instantie ULA_MY
    ula_my ula (
        .clk(clk_6_25),
        .resetn(resetn),
        .busy(busy),
        .h_count(h_count),
        .v_count(v_count)
    );

    // SP_RAM interface
//    reg [12:0] sp_ad;
//    reg [7:0] sp_din;
//    wire [7:0] sp_dout;
    reg sp_oce = 1;
    reg sp_ce = 1;
    reg sp_wre = 0;

/*    // Instantie Gowin_SP RAM
    Gowin_SP ram (
        .dout(sp_dout),
        .clk(clk_6_25),
        .oce(sp_oce),
        .ce(sp_ce),
        .reset(~resetn),
        .wre(sp_wre),
        .ad(sp_ad),
        .din(sp_din)
    );
*/
    // read sp_ram en write sdpb_ram
    wire [7:0] h_count;
    wire [7:0] v_count;
    wire busy;
    wire [13:0] copy_pix_addr = { v_count[7:6], v_count[2:0], v_count[5:3], h_count[7:3] };
    wire [13:0] copy_attr_addr = 6144 + {v_count[7:3], h_count[7:3]};

reg write_phase;        // 0 = pixels, 1 = attributen

always @(posedge cnt[2]) begin
    if (busy) begin
        case (write_phase)
        0: begin
            sp_ad <= copy_pix_addr;
            ram_ada <= copy_pix_addr;
            ram_din <= sp_dout;
            write_phase <= 1;
        end
        1: begin
            sp_ad <= copy_attr_addr;
            ram_ada <= copy_attr_addr;
            ram_din <= sp_dout;
            write_phase <= 0;
        end
        endcase
    end
end


//------------------------------------------------//
    // Pixel & attribute berekeningen

    wire [7:0] h = hcount[9:2];
    wire [7:0] v = vcount[9:2];
    wire [13:0] pix_addr  = { v[7:6], v[2:0], v[5:3], h[7:3] };
    wire [13:0] attr_addr = 6144 + {v[7:3], h[7:3]};  
    wire [2:0] bitpos = 8 - h[2:0];



    // Pipelined registers
    reg [7:0] pixel_byte, pixel_byte_d;
    reg [7:0] attr_byte, attr_byte_d;
    reg [1:0] read_phase;

    always @(posedge clk) begin
        if (!resetn) begin
            hcount <= 0;
            vcount <= 0;
            ram_addr <= 0;
            ram_wre <= 0;
        end else if (de) begin
            // Start-of-frame

            case (read_phase)
            0: begin
            // Leescyclus pixel & attribuut
            ram_addr <= pix_addr;
            pixel_byte <= ram_dout;
            read_phase <= 1;
            end
            1: begin
            ram_addr <= attr_addr;
            attr_byte <= ram_dout;
            read_phase <= 0;
            end
            endcase

            // Pipeline registers
            pixel_byte_d <= pixel_byte;
            attr_byte_d <= attr_byte;

            // RGB-output gebaseerd op pixel-bit en attribuut
            rgb <= pixel_byte_d[bitpos] ? {
                attr_byte[2] ? 8'hC0 : 8'h00, 
                attr_byte[1] ? 8'hC0 : 8'h00, 
                attr_byte[0] ? 8'hC0 : 8'h00} : {
                attr_byte[5] ? 8'hC0 : 8'h00, 
                attr_byte[4] ? 8'hC0 : 8'h00, 
                attr_byte[3] ? 8'hC0 : 8'h00} ;

            // Pixel counters
            if (hcount == HOR_PIXELS-1) begin
                hcount <= 0;
                vcount <= (vcount == VER_PIXELS-1) ? 0 : vcount + 1;
            end else begin
                hcount <= hcount + 1;
            end
        end
    end
endmodule