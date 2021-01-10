package common;

import exam.Question;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ProfessorServer extends Remote {
    void registerStudent(StudentClient client, String studentId) throws IOException;
    void sendAnswer(String studentId, Question question) throws RemoteException;
}
