 private static String readEntityFileContent(String entityName) {
        String filePath = "path/to/original/entities/" + entityName + ".java";
        try {
            return new String(Files.readAllBytes(Paths.get(filePath)));
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    private static String generateModifiedEntityContent(String packageName, String existingContent) {
        StringBuilder modifiedContent = new StringBuilder();
        modifiedContent.append("package ").append(packageName).append(";\n\n");
        modifiedContent.append(existingContent);
        return modifiedContent.toString();
    }
