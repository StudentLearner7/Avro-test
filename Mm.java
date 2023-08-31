   public static void printFields(Object obj) throws IllegalAccessException {
        Field[] fields = obj.getClass().getDeclaredFields();

        for (Field field : fields) {
            field.setAccessible(true);

            if (field.getType().equals(List.class)) {
                List<?> collection = (List<?>) field.get(obj);
                if (collection != null) {
                    System.out.println(field.getName() + " (Collection):");
                    for (Object item : collection) {
                        printFields(item);
                    }
                }
            } else {
                System.out.println(field.getName() + ": " + field.get(obj));
            }
        }
    }