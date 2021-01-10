package exam;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ExamTest {

    private Exam exam;

    @BeforeEach
    public void beforeEach() throws IOException {
        this.exam = ExamBuilderCSV.build("exam.csv");
    }
    /*
    @Test
    public void testExam() {
        Question question = exam.nextQuestion();
        question.answer(1);
        exam.answer(question);
        assertEquals(1, this.exam.getGrade());

        question = exam.nextQuestion();
        question.answer(2);
        exam.answer(question);
        assertEquals(1, exam.getGrade());

        question = exam.nextQuestion();
        question.answer(1);
        exam.answer(question);
        assertEquals(2, exam.getGrade());
    }*/
}