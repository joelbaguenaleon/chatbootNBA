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

/**
 * Interfaz gráfica desarrollada con Java Swing que se comunica
 * con un backend en Python mediante una API local.
 * Funcionalidades:
 * - Chat interactivo 
 * - Conexión automática con backend
 * - Envío asíncrono de mensajes
 */
