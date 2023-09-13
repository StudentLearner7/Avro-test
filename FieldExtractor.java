import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class FieldExtractor {
    public static void main(String[] args) throws IOException {
        File javaFile = new File("YourClass.java"); // Replace with the path to your Java class file
        CompilationUnit compilationUnit = StaticJavaParser.parse(javaFile);

        // Create a visitor to extract private fields
        VoidVisitor<List<FieldDeclaration>> fieldExtractor = new FieldExtractorVisitor();
        List<FieldDeclaration> privateFields = fieldExtractor.visit(compilationUnit, null);

        // Process the private fields
        for (FieldDeclaration field : privateFields) {
            String dataType = field.getVariables().get(0).getType().asString();
            String fieldName = field.getVariables().get(0).getNameAsString();

            // Check if the field is non-primitive and append "DTO" if needed
            if (!isPrimitive(dataType)) {
                dataType = dataType + "DTO";
            }

            // Now, you can pass dataType and fieldName to your FTL template for code generation
            System.out.println("Data Type: " + dataType);
            System.out.println("Field Name: " + fieldName);
        }
    }

    private static boolean isPrimitive(String dataType) {
        return dataType.equals("byte") ||
               dataType.equals("short") ||
               dataType.equals("int") ||
               dataType.equals("long") ||
               dataType.equals("float") ||
               dataType.equals("double") ||
               dataType.equals("char") ||
               dataType.equals("boolean");
    }

    private static class FieldExtractorVisitor extends VoidVisitorAdapter<List<FieldDeclaration>> {
        @Override
        public void visit(FieldDeclaration field, List<FieldDeclaration> collector) {
            // Check if the field is private
            if (field.getModifiers().contains(Modifier.privateModifier())) {
                collector.add(field);
            }
        }
    }
}
