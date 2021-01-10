package exam;

import java.util.*;

public class Exam {

    private final List<Question> questions;
    private final HashMap<Integer, Integer> answers;
    private List<Question> studentAnswers;
    private Integer grade;

    private final ListIterator<Question> itQuestion;

    public Exam(List<Question> questions, HashMap<Integer, Integer> answers) {
        this.questions = questions;
        this.answers = answers;
        this.grade = 0;

        this.studentAnswers = new ArrayList<>();
        this.itQuestion = questions.listIterator();
    }

    private Exam(List<Question> questions, HashMap<Integer,
                 Integer> answers, List<Question> studentAnswers,
                 Integer grade) {
        this.questions = questions;
        this.answers = answers;
        this.studentAnswers = studentAnswers;
        this.grade = grade;
        this.itQuestion = questions.listIterator();
    }

    public Integer getGrade() {
        return this.grade;
    }

    public Question nextQuestion() {
        return this.itQuestion.next();
    }

    public boolean hasNext() {
        return this.itQuestion.hasNext();
    }

    public Question previousQuestion() {
        this.itQuestion.previous();
        return this.itQuestion.next();
    }

    public void answer(Question question) {
        if (correctAnswer(question)) {
            increaseGrade();
        }
    }

    private void increaseGrade() {
        this.grade += 1;
    }

    private boolean correctAnswer(Question question) {
        return this.answers.get(question.getQuestionNumber()).equals(question.getAnswer());
    }

    @Override
    public String toString() {
        return "Exam{" +
                "questions=" + questions +
                ", answers=" + answers +
                ", studentAnswers=" + studentAnswers +
                ", grade=" + grade +
                ", itQuestion=" + itQuestion +
                '}';
    }

    public Exam copy() {
        return new Exam(this.questions, this.answers, this.studentAnswers, this.grade);
    }

    public boolean hasPrevious() {
        return this.itQuestion.hasPrevious();
    }
}
