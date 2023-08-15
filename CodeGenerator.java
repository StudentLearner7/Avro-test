import freemarker.template.*;
import org.reflections.Reflections;

import java.io.*;
import java.lang.reflect.Field;
import java.util.*;
import java.util.stream.Collectors;

public class CodeGenerator {

    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        cfg.setDirectoryForTemplateLoading(new File("path/to/your/templates"));
        cfg.setDefaultEncoding("UTF-8");
        cfg.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);

        // Define the package that contains your entity classes
        String entityPackage = "com.your.package.entities";

        // Use Reflections to find all classes in the package
        Reflections reflections = new Reflections(entityPackage);
        Set<Class<?>> entityClasses = reflections.getTypesAnnotatedWith(javax.persistence.Entity.class);

        // Process templates for each entity class
        for (Class<?> entityClass : entityClasses) {
            String entityName = entityClass.getSimpleName();

            List<Map<String, String>> fields = Arrays.stream(entityClass.getDeclaredFields())
                    .map(field -> {
                        Map<String, String> fieldInfo = new HashMap<>();
                        fieldInfo.put("name", field.getName());
                        fieldInfo.put("type", field.getType().getSimpleName());
                        return fieldInfo;
                    })
                    .collect(Collectors.toList());

            Map<String, Object> root = new HashMap<>();
            root.put("entityName", entityName);
            root.put("fields", fields);

            // Process the DTO template
            Template dtoTemplate = cfg.getTemplate("dto.ftl");
            try (Writer out = new FileWriter("output/" + entityName + "DTO.java")) {
                dtoTemplate.process(root, out);
            }

            // Process the Service template
            Template serviceTemplate = cfg.getTemplate("service.ftl");
            try (Writer out = new FileWriter("output/" + entityName + "Service.java")) {
                serviceTemplate.process(root, out);
            }
        }
    }
}
