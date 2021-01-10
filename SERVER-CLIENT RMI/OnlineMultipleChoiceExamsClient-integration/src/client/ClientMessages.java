package client;

import exam.Question;

public class ClientMessages {

    public static void sendMessage(String message) {
        System.out.println(message);
    }

    public static void sendQuestion(Question question) {
        System.out.println(question);
    }

    public static void enterId() {
        System.out.print("Enter your student id: ");
    }

    public static void waitingExam() {
        System.out.println("Waiting for the exam to start.");
    }

    public static void yourAnswer() {
        System.out.print("Your answer: ");
    }

    public static void answerNotValid() {
        String notValidAnswer = "This answer is not valid.";
        System.out.println("This answer is not valid.");
    }

    public static void examFinished(int grade,String message) {
        System.out.println("\n" + message);
        System.out.println("Your grade: " + grade);
    }

    public static void studentReconnected() {
        System.out.println("You has reconnected correctly");
    }
}
