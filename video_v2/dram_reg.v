module dual_port_ram_dualclk (
    input  wire        clk_cpu,     // klok voor CPU
    input  wire        clk_video,   // klok voor video
    input  wire [12:0] cpu_addr,    // CPU schrijfadres
    input  wire [7:0]  cpu_din,     // CPU data in
    input  wire        cpu_we,      // CPU write enable
    input  wire [12:0] video_addr,  // Video leesadres
    output reg [7:0]   video_dout   // Video data out
);

    // 8 KB geheugen
    reg [7:0] mem [0:8191];

    // ====== INIT vanuit bestand ======
    initial begin
        $readmemh("../asm/zx_jetpac.hex", mem);
        // of: $readmemb("beeld.bin", mem);
    end

    // CPU schrijven
    always @(posedge clk_cpu) begin
        if (cpu_we)
            mem[cpu_addr] <= cpu_din;
    end

    // Video lezen
    always @(posedge clk_video) begin
        video_dout <= mem[video_addr];
    end

endmodule
