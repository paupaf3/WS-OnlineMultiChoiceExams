package client;

import common.*;
import exam.Question;

import javax.rmi.ssl.SslRMIClientSocketFactory;
import java.awt.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Objects;
import java.util.Scanner;

public class Client {

    private Scanner scanner;
    private StudentClientImpl client;
    private ProfessorServer server;

    public static void main(String[] args) {
        new Client().run(args);
        System.exit(0);
    }

    public void run(String[] args) {
        this.scanner = new Scanner(System.in);
        String host = (args.length < 1) ? null : args[0];
        try {
            Registry registry = LocateRegistry.getRegistry(host);

            ClientMessages.enterId();
            String studentId = this.scanner.nextLine();

            ClientMessages.waitingExam();

            this.server = (ProfessorServer) registry.lookup("exam");
            this.client = new StudentClientImpl(studentId, this.server);

            this.server.registerStudent(client, studentId);

            synchronized (this.client) {
                this.client.wait();
                while (true) {
                    this.client.wait();
                    Question question = this.client.getAnswer();
                    this.server.sendAnswer(studentId, question);
                }
            }
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString()); e.printStackTrace();
        }
    }
}
