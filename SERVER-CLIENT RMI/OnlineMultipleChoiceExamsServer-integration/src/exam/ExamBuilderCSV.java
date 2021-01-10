package exam;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class ExamBuilderCSV {
    public static Exam build(String path) throws IOException {
        List<Question> questions = new ArrayList<>();
        HashMap<Integer, Integer> answers = new HashMap<>();

        BufferedReader csvReader = new BufferedReader(new FileReader(path));
        String row;
        String[] data;

        while ((row = csvReader.readLine()) != null) {
            data = row.split(";");

            Integer questionNumber = questions.size() + 1;
            String statement = data[0];
            List<String> choices = new ArrayList<>(Arrays.asList(data).subList(1, data.length - 1));

            Question question = new Question(questionNumber, statement, choices);
            answers.put(questionNumber, Integer.parseInt(data[data.length - 1]));
            questions.add(question);
        }

        return new Exam(questions, answers);
    }
}
