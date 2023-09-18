String input = "@OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, orphanRemoval = true, mappedBy = \"parentEntity\")";

// Split the string by commas and spaces
String[] parts = input.split("[,\\s]+");

// Loop through the parts to find the "mappedBy" attribute
for (int i = 0; i < parts.length; i++) {
    if (parts[i].equals("mappedBy")) {
        String mappedByValue = parts[i + 2].replace("\"", "");
        System.out.println("MappedBy value: " + mappedByValue);
        break;
    }
}