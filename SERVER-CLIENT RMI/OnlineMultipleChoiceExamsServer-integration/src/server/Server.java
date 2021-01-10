package server;

import exam.Exam;
import exam.StoreExam;

import java.awt.*;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.HashMap;
import java.util.Scanner;

import java.net.*;
import java.io.*;

public class Server {

    public static void main(String[] args) throws IOException {
        new Server().run();
        System.exit(0);
    }

    private void run() throws IOException {

        Scanner scanner;
        ProfessorServerImpl server;
        String in;
        scanner = new Scanner(System.in);

        try {
            Registry registry = startRegistry(null);
            server = new ProfessorServerImpl();
            registry.bind("exam", server);

            ServerMessages.serverStart();
            String examPath = scanner.nextLine();
            server.uploadExam(examPath);



            ServerMessages.studentsRegister();

            do {
                in = scanner.nextLine();
            } while (!in.equals("s"));

            server.stopRegister();
            server.startExam();

            ExamThread examThread = new ExamThread(server);
            examThread.start();

            ServerMessages.examStart();

            do {
                in = scanner.nextLine();
            } while (!in.equals("c"));
            examThread.interrupt();

            server.examFinished();
            HashMap<String, Exam> exams = examThread.finishExam();
            ServerMessages.examStop();

            StoreExam.storeExam("grades.csv", exams);
            server.postExam("grades.csv");

        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString()); e.printStackTrace();
        }
    }

    private Registry startRegistry(Integer port) throws RemoteException {
        if (port == null) port = 1099;
        try {
            Registry registry = LocateRegistry.getRegistry(port);
            registry.list();
            return registry;
        } catch (RemoteException ex) {
            Registry registry = LocateRegistry.createRegistry(port);
            return registry;
        }
    }
}
