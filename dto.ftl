public class ${entityName}DTO {

<#list fields as field>
    private ${field.type} ${field.name};
</#list>

    // Getters and setters
<#list fields as field>
    public ${field.type} get${field.name?cap_first}() {
        return ${field.name};
    }

    public void set${field.name?cap_first}(${field.type} ${field.name}) {
        this.${field.name} = ${field.name};
    }
</#list>
}
