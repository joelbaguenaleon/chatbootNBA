package interfaz;

import javax.swing.SwingUtilities;

public class Main {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            VentanaChatbotNBA ventana = new VentanaChatbotNBA();
            ventana.setVisible(true);
        });
    }
}


