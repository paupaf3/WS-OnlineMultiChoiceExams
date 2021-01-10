package server;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import common.ProfessorServer;
import common.StudentClient;
import exam.Exam;
import exam.ExamBuilderCSV;
import exam.Question;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.rmi.ConnectException;
import java.rmi.RemoteException;
import java.rmi.UnmarshalException;
import java.rmi.server.UnicastRemoteObject;
import java.text.Format;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.StringTokenizer;


public class ProfessorServerImpl extends UnicastRemoteObject implements ProfessorServer {

    private Exam exam;
    private HashMap<String, StudentClient> students;
    private HashMap<String, Exam> studentExam;
    private boolean canRegistry;
    private boolean examInProgress;
    private Integer studentsNumber;
    private String studentRequest;
    private Integer examsInProgress;
    private boolean studentReconnecting;
    private String examID;

    public ProfessorServerImpl() throws RemoteException {
        super();
        this.students = new HashMap<>();
        this.studentExam = new HashMap<>();
        this.canRegistry = true;
        this.studentsNumber = 0;
        this.examsInProgress = 0;
        this.examInProgress = true;
        this.studentReconnecting = false;
    }

    public void uploadExam(String path) throws IOException, UnirestException {
        Format f = new SimpleDateFormat("HH:mm:ss");
        String hour = f.format(new Date());
        f = new SimpleDateFormat("yyyy-MM-dd");
        String date = f.format(new Date());

        Unirest.setTimeouts(0, 0);
        HttpResponse<String> response = Unirest.post("http://localhost:8000/api/exam/upload/")
                .field("description", "exam")
                .field("time", hour)
                .field("date", date)
                .field("location", "cv.udl.cat/exams")
                .field("exam_file", new File(path))
                .asString();
        Unirest.shutdown();

        StringTokenizer st = new StringTokenizer(response.getBody() , ":,{}");
        st.nextToken();
        this.examID = st.nextToken();

        this.exam = ExamBuilderCSV.build(path);
    }

    public void stopRegister() {
        this.canRegistry = false;
    }

    public synchronized void examFinished(String studentRequest) throws RemoteException {
        try {
            this.students.get(studentRequest).examFinished(this.studentExam.get(studentRequest).getGrade(), "You finished the exam.");
        } catch (UnmarshalException ignored) {}
    }

    public synchronized void nextQuestion(String studentId) throws RemoteException {
        this.students.get(studentId).sendQuestion(this.studentExam.get(studentId).nextQuestion());
    }

    public void previousQuestion(String studentId) throws RemoteException {
        if (this.studentExam.get(studentId).hasPrevious()) {
            this.students.get(studentId).sendQuestion(this.studentExam.get(studentId).previousQuestion());
        } else {
            this.students.get(studentId).sendQuestion(this.studentExam.get(studentId).nextQuestion());
        }
        this.studentReconnecting = false;
    }

    public void startExam() throws RemoteException {
        for (HashMap.Entry<String, StudentClient> studentSet  : this.students.entrySet()) {
            String studentId = studentSet.getKey();
            StudentClient student = studentSet.getValue();
            try {
                student.startExam("The exam starts now.");
                student.sendQuestion(this.studentExam.get(studentId).nextQuestion());
                this.examsInProgress++;
            } catch (ConnectException ignored) {}
        }
    }

    public String getStudentId() {
        return this.studentRequest;
    }

    public synchronized boolean studentHasFinished(String studentId) {
        if (!this.studentExam.get(studentId).hasNext()) {
            this.examsInProgress--;
            return true;
        }
        return false;
    }

    public void examFinished() throws RemoteException {
        for (HashMap.Entry<String, StudentClient> studentSet  : this.students.entrySet()) {
            String studentId = studentSet.getKey();
            StudentClient student = studentSet.getValue();
            try {
                student.examFinished(this.studentExam.get(studentId).getGrade(),"The exam was finished.");
            } catch (ConnectException | UnmarshalException ignored) {}
        }
    }

    public boolean studentsFinished() {
        return this.examsInProgress == 0;
    }

    public HashMap<String, Exam> getStudentsExams() {
        return this.studentExam;
    }

    @Override
    public synchronized void registerStudent(StudentClient client, String studentId) throws IOException {
        URL url = new URL ("http://127.0.0.1:8000/api/user/validate/" + studentId);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String validation = br.readLine();
        conn.disconnect();

        if (validation.equals("true")) {
            if (this.canRegistry) {
                this.students.put(studentId, client);
                this.studentsNumber += 1;
                ServerMessages.studentJoined(studentId, this.studentsNumber);
                this.studentExam.put(studentId, this.exam.copy());
            } else if (this.students.containsKey(studentId)) {
                this.students.put(studentId, client);
                this.studentRequest = studentId;
                this.studentReconnecting = true;
                notify();
            } else {
                client.registerExpired("The registration time has expired.");
                ServerMessages.studentTriedToJoin(studentId);
            }
        } else {
            System.out.println("Student with id: " + studentId + " tried to join the exam");
            client.registerExpired("You are not registered");
        }

    }

    @Override
    public synchronized void sendAnswer(String studentId, Question question) throws RemoteException {
        if (this.examInProgress) {
            this.studentExam.get(studentId).answer(question);
            this.studentRequest = studentId;
        }
        notify();
    }

    public synchronized void reconectStudent(String studentRequest) throws RemoteException {
        this.students.get(studentRequest).reconnectStudent();
    }

    public synchronized boolean isStudentReconnecting() {
        return this.studentReconnecting;
    }

    public void postExam(String path) throws UnirestException, IOException {
        for (HashMap.Entry<String, StudentClient> studentSet  : this.students.entrySet()) {
            String studentId = studentSet.getKey();
            Unirest.setTimeouts(0, 0);
            HttpResponse<String> response = Unirest.post("http://localhost:8000/api/grade/upload/")
                    .field("exam", this.examID)
                    .field("user", studentId)
                    .field("grade_file", new File(path))
                    .asString();
            Unirest.shutdown();
        }
    }
}
