package com.example.demo;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class UpdatePackageAndMoveFiles {
    public static void main(String[] args) {
        String packageName = "com.example.entities"; // Replace with your desired package name
        String sourceDirectoryPath = "src/main/java"; // Replace with the path to your source files
        String targetDirectoryPath = sourceDirectoryPath + "/" + packageName.replace('.', '/');

        try {
            // Get all Java file paths in the source package directory
            String packagePath = packageName.replace('.', '/');
            File packageDirectory = new File(sourceDirectoryPath, packagePath);
            String[] javaFileNames = packageDirectory.list((dir, name) -> name.endsWith(".java"));

            // Update each Java file and save it to the target directory
            if (javaFileNames != null) {
                for (String javaFileName : javaFileNames) {
                    String filePath = new File(packageDirectory, javaFileName).getPath();
                    String updatedContent = addPackageToJavaFile(filePath, packageName);
                    String targetFilePath = targetDirectoryPath + "/" + javaFileName;
                    writeContentToFile(updatedContent, targetFilePath);
                    System.out.println("Updated and moved: " + targetFilePath);
                }
            } else {
                System.out.println("No Java files found in the package: " + packageName);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Helper method to add package declaration to a Java file
    private static String addPackageToJavaFile(String filePath, String packageName) throws IOException {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            content.append("package ").append(packageName).append(";\n\n");
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }
        }
        return content.toString();
    }

    // Helper method to write content to a file
    private static void writeContentToFile(String content, String filePath) throws IOException {
        Path targetPath = Paths.get(filePath);
        Files.createDirectories(targetPath.getParent());
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            writer.write(content);
        }
    }
}
