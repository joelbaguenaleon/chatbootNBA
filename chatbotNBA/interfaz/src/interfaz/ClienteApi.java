package interfaz;

import java.io.IOException;
import java.net.ConnectException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public class ClienteApi {

    private static final String URL_API = "http://127.0.0.1:8000/preguntar"; //url api local cx con HTTP
    private final HttpClient client;										 //url tiene que coincidir con api, en caso de cambio modificar

    public ClienteApi() {
        this.client = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(Duration.ofSeconds(5))
                .build();
    }
    /**
     * Envía una pregunta al backend y devuelve la respuesta del chatbot.
     * @param pregunta Texto introducido por el usuario
     * @return Respuesta del backend
     * @throws Exception si ocurre un error de cx 
     */
    public String enviarPregunta(String pregunta) throws IOException, InterruptedException {
        String json = "{\"texto\":\"" + escaparJson(pregunta) + "\"}"; //JSON a partir de texto escrito en chat

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(URL_API))
                .timeout(Duration.ofSeconds(20))
                .header("Content-Type", "application/json; charset=UTF-8")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json, StandardCharsets.UTF_8))
                .build();

        try { //leer api y extraer respuesta
            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            int status = response.statusCode();
            String body = response.body();

            if (status != 200) {
                throw new IOException("Error HTTP " + status + ": " + body);
            }

            String respuesta = extraerCampoRespuesta(body);

            if (respuesta == null || respuesta.isBlank()) {
                return "No se pudo leer la respuesta de la API.\n\nRespuesta completa:\n" + body;
            }

            return respuesta;

        } catch (ConnectException e) {
            throw new IOException("No se pudo conectar con la API. Asegúrate de que Python está arrancado.", e);
        }
    }

    private String escaparJson(String texto) {
        return texto
                .replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    private String extraerCampoRespuesta(String json) {
        String clave = "\"respuesta\":";
        int inicioClave = json.indexOf(clave);

        if (inicioClave == -1) {
            return null;
        }

        int inicioComillas = json.indexOf("\"", inicioClave + clave.length());
        if (inicioComillas == -1) {
            return null;
        }

        StringBuilder resultado = new StringBuilder();
        boolean escape = false;

        for (int i = inicioComillas + 1; i < json.length(); i++) {
            char c = json.charAt(i);

            if (escape) {
                switch (c) {
                    case 'n':
                        resultado.append('\n');
                        break;
                    case 'r':
                        resultado.append('\r');
                        break;
                    case 't':
                        resultado.append('\t');
                        break;
                    case '"':
                        resultado.append('"');
                        break;
                    case '\\':
                        resultado.append('\\');
                        break;
                    default:
                        resultado.append(c);
                        break;
                }
                escape = false;
            } else {
                if (c == '\\') {
                    escape = true;
                } else if (c == '"') {
                    return resultado.toString();
                } else {
                    resultado.append(c);
                }
            }
        }

        return null;
    }
}