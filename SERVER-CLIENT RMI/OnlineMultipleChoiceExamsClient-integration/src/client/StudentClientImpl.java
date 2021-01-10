package client;

import common.ProfessorServer;
import common.StudentClient;
import exam.Question;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.Scanner;

public class StudentClientImpl extends UnicastRemoteObject implements StudentClient {

    private Scanner scanner;
    private String studentId;
    private boolean examInProgress;
    private Question question;

    public StudentClientImpl(String studentId, ProfessorServer server) throws RemoteException {
        super();
        this.studentId = studentId;
        this.scanner = new Scanner(System.in);
        this.examInProgress = true;
    }

    @Override
    public synchronized void startExam(String message) {
        ClientMessages.sendMessage(message);
        notify();
    }

    @Override
    public synchronized void sendQuestion(Question question) throws RemoteException {
        ClientMessages.sendQuestion(question);
        this.question = question;
        notify();
    }

    @Override
    public void examFinished(int grade, String message) {
        this.examInProgress = false;
        ClientMessages.examFinished(grade, message);
    }

    @Override
    public void registerExpired(String message) {
        ClientMessages.sendMessage(message);
    }

    public Question getAnswer() {
        Integer answer;
        do {
            ClientMessages.yourAnswer();
            answer = this.scanner.nextInt();
            if (!this.question.validQuestion(answer)) {
                ClientMessages.answerNotValid();
            }
        } while (!this.question.validQuestion(answer));
        this.question.answer(answer);
        return this.question;
    }

    @Override
    public synchronized void reconnectStudent() throws RemoteException {
        ClientMessages.studentReconnected();
        notify();
    }
}
