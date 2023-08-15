import freemarker.template.*;
import java.io.*;
import java.lang.reflect.Field;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        cfg.setClassForTemplateLoading(Main.class, "/");
        cfg.setDefaultEncoding("UTF-8");
        cfg.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);
        cfg.setLogTemplateExceptions(false);
        cfg.setWrapUncheckedExceptions(true);

        // Using DefaultObjectWrapper
        DefaultObjectWrapper wrapper = new DefaultObjectWrapperBuilder(Configuration.VERSION_2_3_31).build();
        cfg.setObjectWrapper(wrapper);

        List<Map<String, Object>> entities = new ArrayList<>();

        // Example: List of entity classes in EntityFolder
        String[] entityClassNames = {"Employee", "Department"}; // Add your entity class names here

        for (String className : entityClassNames) {
            Class<?> entityClass = Class.forName(className); // Assuming fully qualified class name

            Map<String, Object> entity = new HashMap<>();
            entity.put("name", className);

            List<Map<String, Object>> fields = new ArrayList<>();
            for (Field field : entityClass.getDeclaredFields()) {
                Map<String, Object> fieldMap = new HashMap<>();
                fieldMap.put("name", field.getName());
                fieldMap.put("type", field.getType().getSimpleName());
                fieldMap.put("isPrimitive", isPrimitive(field.getType()));
                fields.add(fieldMap);
            }
            entity.put("fields", fields);
            entities.add(entity);
        }

        // Create the data-model for ModelMapper
        Map<String, Object> modelMapperData = new HashMap<>();
        modelMapperData.put("entities", entities);

        // Process ModelMapper template
        processTemplate(cfg, "ModelMapper.ftl", modelMapperData);
    }

    private static boolean isPrimitive(Class<?> type) {
        return type.isPrimitive() || type.getName().startsWith("java.lang");
    }

    private static void processTemplate(Configuration cfg, String templateName, Map<String, Object> data) throws Exception {
        Template temp = cfg.getTemplate(templateName);
        Writer out = new OutputStreamWriter(System.out);
        temp.process(data, out);
        out.flush();
        System.out.println(); // Line break between templates
    }
}
