package common;

import exam.Question;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface StudentClient extends Remote {
    void startExam(String message) throws RemoteException;
    void sendQuestion(Question question) throws RemoteException;
    void examFinished(int grade, String message) throws RemoteException;
    void registerExpired(String message) throws RemoteException;
    void reconnectStudent() throws RemoteException;
}
