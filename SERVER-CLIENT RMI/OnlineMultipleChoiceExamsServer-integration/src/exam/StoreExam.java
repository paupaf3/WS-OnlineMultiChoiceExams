package exam;

import common.StudentClient;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class StoreExam {

    public static void storeExam(String path, HashMap<String, Exam> studentExam) {

        FileWriter fw;

        try {
            fw = new FileWriter(path);
            BufferedWriter bw = new BufferedWriter(fw);
            String line;

            for(Map.Entry<String, Exam> student : studentExam.entrySet()) {
                String studentId = student.getKey();
                String grade = Integer.toString(student.getValue().getGrade());
                line = studentId + ";" + grade + "\n";
                bw.write(line);
            }

            bw.close();
            fw.close();

        } catch (IOException e){
            e.printStackTrace();
        }
    }
}
