package common;

import exam.Question;

import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ProfessorServer extends Remote {
    void registerStudent(StudentClient clien, String studentId) throws IOException;
    void sendAnswer(String studentId, Question question) throws RemoteException;
}
