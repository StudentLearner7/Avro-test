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

        List<SimpleHash> entities = new ArrayList<>();

        // Example: List of entity classes in EntityFolder
        String[] entityClassNames = {"Employee", "Department"}; // Add your entity class names here

        for (String className : entityClassNames) {
            Class<?> entityClass = Class.forName(className); // Assuming fully qualified class name

            SimpleHash entity = new SimpleHash();
            entity.put("name", className);

            List<SimpleHash> fields = new ArrayList<>();
            for (Field field : entityClass.getDeclaredFields()) {
                SimpleHash fieldMap = new SimpleHash();
                fieldMap.put("name", field.getName());
                fieldMap.put("type", field.getType().getSimpleName());
                fieldMap.put("isPrimitive", isPrimitive(field.getType()));
                fields.add(fieldMap);
            }
            entity.put("fields", new SimpleSequence(fields));
            entities.add(entity);
        }

        // Create the data-model for ModelMapper
        SimpleHash modelMapperData = new SimpleHash();
        modelMapperData.put("entities", new SimpleSequence(entities));

        // Process ModelMapper template
        processTemplate(cfg, "ModelMapper.ftl", modelMapperData);
    }

    private static boolean isPrimitive(Class<?> type) {
        return type.isPrimitive() || type.getName().startsWith("java.lang");
    }

    private static void processTemplate(Configuration cfg, String templateName, TemplateHashModel data) throws Exception {
        Template temp = cfg.getTemplate(templateName);
        Writer out = new OutputStreamWriter(System.out);
        temp.process(data, out);
        out.flush();
        System.out.println(); // Line break between templates
    }
}
