package interfaz;

import javax.swing.ImageIcon;
import java.io.File;
import java.awt.BorderLayout;
import javax.swing.Box;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Insets;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;
import javax.swing.UIManager;
import javax.swing.border.EmptyBorder;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;
import javax.swing.JTextField;
import java.awt.GridLayout;

public class VentanaChatbotNBA extends JFrame {

    private final ClienteApi clienteApi;
    private JPanel panelMensajes;
    private JScrollPane scrollMensajes;
    private JTextField txtCampo;
    private JButton btnEnviar;
    private JButton btnLimpiar;
    private JLabel lblEstado;

    public VentanaChatbotNBA() {  //crea interfaz, backend y funcionalidades
        this.clienteApi = new ClienteApi();

        configurarVentana();		//diseño interfaz
        lanzarBackendSimple(); 		//arrancar el backend
        inicializarComponentes();	//funcionalidades
        
        agregarMensajeBot("Hola. Soy tu asistente NBA. Puedes preguntarme por equipos, jugadores, partidos o clasificación.");
    }

    private void configurarVentana() {	//diseño interfaz
        setTitle("Chatbot NBA");
        setSize(820, 620);
        setMinimumSize(new Dimension(700, 500));
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        ImageIcon icono = new ImageIcon(getClass().getResource("/nba.png")); //icono app
        setIconImage(icono.getImage());
    }
    
    private void lanzarBackendSimple() {  //arrancar backend
    	try {
            File archivo = new File("backend/api.exe");

            if (archivo.exists()) {
                new ProcessBuilder(archivo.getAbsolutePath()).start();
            } else {
                System.out.println("No se encontró el backend en: " + archivo.getAbsolutePath());
            }

        } catch (Exception e) {
            System.out.println("Error al lanzar backend: " + e.getMessage());
        
    }}

    private void inicializarComponentes() { 	//funcionalidades del chat
        JPanel contenedor = new JPanel(new BorderLayout());
        contenedor.setBackground(new Color(236, 239, 241));
        setContentPane(contenedor);
        contenedor.add(crearZonaChat(), BorderLayout.CENTER);
        contenedor.add(crearZonaEntrada(), BorderLayout.SOUTH);
        contenedor.add(crearCabecera(), BorderLayout.NORTH);
    }

    private JPanel crearCabecera() { //diseño parte de arriba de la app
        JPanel cabecera = new JPanel(new BorderLayout());
        cabecera.setBackground(new Color(7, 94, 84));
        cabecera.setBorder(new EmptyBorder(12, 16, 12, 16));

        JLabel lblTitulo = new JLabel("Asistente de ayuda NBA");
        lblEstado = new JLabel("Listo"); //pestaña de listo
        lblTitulo.setForeground(Color.WHITE);
        lblTitulo.setFont(new Font("SansSerif", Font.BOLD, 22));
        cabecera.add(lblTitulo, BorderLayout.WEST);
        lblEstado.setForeground(new Color(220, 255, 220));
        lblEstado.setFont(new Font("SansSerif", Font.PLAIN, 13));
        //cabecera.add(lblEstado, BorderLayout.EAST);  //pestaña de listo, descomentar si se quiere añadir funcionalidad

        return cabecera;
    }

    private JScrollPane crearZonaChat() {	//historial menajes+scroll del chat
        panelMensajes = new JPanel();
        panelMensajes.setLayout(new BoxLayout(panelMensajes, BoxLayout.Y_AXIS));
        panelMensajes.setBackground(new Color(229, 221, 213));
        panelMensajes.setBorder(new EmptyBorder(15, 15, 15, 15));
        scrollMensajes = new JScrollPane(panelMensajes);
        scrollMensajes.setBorder(null);
        scrollMensajes.getVerticalScrollBar().setUnitIncrement(16);

        return scrollMensajes;
    }

    private JPanel crearZonaEntrada() {
        JPanel panelInferior = new JPanel(new BorderLayout(8, 0));
        panelInferior.setBackground(new Color(240, 242, 245));
        panelInferior.setBorder(new EmptyBorder(10, 12, 10, 12));

        txtCampo = new JTextField();
        txtCampo.setFont(new Font("SansSerif", Font.PLAIN, 14));
        txtCampo.setPreferredSize(new Dimension(100, 34));
        txtCampo.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(200, 200, 200), 1),
                BorderFactory.createEmptyBorder(6, 10, 6, 10)
        ));

        JPanel panelBotones = new JPanel(new GridLayout(2, 1, 0, 6));
        panelBotones.setBackground(new Color(240, 242, 245));

        btnEnviar = new JButton("Enviar");
        btnLimpiar = new JButton("Limpiar");

        Font fuenteBoton = new Font("SansSerif", Font.PLAIN, 12);
        btnEnviar.setFont(fuenteBoton);
        btnLimpiar.setFont(fuenteBoton);

        btnEnviar.setFocusPainted(false);
        btnLimpiar.setFocusPainted(false);

        btnEnviar.setBackground(new Color(37, 211, 102));
        btnEnviar.setForeground(Color.BLACK);

        btnEnviar.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        btnLimpiar.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));

        Dimension tamBoton = new Dimension(92, 30);
        btnEnviar.setPreferredSize(tamBoton);
        btnLimpiar.setPreferredSize(tamBoton);

        panelBotones.add(btnEnviar);
        panelBotones.add(btnLimpiar);

        panelInferior.add(txtCampo, BorderLayout.CENTER);
        panelInferior.add(panelBotones, BorderLayout.EAST);

        btnEnviar.addActionListener(e -> {
            String mensaje = txtCampo.getText().trim();
            if (!mensaje.isEmpty()) {
                enviarMensajeDesdeCampo(txtCampo, mensaje);
            }
        });

        btnLimpiar.addActionListener(e -> limpiarChat());

        txtCampo.addActionListener(e -> {
            String mensaje = txtCampo.getText().trim();
            if (!mensaje.isEmpty()) {
                enviarMensajeDesdeCampo(txtCampo, mensaje);
            }
        });

        return panelInferior;
    }

    private void enviarMensajeDesdeCampo(JTextField txtCampo, String mensaje) { //envia mensaje de usuario a peticion de backend
        agregarMensajeUsuario(mensaje);
        txtCampo.setText("");
        txtCampo.requestFocus();

        btnEnviar.setEnabled(false);
        lblEstado.setText("Consultando...");
        JLabel indicador = agregarIndicadorEscribiendo();

        SwingWorker<String, Void> worker = new SwingWorker<>() {
            @Override
            protected String doInBackground() throws Exception {
                return clienteApi.enviarPregunta(mensaje);
            }

            @Override
            protected void done() {
                quitarIndicadorEscribiendo(indicador);

                try {
                    String respuesta = get();
                    agregarMensajeBot(respuesta);
                    lblEstado.setText("Listo");
                } catch (Exception ex) {
                    agregarMensajeBot("Error al conectar con la API: " + obtenerMensajeRaiz(ex));
                    lblEstado.setText("Sin conexión");
                } finally {
                    btnEnviar.setEnabled(true);
                }
            }
        };

        worker.execute();
    }

    private void limpiarChat() {  //vaciar historial de la converación 
        panelMensajes.removeAll();
        panelMensajes.revalidate();
        panelMensajes.repaint();
        agregarMensajeBot("Chat reiniciado. Escribe una nueva consulta.");
        lblEstado.setText("Listo");
        txtCampo.requestFocus();
    }

    private void agregarMensajeUsuario(String texto) { //añade mensajes de usuario al chat
        agregarMensaje(texto, true);
    }

    private void agregarMensajeBot(String texto) { //añade respuestas del bot al chat
        agregarMensaje(texto, false);
    }

    private void agregarMensaje(String texto, boolean esUsuario) {
        JPanel fila = new JPanel(new FlowLayout(esUsuario ? FlowLayout.RIGHT : FlowLayout.LEFT));
        fila.setOpaque(false);
        fila.setAlignmentX(Component.LEFT_ALIGNMENT);

        JTextPane burbuja = crearBurbuja(texto, esUsuario);
        fila.add(burbuja);

        panelMensajes.add(fila);
        panelMensajes.add(Box.createVerticalStrut(8));

        refrescarChat();
    }

    private JTextPane crearBurbuja(String texto, boolean esUsuario) { //define el color del mensaje de cada uno
        JTextPane pane = new JTextPane();
        pane.setEditable(false);
        pane.setOpaque(true);
        pane.setFont(new Font("SansSerif", Font.PLAIN, 15));
        pane.setBorder(new EmptyBorder(10, 12, 10, 12));
        pane.setMargin(new Insets(0, 0, 0, 0));

        if (esUsuario) {
            pane.setBackground(new Color(220, 248, 198));
        } else {
            pane.setBackground(Color.WHITE);
        }

        pane.setForeground(Color.BLACK);

        StyledDocument doc = pane.getStyledDocument();
        SimpleAttributeSet attrs = new SimpleAttributeSet();
        StyleConstants.setLineSpacing(attrs, 0.15f);
        StyleConstants.setLeftIndent(attrs, 0);
        StyleConstants.setRightIndent(attrs, 0);

        pane.setText(texto);
        doc.setParagraphAttributes(0, doc.getLength(), attrs, false);

        int anchoMax = 420;
        pane.setSize(new Dimension(anchoMax, Short.MAX_VALUE));
        Dimension pref = pane.getPreferredSize();
        pane.setPreferredSize(new Dimension(Math.min(pref.width, anchoMax), pref.height + 4));

        return pane;
    }

    private JLabel agregarIndicadorEscribiendo() { //replica el escribiendo cuando app tarda en responder
        JPanel fila = new JPanel(new FlowLayout(FlowLayout.LEFT));
        fila.setOpaque(false);
        fila.setAlignmentX(Component.LEFT_ALIGNMENT);

        JLabel lbl = new JLabel("Escribiendo...");
        lbl.setFont(new Font("SansSerif", Font.ITALIC, 13));
        lbl.setForeground(Color.DARK_GRAY);

        fila.add(lbl);
        panelMensajes.add(fila);
        panelMensajes.add(Box.createVerticalStrut(8));

        refrescarChat();
        return lbl;
    }

    private void quitarIndicadorEscribiendo(JLabel lbl) {
        if (lbl == null) {
            return;
        }

        Component fila = lbl.getParent();
        int index = -1;

        for (int i = 0; i < panelMensajes.getComponentCount(); i++) {
            if (panelMensajes.getComponent(i) == fila) {
                index = i;
                break;
            }
        }

        if (index >= 0) {
            panelMensajes.remove(index);
            if (index < panelMensajes.getComponentCount()) {
                panelMensajes.remove(index);
            }
        }

        refrescarChat();
    }

    private void refrescarChat() {
        panelMensajes.revalidate();
        panelMensajes.repaint();

        SwingUtilities.invokeLater(() -> {
            JScrollPane scroll = scrollMensajes;
            scroll.getVerticalScrollBar().setValue(scroll.getVerticalScrollBar().getMaximum());
        });
    }

    private String obtenerMensajeRaiz(Exception e) {
        Throwable t = e;
        while (t.getCause() != null) {
            t = t.getCause();
        }

        String msg = t.getMessage();
        return (msg == null || msg.isBlank()) ? t.toString() : msg;
    }
}