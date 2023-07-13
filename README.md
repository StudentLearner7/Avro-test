import org.apache.maven.project.MavenProject;
import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MyClass {
    public static String[] getFullyQualifiedClassNames(MavenProject project, String packageName) {
        String sourceDirectory = project.getCompileSourceRoots().get(0); // Assuming only one source directory

        Path packagePath = Paths.get(packageName.replace('.', File.separator));
        String packageDirectory = sourceDirectory + File.separator + packagePath.toString();

        List<String> classNames = traverseDirectory(new File(packageDirectory), packageName);

        return classNames.toArray(new String[0]);
    }

    private static List<String> traverseDirectory(File directory, String packageName) {
        List<String> classNames = new ArrayList<>();

        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    String newPackageName = packageName + "." + file.getName();
                    classNames.addAll(traverseDirectory(file, newPackageName));
                } else if (file.getName().endsWith(".java")) {
                    String className = packageName + "." + file.getName().replace(".java", "");
                    classNames.add(className);
                }
            }
        }

        return classNames;
    }
}
