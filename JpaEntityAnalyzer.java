import java.util.regex.*;
import java.io.*;

public class JpaEntityAnalyzer {

    public static void main(String[] args) {
        try {
            String code = new String(Files.readAllBytes(Paths.get("EntityClass.java")), StandardCharsets.UTF_8);
            findIdAnnotations(code);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void findIdAnnotations(String code) {
        Pattern pattern = Pattern.compile("@Id\\s+private\\s+([\\w\\.]+)\\s+(\\w+);");
        Matcher matcher = pattern.matcher(code);

        while (matcher.find()) {
            String dataType = matcher.group(1);
            String fieldName = matcher.group(2);
            System.out.println("Field: " + fieldName + ", Data Type: " + dataType);
        }
    }
}
