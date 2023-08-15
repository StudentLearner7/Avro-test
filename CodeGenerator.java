public class Main {
    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        cfg.setClassForTemplateLoading(Main.class, "/");
        
        // Example: Employee class
        Class<?> entityClass = Employee.class; // Change this to test other entities
        String entityName = entityClass.getSimpleName();

        // Identify the non-primitive fields
        List<Map<String, Object>> fields = new ArrayList<>();
        Set<String> nonPrimitiveFieldTypes = new HashSet<>();
        for (Field field : entityClass.getDeclaredFields()) {
            String fieldType = field.getType().getSimpleName();
            String fieldName = field.getName();
            fields.add(Map.of("name", fieldName, "type", fieldType));
            if (isNonPrimitive(field.getType())) {
                nonPrimitiveFieldTypes.add(fieldType);
            }
        }
        
        // Create the data-model
        Map<String, Object> data = new HashMap<>();
        data.put("entityName", entityName);
        data.put("fields", fields);
        data.put("nonPrimitiveFieldTypes", nonPrimitiveFieldTypes);

        // Process DTO template
        processTemplate(cfg, "dto.ftl", data);
        
        // Process Service template
        processTemplate(cfg, "service.ftl", data);
    }

    private static boolean isNonPrimitive(Class<?> type) {
        return !type.isPrimitive() && !type.getName().startsWith("java.lang");
    }

    private static void processTemplate(Configuration cfg, String templateName, Map<String, Object> data) throws Exception {
        Template temp = cfg.getTemplate(templateName);
        Writer out = new OutputStreamWriter(System.out);
        temp.process(data, out);
        out.flush();
        System.out.println(); // Line break between templates
    }
}
