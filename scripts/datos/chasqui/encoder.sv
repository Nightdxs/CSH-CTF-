// Bloque funcional recuperado del FPGA de la estacion de relevo chasqui.
// Codifica nibbles de 4 bits en palabras de 7 bits (Hamming 7,4).

module encoder(
    input  [3:0] data_in,
    output [6:0] data_out
);
    wire p0, p1, p2;

    assign p0 = data_in[3] ^ data_in[2] ^ data_in[0];
    assign p1 = data_in[3] ^ data_in[1] ^ data_in[0];
    assign p2 = data_in[2] ^ data_in[1] ^ data_in[0];

    // Orden de bits de salida: {p0, p1, d3, p2, d2, d1, d0}
    assign data_out = {p0, p1, data_in[3], p2, data_in[2], data_in[1], data_in[0]};
endmodule

// Testbench para probar el codificador.
module main;
    wire [3:0] data_in = 5; // 0101
    wire [6:0] data_out;

    encoder en(data_in, data_out);

    initial begin
        #10;
        $display("%b", data_out); // Imprime la version codificada de 0101
    end
endmodule
