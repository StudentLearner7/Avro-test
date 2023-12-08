package org.example;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import java.util.*;
import java.util.regex.*;

import java.util.*;
import java.util.regex.*;

import java.util.*;
import java.util.regex.*;

import java.util.*;
import java.util.regex.*;

public class JDLParser {
    public static void main(String[] args) {
        // Replace 'jdlInput' with your JDL input string
        String jdlInput = "entity Region {\n" +
                "\tregionName String\n" +
                "}\n" +
                "\n" +
                "entity Country {\n" +
                "\tcountryName String\n" +
                "}\n" +
                "\n" +
                "// an ignored comment\n" +
                "/** not an ignored comment */\n" +
                "entity Location {\n" +
                "\tstreetAddress String\n" +
                "\tpostalCode String\n" +
                "\tcity String\n" +
                "\tstateProvince String\n" +
                "}";


        JDLParser parser = new JDLParser();
        List<String> classDefinitions = parser.parseJDL(jdlInput);

        // Print Java class definitions
        for (String classDefinition : classDefinitions) {
            System.out.println(classDefinition);
        }
    }

    public List<String> parseJDL(String jdlInput) {
        List<String> classDefinitions = new ArrayList<>();

        // Regular expressions to match entity definitions
        Pattern entityPattern = Pattern.compile("entity\\s+(\\w+)\\s*\\{([^}]+)\\}", Pattern.DOTALL);
        Pattern attributePattern = Pattern.compile("(\\w+)\\s+(\\w+)(\\s+([\\w<>]+))?(\\s+(\\w+))?");

        Matcher entityMatcher = entityPattern.matcher(jdlInput);

        while (entityMatcher.find()) {
            String entityName = entityMatcher.group(1);
            String attributesText = entityMatcher.group(2);

            StringBuilder classDefinition = new StringBuilder();
            classDefinition.append("public class ").append(entityName).append(" {\n");

            Matcher attributeMatcher = attributePattern.matcher(attributesText);

            while (attributeMatcher.find()) {
                String jdlType = attributeMatcher.group(1);
                String name = attributeMatcher.group(2);
                String genericType = attributeMatcher.group(4);
                String modifier = attributeMatcher.group(6);

                String javaType = mapJDLTypeToJavaType(jdlType);

                if (genericType != null) {
                    javaType = javaType + "<" + mapJDLTypeToJavaType(genericType) + ">";
                }

                classDefinition.append("    private ");

                if (modifier != null && modifier.equals("required")) {
                    classDefinition.append(javaType).append(" ").append(name).append(";\n");
                } else {
                    classDefinition.append(javaType).append(" ").append(name).append(";\n");
                }
            }

            classDefinition.append("}\n");
            classDefinitions.add(classDefinition.toString());
        }

        return classDefinitions;
    }

    private String mapJDLTypeToJavaType(String jdlType) {
        switch (jdlType) {
            case "String":
                return "String";
            case "Integer":
                return "Integer";
            case "Long":
                return "Long";
            case "Instant":
                return "Instant";
            // Add more type mappings as needed
            default:
                return "UnknownType";
        }
    }
}

