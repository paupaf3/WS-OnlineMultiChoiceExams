package server;

import exam.Exam;

import java.util.HashMap;

public class ExamThread extends Thread {

    private ProfessorServerImpl server;

    public ExamThread(ProfessorServerImpl server) {
        this.server = server;
    }

    @Override
    public void run() {
        try {
            while (!this.server.studentsFinished()) {
                synchronized (this.server) {
                    this.server.wait();
                    String studentRequest = this.server.getStudentId();
                    if (this.server.isStudentReconnecting()) {
                        this.server.reconectStudent(studentRequest);
                        this.server.previousQuestion(studentRequest);
                    }else if (!this.server.studentHasFinished(studentRequest)) {
                        this.server.nextQuestion(studentRequest);
                    } else {
                        this.server.examFinished(studentRequest);
                    }
                }
            }
            ServerMessages.allStudentsFinished();

        } catch (InterruptedException e) {
            ServerMessages.examFinished();
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
        }
    }

    public HashMap<String, Exam> finishExam() {
        return this.server.getStudentsExams();
    }
}
