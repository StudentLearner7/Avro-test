// ...

private ${entityName} toEntity(${entityName}DTO dto) {
    ${entityName} entity = new ${entityName}();
<#list fields as field>
    <#if nonPrimitiveFieldTypes?seq_contains(field.type)>
        entity.set${field.name?cap_first}(toEntity(dto.get${field.name?cap_first}()));
    <#else>
        entity.set${field.name?cap_first}(dto.get${field.name?cap_first}());
    </#if>
</#list>
    return entity;
}

private ${entityName}DTO toDTO(${entityName} entity) {
    ${entityName}DTO dto = new ${entityName}DTO();
<#list fields as field>
    <#if nonPrimitiveFieldTypes?seq_contains(field.type)>
        dto.set${field.name?cap_first}(toDTO(entity.get${field.name?cap_first}()));
    <#else>
        dto.set${field.name?cap_first}(entity.get${field.name?cap_first}());
    </#if>
</#list>
    return dto;
}

// ...
